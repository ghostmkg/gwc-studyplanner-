# Utility: Date Formatter for Study Planner

from datetime import datetime

def format_date(date_str):
    """
    Convert date string from 'YYYY-MM-DD' to a more friendly format like '23 October 2025'.
    """
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%d %B %Y")
    except ValueError:
        return "Invalid date format. Please use YYYY-MM-DD."

# Example usage
if __name__ == "__main__":
    sample_date = "2025-10-23"
    print("Formatted Date:", format_date(sample_date))
