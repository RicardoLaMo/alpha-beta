"""
Create sample Excel files for Canvas quiz attachments
"""
import pandas as pd
import random
from datetime import datetime, timedelta

def create_temperature_data_excel():
    """
    Create an Excel file with temperature data for student analysis.
    Students will need to perform calculations on this data.
    """
    # Generate sample temperature data for 30 days
    start_date = datetime(2024, 1, 1)
    dates = [start_date + timedelta(days=i) for i in range(30)]

    # Generate realistic temperature data (in Fahrenheit)
    random.seed(42)  # For reproducibility
    temp_f = [random.uniform(20, 85) for _ in range(30)]

    # Create DataFrame
    df = pd.DataFrame({
        'Date': dates,
        'Temperature_F': [round(t, 1) for t in temp_f],
        'Temperature_C': [''] * 30,  # Students will fill this
        'Temperature_K': [''] * 30   # Students will fill this
    })

    # Save to Excel
    filename = 'temperature_data.xlsx'
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Temperature Data', index=False)

        # Add instructions sheet
        instructions = pd.DataFrame({
            'Instructions': [
                '1. Download this Excel file',
                '2. Fill in the Temperature_C column by converting from Fahrenheit',
                '3. Fill in the Temperature_K column by converting from Celsius',
                '4. Use the formulas: C = (F - 32) × 5/9',
                '5. Use the formula: K = C + 273.15',
                '6. Calculate statistics as requested in the quiz',
                '',
                'Example:',
                'If Temperature_F = 68, then',
                'Temperature_C = (68 - 32) × 5/9 = 20.0',
                'Temperature_K = 20.0 + 273.15 = 293.15'
            ]
        })
        instructions.to_excel(writer, sheet_name='Instructions', index=False)

    print(f"Created {filename}")
    return filename


def create_sales_data_excel():
    """
    Create an Excel file with sales data for student analysis.
    """
    random.seed(123)

    products = ['Product A', 'Product B', 'Product C', 'Product D', 'Product E']
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']

    data = []
    for product in products:
        for month in months:
            data.append({
                'Product': product,
                'Month': month,
                'Units_Sold': random.randint(50, 200),
                'Price_Per_Unit': random.uniform(10, 50),
                'Total_Revenue': ''  # Students calculate this
            })

    df = pd.DataFrame(data)

    filename = 'sales_data.xlsx'
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Sales Data', index=False)

        # Add instructions
        instructions = pd.DataFrame({
            'Task': [
                'Calculate Total_Revenue for each row',
                'Find the product with highest total revenue',
                'Calculate average units sold per month',
                'Find the month with lowest sales',
                'Calculate total revenue across all products'
            ]
        })
        instructions.to_excel(writer, sheet_name='Tasks', index=False)

    print(f"Created {filename}")
    return filename


def create_statistics_data_excel():
    """
    Create an Excel file for statistics calculations.
    """
    random.seed(456)

    # Generate sample test scores
    students = [f'Student {i+1}' for i in range(25)]
    scores = [random.randint(65, 100) for _ in range(25)]

    df = pd.DataFrame({
        'Student_ID': students,
        'Test_Score': scores
    })

    # Add a summary section
    summary = pd.DataFrame({
        'Statistic': ['Mean', 'Median', 'Mode', 'Std Dev', 'Min', 'Max'],
        'Value': [''] * 6
    })

    filename = 'statistics_data.xlsx'
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Test Scores', index=False)
        summary.to_excel(writer, sheet_name='Summary Statistics', index=False)

        instructions = pd.DataFrame({
            'Instructions': [
                'Analyze the test scores data',
                'Calculate mean, median, mode, and standard deviation',
                'Fill in the Summary Statistics sheet',
                'Answer the questions in the quiz based on your calculations'
            ]
        })
        instructions.to_excel(writer, sheet_name='Instructions', index=False)

    print(f"Created {filename}")
    return filename


if __name__ == '__main__':
    print("Creating sample Excel files for Canvas quizzes...\n")
    create_temperature_data_excel()
    create_sales_data_excel()
    create_statistics_data_excel()
    print("\nAll sample Excel files created successfully!")
