"""
Example script for analyzing hotel phone numbers using the chinese_phone_parser package.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import re
from collections import Counter

from chinese_phone_parser import PhoneParser
from chinese_phone_parser.utils.helpers import (
    analyze_phone_dataset,
    get_phone_stats,
    plot_phone_formats,
    plot_area_code_map
)
from chinese_phone_parser.utils.constants import PLOT_COLORS


def main(file_path):
    """Main function to analyze hotel phone numbers from a CSV file."""
    print(f"Analyzing hotel phone numbers from {file_path}...")
    
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Rename the phone column if needed
    if '酒店电话' in df.columns:
        df = df.rename(columns={'酒店电话': 'phone'})
    
    # Get basic statistics about the dataset
    print(f"Total records: {len(df)}")
    print(f"Total phone numbers: {df['phone'].count()}")
    print(f"Unique phone numbers: {df['phone'].nunique()}")
    
    # Analyze the phone numbers
    analyzed_df = analyze_phone_dataset(df, 'phone')
    
    # Get detailed phone stats
    stats = get_phone_stats(df, 'phone')
    
    # Print summary of the analysis
    print("\nSummary of Hotel Phone Number Analysis:")
    print(f"1. Total phone numbers analyzed: {stats['total_count']}")
    print(f"2. Unique phone numbers: {stats['unique_count']} ({stats['unique_percentage']:.2f}%)")
    
    # Most common digit count
    if 'patterns' in stats and 'digit_counts' in stats['patterns']:
        most_common_length = max(stats['patterns']['digit_counts'].items(), key=lambda x: x[1])
        print(f"3. Most common phone number length: {most_common_length[0]} digits")
    
    # Pattern statistics
    if 'patterns' in stats:
        patterns = stats['patterns']
        print(f"4. {patterns.get('multiple_count', 0)} hotels have multiple phone numbers listed")
        print(f"5. {patterns.get('extension_count', 0)} phone numbers include extensions")
        print(f"6. {patterns.get('international_count', 0)} phone numbers are in international format")
        print(f"7. {patterns.get('missing_area_count', 0)} phone numbers have missing area codes")
        print(f"8. {patterns.get('no_area_code_count', 0)} phone numbers have no area code (just 7-8 digits)")
        print(f"9. {patterns.get('concatenated_count', 0)} phone numbers appear to be concatenated without proper formatting")
        print(f"10. {patterns.get('mobile_count', 0)} phone numbers are mobile numbers")
        print(f"11. {patterns.get('mixed_format_count', 0)} phone numbers mix area codes with mobile numbers")
        print(f"12. {patterns.get('tollfree_count', 0)} phone numbers are toll-free numbers (400/800)")
    
    # Most common format
    if 'format_counts' in stats:
        most_common_format = max(stats['format_counts'].items(), key=lambda x: x[1])
        print(f"13. Most common phone format: {most_common_format[0]} with {most_common_format[1]} occurrences")
    
    # Find examples of different phone formats
    print("\nExamples of Different Phone Formats:")
    
    # Mobile examples
    mobile_examples = analyzed_df[analyzed_df['phone_format'] == 'Mobile']['phone'].head(3)
    print(f"\nMobile numbers:")
    for example in mobile_examples:
        print(f"  - {example}")
    
    # International examples
    intl_examples = analyzed_df[analyzed_df['phone_format'].str.contains('International')]['phone'].head(3)
    print(f"\nInternational format:")
    for example in intl_examples:
        print(f"  - {example}")
    
    # Landline examples
    landline_examples = analyzed_df[analyzed_df['phone_format'] == 'Domestic (0XX)']['phone'].head(3)
    print(f"\nLandline numbers:")
    for example in landline_examples:
        print(f"  - {example}")
    
    # Multiple numbers examples
    multiple_examples = df[df['phone'].astype(str).str.contains('/')]['phone'].head(3)
    print(f"\nMultiple numbers:")
    for example in multiple_examples:
        print(f"  - {example}")
    
    # Toll-free examples
    tollfree_examples = analyzed_df[analyzed_df['phone_format'].str.contains('Toll-Free')]['phone'].head(3)
    print(f"\nToll-free numbers:")
    for example in tollfree_examples:
        print(f"  - {example}")
    
    # Concatenated examples
    concat_examples = analyzed_df[analyzed_df['phone_format'] == 'Concatenated']['phone'].head(3)
    print(f"\nConcatenated numbers:")
    for example in concat_examples:
        print(f"  - {example}")
    
    # Create visualization of phone formats
    format_fig = plot_phone_formats(df, 'phone', PLOT_COLORS)
    format_fig.write_html("hotel_phone_formats.html")
    print("\nGenerated 'hotel_phone_formats.html' with phone format distribution")
    
    # Create visualization of area codes
    area_fig = plot_area_code_map(df, 'phone', top_n=15, color_scheme=PLOT_COLORS)
    area_fig.write_html("hotel_area_codes.html")
    print("Generated 'hotel_area_codes.html' with top area codes")
    
    # Check for problematic phone numbers
    print("\nExamples of Problematic Phone Numbers:")
    
    # Empty phone numbers
    empty_count = len(df[df['phone'].isna() | (df['phone'].astype(str).str.strip() == '')])
    print(f"\nEmpty phone numbers count: {empty_count}")
    
    # Unusually short phone numbers
    short_phones = df[df['phone'].astype(str).apply(lambda x: len(re.sub(r'\D', '', x)) < 7 and len(re.sub(r'\D', '', x)) > 0)]
    print(f"\nUnusually short phone numbers count: {len(short_phones)}")
    if not short_phones.empty:
        print("Examples:")
        for phone in short_phones['phone'].head(3):
            print(f"  - {phone}")
    
    # Unknown format phones
    unknown_format = analyzed_df[analyzed_df['phone_format'] == 'Other']
    print(f"\nUnknown format phone numbers count: {len(unknown_format)}")
    if not unknown_format.empty:
        print("Examples:")
        for phone in unknown_format['phone'].head(3):
            print(f"  - {phone}")
    
    print("\nAnalysis complete!")


if __name__ == "__main__":
    # Example usage
    # main("path/to/your/hotel_data.csv")
    
    # For demonstration, let's create a small sample dataset
    sample_data = {
        'hotel_id': list(range(1, 21)),
        '酒店电话': [
            '+86-010-12345678',
            '13812345678',
            '0755-87654321',
            '400-123-4567',
            '010-12345678 转 123',
            '+86-13812345678',
            '0086-755-12345678',
            '0531-12345678',
            '13987654321 / 0571-12345678',
            '0571-12345678, 13712345678',
            '020-12345678;021-87654321',
            '01012345678139********',  # Concatenated
            '0755-',  # Incomplete
            '',  # Empty
            '12345',  # Too short
            '010-12345678-123',  # With extension
            '0592-12345678',
            '0771-12345678',
            '800-123-4567',
            '13512345678'
        ]
    }
    
    # Create a temporary CSV file
    sample_df = pd.DataFrame(sample_data)
    sample_file = "sample_hotel_data.csv"
    sample_df.to_csv(sample_file, index=False)
    
    # Run the analysis
    main(sample_file)