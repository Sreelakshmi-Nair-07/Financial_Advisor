"""
Calculator Tool - Performs mathematical calculations for budgeting and financial planning.
"""

import re
from typing import Union
from langchain.tools import Tool
from langchain.pydantic_v1 import BaseModel, Field


class CalculatorInput(BaseModel):
    """Input schema for calculator tool."""
    expression: str = Field(description="Mathematical expression to calculate (e.g., '15% of 10000', '5000 * 0.3', '(5000 - 1000) / 12')")


def safe_calculate(expression: str) -> str:
    """
    Safely evaluate mathematical expressions for financial calculations.
    
    Args:
        expression: Mathematical expression (supports +, -, *, /, %, parentheses, and percentages)
        
    Returns:
        Calculation result or error message
    """
    try:
        # Validate input
        if not expression or not expression.strip():
            return "❌ Error: Please provide a mathematical expression to calculate."
        
        expression = expression.strip()
        original_expression = expression
        
        # Handle percentage expressions (e.g., "15% of 10000" or "20% * 5000")
        percent_patterns = [
            (r'(\d+\.?\d*)\s*%\s*of\s*(\d+\.?\d*)', lambda m: f"({m.group(1)} / 100) * {m.group(2)}"),
            (r'(\d+\.?\d*)\s*%\s*\*\s*(\d+\.?\d*)', lambda m: f"({m.group(1)} / 100) * {m.group(2)}"),
            (r'(\d+\.?\d*)\s*\*\s*(\d+\.?\d*)\s*%', lambda m: f"{m.group(1)} * ({m.group(2)} / 100)"),
        ]
        
        for pattern, replacement in percent_patterns:
            expression = re.sub(pattern, replacement, expression)
        
        # Remove any non-mathematical characters (security)
        # Allow: digits, operators, parentheses, decimal points, spaces
        if not re.match(r'^[\d\s\+\-\*\/\(\)\.\%]+$', expression):
            return f"❌ Error: Invalid characters in expression. Only numbers and operators (+, -, *, /, %, parentheses) are allowed."
        
        # Replace % with /100 for remaining percentages
        expression = re.sub(r'(\d+\.?\d*)%', r'(\1/100)', expression)
        
        # Evaluate the expression safely
        result = eval(expression, {"__builtins__": {}}, {})
        
        # Format the result
        response = f"""
🧮 **Calculator Result**

**Expression**: {original_expression}
**Result**: {result:,.2f}

**Formatted Results**:
"""
        
        # Add different formats
        response += f"- Decimal: {result:.2f}\n"
        response += f"- Rounded: {round(result):,}\n"
        
        # If the result is a reasonable money amount, show it
        if 0 < result < 1_000_000_000:
            response += f"- Currency: ${result:,.2f}\n"
        
        # Add percentage if it makes sense
        if 0 < result < 100:
            response += f"- As Percentage: {result:.2f}%\n"
        
        # Add financial context based on the expression
        if 'of' in original_expression.lower() or '%' in original_expression:
            response += f"\n💡 **Financial Context**: This could represent a portion of a budget, investment, or savings."
        
        return response
        
    except ZeroDivisionError:
        return "❌ Error: Division by zero is not allowed."
    except SyntaxError:
        return f"❌ Error: Invalid mathematical syntax in '{original_expression}'. Please check your expression."
    except Exception as e:
        return f"❌ Error calculating '{original_expression}': {str(e)}"


def get_calculator_tool() -> Tool:
    """
    Create and return the calculator tool for LangChain agent.
    
    Returns:
        Tool: LangChain Tool for calculations
    """
    return Tool(
        name="Calculator",
        func=safe_calculate,
        description="""
        Useful for performing mathematical calculations including budgeting, percentages, and financial planning.
        Input should be a mathematical expression like:
        - "15% of 10000" (calculate percentage)
        - "5000 * 0.3" (multiplication)
        - "(5000 - 1000) / 12" (monthly budget calculation)
        - "10000 + 2000 - 500" (addition and subtraction)
        Returns the calculated result with different formats.
        Use this tool for any mathematical calculations, especially budgeting and financial planning.
        """,
        args_schema=CalculatorInput
    )


# For testing purposes
if __name__ == "__main__":
    # Test with various expressions
    test_expressions = [
        "15% of 10000",
        "5000 * 0.3",
        "(5000 - 1000) / 12",
        "10000 + 2000 - 500",
        "30% * 5000",
        "100 / 0",  # Error case
        "invalid expression !!",  # Error case
    ]
    
    for expr in test_expressions:
        print(f"\n{'='*60}")
        print(f"Testing: {expr}")
        print('='*60)
        result = safe_calculate(expr)
        print(result)

