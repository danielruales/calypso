import litellm
import os
from pathlib import Path


class BaselineAgent:
    """
    Baseline AI Data Scientist agent that generates Python code to answer questions
    about CSV data using only schema information and file names.
    """
    
    def __init__(self, model="gpt-4.1-mini"):
        self.model = model
        self.schema_path = Path("../data/schema.md")
        self.data_files = {
            "products": "../data/products.csv",
            "customers": "../data/customers.csv", 
            "orders": "../data/orders.csv"
        }
    
    def load_schema(self) -> str:
        """Load the schema.md file content"""
        try:
            with open(self.schema_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Schema file not found: {self.schema_path}")
    
    def generate_code(self, question: str) -> str:
        """
        Generate Python code to answer a data science question
        
        Args:
            question (str): The data analysis question to answer
            
        Returns:
            str: Python code that answers the question
        """
        schema = self.load_schema()
        
        # Create the prompt
        prompt = f"""
You are an expert Python data scientist. Generate Python code to answer the following question using pandas.

AVAILABLE DATA FILES:
- products.csv (load with: df_products = pd.read_csv('../data/products.csv'))
- customers.csv (load with: df_customers = pd.read_csv('../data/customers.csv'))
- orders.csv (load with: df_orders = pd.read_csv('../data/orders.csv'))

DATABASE SCHEMA:
{schema}

QUESTION: {question}

REQUIREMENTS:
1. Import pandas as pd and any other needed libraries
2. Load only the CSV files you need for this analysis
3. Write clear, efficient pandas code
4. Include comments explaining your approach
5. Print the final result
6. Handle any data type conversions if needed
7. Only output the Python code, no explanations before or after

Example format:
```python
import pandas as pd
import matplotlib.pyplot as plt

# Load data
df_products = pd.read_csv('../data/products.csv')

# Your analysis code here
result = df_products.groupby('product_category')['product_price'].mean()
print(result)
```

Generate the Python code:
"""

        try:
            response = litellm.completion(
                model=self.model,
                messages=[{
                    "role": "user", 
                    "content": prompt
                }],
                temperature=0.1  # Low temperature for more consistent code generation
            )
            
            # Extract code from response
            code = response['choices'][0]['message']['content']
            
            # Clean up the code (remove markdown formatting if present)
            if '```python' in code:
                code = code.split('```python')[1].split('```')[0].strip()
            elif '```' in code:
                code = code.split('```')[1].split('```')[0].strip()
            
            return code
            
        except Exception as e:
            return f"Error generating code: {str(e)}"
    
    def generate_visualization_code(self, question: str) -> str:
        """
        Generate Python code for visualizing data analysis results.
        The LLM automatically chooses the best chart type for the data and question.
        
        Args:
            question (str): The data analysis question to visualize
            
        Returns:
            str: Python code that creates an appropriate visualization
        """
        schema = self.load_schema()
        
        # Create the prompt for visualization
        prompt = f"""
You are an expert Python data scientist creating visualizations for non-technical business users. Generate Python code to create the most appropriate visualization that answers the following question.

AVAILABLE DATA FILES:
- products.csv (load with: df_products = pd.read_csv('../data/products.csv'))
- customers.csv (load with: df_customers = pd.read_csv('../data/customers.csv'))
- orders.csv (load with: df_orders = pd.read_csv('../data/orders.csv'))

DATABASE SCHEMA:
{schema}

QUESTION: {question}

REQUIREMENTS:
1. Import pandas, matplotlib.pyplot, and seaborn
2. Load only the CSV files you need for this visualization
3. Process the data to answer the question
4. Automatically choose the BEST chart type for the data and question:
   - Bar charts for categorical comparisons (maintain DataFrame order by using the `order=` argument with Seaborn)
   - Line plots for trends over time
   - Pie charts for parts of a whole (max 6 categories)
   - Histograms for distributions
   - Scatter plots for relationships between variables
   - Box plots for statistical summaries
5. Add clear, business-friendly title and labels
6. Use colors and formatting that are professional and easy to read
7. Use `plt.show()` to display the chart
8. Annotate bar charts by matching annotation order to actual bar positions using `order=` in `sns.barplot()` or `ax.patches`
9. Make the chart accessible to non-technical users
10. Only output the Python code, no explanations before or after
11. Ensure labels and annotations do not overlap with the chart edges. If necessary, use plt.subplots_adjust(right=0.85) to create extra space for labels on the right or bbox positioning for tight text placement.
12.	If you add text labels using a loop, reset the DataFrame index or use enumerate() to avoid spacing/layout issues in the chart.
13. Set an appropriate figure size using `plt.figure(figsize=(width, height))`, where `height` scales with the number of bars (e.g., `len(df) * 0.6`) to prevent excessive whitespace.


Example format:
```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df_products = pd.read_csv('../data/products.csv')

# Process data for visualization
category_prices = df_products.groupby('product_category')['product_price'].mean()

# Create visualization
plt.figure(figsize=(10, 6))
category_prices.plot(kind='bar')
plt.title('Average Product Price by Category')
plt.xlabel('Product Category')
plt.ylabel('Average Price ($)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```

Generate the Python visualization code:
"""

        try:
            response = litellm.completion(
                model=self.model,
                messages=[{
                    "role": "user", 
                    "content": prompt
                }],
                temperature=0.1  # Low temperature for more consistent code generation
            )
            
            # Extract code from response
            code = response['choices'][0]['message']['content']
            
            # Clean up the code (remove markdown formatting if present)
            if '```python' in code:
                code = code.split('```python')[1].split('```')[0].strip()
            elif '```' in code:
                code = code.split('```')[1].split('```')[0].strip()
            
            return code
            
        except Exception as e:
            return f"Error generating visualization code: {str(e)}"

    def analyze(self, question: str, execute: bool = False, include_viz: bool = False) -> dict:
        """
        Analyze a question and optionally execute the generated code
        
        Args:
            question (str): The data analysis question
            execute (bool): Whether to execute the generated code
            include_viz (bool): Whether to include visualization code (LLM chooses best chart type)
            
        Returns:
            dict: Contains 'question', 'code', and optionally 'result', 'viz_code'
        """
        code = self.generate_code(question)
        
        result = {
            'question': question,
            'code': code
        }
        
        if include_viz:
            viz_code = self.generate_visualization_code(question)
            result['viz_code'] = viz_code
        
        if execute:
            try:
                # Execute the code in a local namespace
                exec_globals = {}
                exec(code, exec_globals)
                result['status'] = 'success'
                
                # Execute visualization code if included
                if include_viz:
                    exec(result['viz_code'], exec_globals)
                    
            except Exception as e:
                result['status'] = 'error'
                result['error'] = str(e)
        
        return result


# Example usage functions
def demo_questions():
    """Demo questions for testing the agent"""
    return [
        "What are the top 5 most expensive products?",
        "How many customers are there by state?",
        "What is the total revenue by product category?",
        "Which customers have made the most orders?",
        "What is the average order value by customer age group?",
        "Show the monthly sales trend",
        "Which product categories are most popular by customer gender?",
        "What is the distribution of customer ages?",
        "Find the top 10 customers by total spending",
        "Calculate the average product price by brand"
    ]


if __name__ == "__main__":
    # Initialize the agent
    agent = BaselineAgent()
    
    # Test with a sample question
    question = "What are the top 5 most expensive products?"
    result = agent.analyze(question)
    
    print(f"Question: {result['question']}")
    print(f"Generated Code:\n{result['code']}")
