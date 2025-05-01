# Chinese Phone Number Parser Usage Guide

This document provides detailed usage instructions for the Chinese Phone Number Parser package.

## Installation

```bash
pip install chinese-phone-parser
```

## Basic Usage

### Parsing a Single Phone Number

```python
from chinese_phone_parser import PhoneParser

# Create a parser instance
parser = PhoneParser()

# Parse a phone number
result = parser.parse("+86-010-12345678")
print(result)
```

Output:
```
{
    'original': '+86-010-12345678',
    'normalized': '+8601012345678',
    'type': 'landline',
    'area_code': '010',
    'city': 'Beijing'
}
```

### Individual Functions

You can also use the individual functions directly:

```python
from chinese_phone_parser.cleaner import clean_phone_number, normalize_phone
from chinese_phone_parser.extractor import extract_area_code, extract_phone_numbers
from chinese_phone_parser.validator import is_valid_phone_number, categorize_phone_format

# Clean a phone number
cleaned = clean_phone_number("+86 (010) 1234-5678")
print(cleaned)  # +86010-12345678

# Normalize a phone number
normalized = normalize_phone(cleaned)
print(normalized)  # +8601012345678

# Extract area code
area_code = extract_area_code(normalized)
print(area_code)  # 010

# Check if valid
is_valid = is_valid_phone_number(normalized)
print(is_valid)  # True

# Categorize format
format_type = categorize_phone_format(normalized)
print(format_type)  # landline

# Extract multiple phone numbers from text
text = "Contact us at +86-010-12345678 or 13812345678"
numbers = extract_phone_numbers(text)
print(numbers)  # ['+86-010-12345678', '13812345678']
```

## Advanced Features

### Analyze a Dataset with Phone Numbers

```python
import pandas as pd
from chinese_phone_parser.utils.helpers import analyze_phone_dataset

# Sample dataframe with phone numbers
df = pd.DataFrame({
    'id': [1, 2, 3, 4],
    'name': ['Hotel A', 'Hotel B', 'Hotel C', 'Hotel D'],
    'phone': ['+86-010-12345678', '0755-87654321', '13812345678', '400-123-4567']
})

# Analyze the dataset
result_df = analyze_phone_dataset(df, phone_column='phone')
print(result_df.head())
```

The output will include additional columns with phone analysis:
- `phone_cleaned`: Cleaned phone number
- `phone_normalized`: Normalized phone number
- `phone_type`: Type of phone (mobile, landline, toll-free)
- `phone_area_code`: Area code (if applicable)
- `phone_city`: City corresponding to area code
- `phone_is_valid`: Validity flag

### Get Comprehensive Statistics

```python
from chinese_phone_parser.utils.helpers import get_phone_stats

# Get statistics about phone numbers in a dataset
stats = get_phone_stats(df, phone_column='phone')
print(stats)
```

### Analyze Phone Patterns

```python
from chinese_phone_parser.utils.helpers import analyze_phone_patterns

# Sample list of phone numbers
phone_list = [
    '+86-010-12345678',
    '0755-87654321',
    '13812345678',
    '400-123-4567',
    '010-12345678-123'
]

patterns = analyze_phone_patterns(phone_list)
print(patterns)
```

### Visualization

```python
from chinese_phone_parser.utils.helpers import plot_phone_formats, plot_area_code_map

# Create visualization of phone formats
fig1 = plot_phone_formats(df, phone_column='phone')
fig1.show()

# Create map visualization of area codes
fig2 = plot_area_code_map(df, phone_column='phone', top_n=10)
fig2.show()
```

## Supported Phone Number Formats

The package supports various Chinese phone number formats:

### Mobile Numbers (11 digits)
- Standard: `13812345678`
- International: `+86 138 1234 5678`
- With prefix: `0086-13812345678`

### Landline Numbers
- Local: `010-12345678`
- With area code: `0755-87654321`
- International: `+86 10 1234 5678`

### Toll-Free Numbers (10 digits)
- 400 numbers: `400-123-4567`
- 800 numbers: `800-123-4567`

### Special Formats
- With extensions: 
  - `010-12345678-123`
  - `0755-87654321 转 456`
  - `010-12345678 ext 789`
  - `010-12345678 分机 321`
- Multiple numbers:
  - `010-12345678 / 13812345678`
  - `0755-87654321, 400-123-4567`
- Concatenated numbers without delimiters
- Missing area codes
- Service numbers (110, 12345, etc.)

## Error Handling

The package is designed to handle various edge cases:

```python
from chinese_phone_parser import PhoneParser

parser = PhoneParser()

# Handling None or empty string
result1 = parser.parse(None)
print(result1)  # None

# Handling invalid format
result2 = parser.parse("not-a-phone-number")
print(result2)  # Returns basic structure but with validation flags indicating issues
```

## Performance Considerations

For large datasets, consider using batch processing:

```python
import pandas as pd
from chinese_phone_parser.utils.helpers import analyze_phone_dataset

# Process in chunks for large datasets
chunk_size = 10000
for chunk in pd.read_csv('large_dataset.csv', chunksize=chunk_size):
    processed_chunk = analyze_phone_dataset(chunk, phone_column='phone')
    # Save or process each chunk
    # ...
``` 