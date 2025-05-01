"""
Basic usage examples for the Chinese phone number parser.
"""

import pandas as pd
from cn_phone_parser import PhoneParser
from cn_phone_parser.cleaner import clean_phone_number, normalize_phone
from cn_phone_parser.extractor import extract_area_code, extract_phone_numbers
from cn_phone_parser.validator import categorize_phone_format
from cn_phone_parser.utils.helpers import analyze_phone_dataset, get_phone_stats, plot_phone_formats

def example_single_phone():
    """Example of parsing a single phone number."""
    parser = PhoneParser()
    
    # Parse different formats
    examples = [
        "+86-010-12345678",
        "13812345678",
        "0755-87654321",
        "400-123-4567",
        "0086-021-12345678",
        "010-12345678 转 123",
        "13812345678 / 010-12345678"
    ]
    
    for phone in examples:
        result = parser.parse(phone)
        print(f"\nOriginal: {phone}")
        print(f"Parsed: {result}")


def example_dataframe():
    """Example of processing a dataframe of phone numbers."""
    # Create a sample dataframe
    data = {
        'id': [1, 2, 3, 4, 5],
        'phone': [
            '+86-010-12345678',
            '13812345678',
            '0755-87654321',
            '400-123-4567',
            '010-12345678 转 123'
        ]
    }
    df = pd.DataFrame(data)
    
    # Process the dataframe
    result_df = analyze_phone_dataset(df, 'phone')
    
    # Print the results
    print("\nProcessed DataFrame:")
    print(result_df)
    
    # Get statistics
    stats = get_phone_stats(df, 'phone')
    print("\nPhone Statistics:")
    print(f"Total count: {stats['total_count']}")
    print(f"Unique count: {stats['unique_count']}")
    print(f"Format counts: {stats['format_counts']}")


def example_visualization():
    """Example of visualizing phone number data."""
    # Create a sample dataframe
    data = {
        'id': list(range(1, 21)),
        'phone': [
            '+86-010-12345678',
            '13812345678',
            '0755-87654321',
            '400-123-4567',
            '010-12345678 转 123',
            '+86-13812345678',
            '0086-755-12345678',
            '0531-12345678',
            '13987654321',
            '0571-12345678',
            '13712345678',
            '020-12345678',
            '021-12345678',
            '0755-12345678',
            '010-87654321',
            '13612345678',
            '0592-12345678',
            '0771-12345678',
            '800-123-4567',
            '13512345678'
        ]
    }
    df = pd.DataFrame(data)
    
    # Create a format distribution plot
    fig = plot_phone_formats(df, 'phone')
    
    # In a real application, you would save or display this figure
    # fig.write_html("phone_formats.html")
    print("\nVisualization example:")
    print("A plot of phone formats has been created. In a real application, this would be saved or displayed.")


if __name__ == "__main__":
    print("Chinese Phone Number Parser - Basic Usage Examples")
    print("=" * 50)
    
    example_single_phone()
    example_dataframe()
    example_visualization()