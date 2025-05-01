# Chinese Phone Number Parser - Usage Guide

This guide provides detailed instructions for using the `cn_phone_parser` package to clean, normalize, and analyze Chinese phone numbers.

## Table of Contents

- [Chinese Phone Number Parser - Usage Guide](#chinese-phone-number-parser---usage-guide)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Basic Usage](#basic-usage)
  - [Working with Single Phone Numbers](#working-with-single-phone-numbers)
    - [Parse a Phone Number](#parse-a-phone-number)
    - [Clean and Normalize](#clean-and-normalize)
    - [Extract Components](#extract-components)
    - [Validate and Categorize](#validate-and-categorize)
  - [Working with DataFrames](#working-with-dataframes)
  - [Analyzing Phone Numbers](#analyzing-phone-numbers)
  - [Visualizing Phone Data](#visualizing-phone-data)
  - [Handling Specific Phone Formats](#handling-specific-phone-formats)
    - [Mobile Numbers](#mobile-numbers)
    - [Landline Numbers](#landline-numbers)
    - [Numbers with Extensions](#numbers-with-extensions)
    - [Multiple Numbers in One String](#multiple-numbers-in-one-string)
  - [API Reference](#api-reference)
    - [Main Classes](#main-classes)
    - [Cleaner Module](#cleaner-module)
    - [Extractor Module](#extractor-module)
    - [Validator Module](#validator-module)
    - [Helper Functions](#helper-functions)
    - [Data](#data)

## Installation

Install the package using pip:

```bash
pip install cn-phone-parser
```

## Basic Usage

Import the required modules:

```python
from cn_phone_parser import PhoneParser
from cn_phone_parser.cleaner import clean_phone_number, normalize_phone
from cn_phone_parser.extractor import extract_area_code, extract_phone_numbers
from cn_phone_parser.validator import categorize_phone_format
from cn_phone_parser.utils.helpers import analyze_phone_dataset
```

## Working with Single Phone Numbers

### Parse a Phone Number

Use the `PhoneParser` class to get detailed information about a phone number:

```python
parser = PhoneParser()
result = parser.parse("+86-010-12345678")
print(result)
# Output:
# {
#     'original': '+86-010-12345678',
#     'normalized': '+8601012345678',
#     'type': 'International (+86)',
#     'area_code': '010',
#     'city': 'Beijing'
# }
```

### Clean and Normalize

Clean and normalize phone numbers:

```python
# Clean a phone number (handle multiple numbers, etc.)
cleaned = clean_phone_number("010-12345678, 13812345678")
print(cleaned)  # Output: 010-12345678

# Normalize a phone number (remove non-digits)
normalized = normalize_phone("010-12345678")
print(normalized)  # Output: 01012345678
```

### Extract Components

Extract components from phone numbers:

```python
# Extract area code
area_code = extract_area_code("010-12345678")
print(area_code)  # Output: 010

# Extract extension
from cn_phone_parser.extractor import extract_extension
extension_info = extract_extension("010-12345678 转 123")
print(extension_info)  # Output: {'main': '010-12345678', 'extension': '123'}

# Extract multiple phone numbers from text
phone_numbers = extract_phone_numbers("Contact us at 010-12345678 or 13812345678")
print(phone_numbers)  # Output: ['010-12345678', '13812345678']
```

### Validate and Categorize

Validate and categorize phone numbers:

```python
from cn_phone_parser.validator import validate_phone, categorize_phone_format

# Validate a phone number
is_valid, error_msg = validate_phone("13812345678")
print(is_valid, error_msg)  # Output: True, ""

# Categorize a phone number
format_category = categorize_phone_format("010-12345678")
print(format_category)  # Output: Domestic (0XX)
```

## Working with DataFrames

Analyze a DataFrame containing phone numbers:

```python
import pandas as pd
from cn_phone_parser.utils.helpers import analyze_phone_dataset

# Create a sample DataFrame
df = pd.DataFrame({
    'id': [1, 2, 3],
    'phone': ['+86-010-12345678', '13812345678', '0755-87654321']
})

# Process the DataFrame
result_df = analyze_phone_dataset(df, 'phone')
print(result_df)
```

The resulting DataFrame will have additional columns:
- `clean_phone`: Cleaned phone number
- `normalized_phone`: Normalized phone number
- `area_code`: Extracted area code
- `city`: City corresponding to the area code
- `phone_format`: Format category of the phone number

## Analyzing Phone Numbers

Get statistics about phone numbers in a dataset:

```python
from cn_phone_parser.utils.helpers import get_phone_stats

# Get phone statistics
stats = get_phone_stats(df, 'phone')
print(stats)
```

The stats dictionary contains:
- `total_count`: Total number of phone numbers
- `unique_count`: Number of unique phone numbers
- `unique_percentage`: Percentage of unique phone numbers
- `format_counts`: Counts of different phone formats
- `area_code_counts`: Counts of different area codes
- `city_counts`: Counts of different cities
- `patterns`: Detailed pattern analysis

## Visualizing Phone Data

Create visualizations of phone number data:

```python
from cn_phone_parser.utils.helpers import plot_phone_formats, plot_area_code_map

# Plot phone formats
format_fig = plot_phone_formats(df, 'phone')
format_fig.write_html("phone_formats.html")

# Plot area code distribution
area_fig = plot_area_code_map(df, 'phone', top_n=10)
area_fig.write_html("area_codes.html")
```

## Handling Specific Phone Formats

### Mobile Numbers

Check if a number is a mobile number:

```python
from cn_phone_parser.validator import is_mobile_number

is_mobile = is_mobile_number("13812345678")
print(is_mobile)  # Output: True
```

### Landline Numbers

Check if a number is a landline number:

```python
from cn_phone_parser.validator import is_landline_number

is_landline = is_landline_number("010-12345678")
print(is_landline)  # Output: True
```

### Numbers with Extensions

Extract the main number and extension:

```python
from cn_phone_parser.extractor import extract_extension

result = extract_extension("010-12345678 转 123")
print(result)  # Output: {'main': '010-12345678', 'extension': '123'}
```

### Multiple Numbers in One String

Extract all phone numbers from a string:

```python
from cn_phone_parser.extractor import extract_phone_numbers

numbers = extract_phone_numbers("Contact us at 010-12345678 or 13812345678")
print(numbers)  # Output: ['010-12345678', '13812345678']
```

## API Reference

### Main Classes

- `PhoneParser`: Main class for parsing phone numbers

### Cleaner Module

- `clean_phone_number(phone)`: Clean a phone number string
- `normalize_phone(phone)`: Normalize a phone number by removing non-digits
- `convert_to_standard_format(phone)`: Convert a normalized phone number to a standard display format

### Extractor Module

- `extract_area_code(phone)`: Extract the area code from a phone number
- `extract_phone_numbers(text)`: Extract all phone numbers from a text string
- `extract_extension(phone)`: Extract the extension from a phone number

### Validator Module

- `validate_phone(phone)`: Validate if a string is a valid Chinese phone number
- `categorize_phone_format(phone)`: Categorize a phone number into different format types
- `is_mobile_number(phone)`: Check if a phone number is a Chinese mobile number
- `is_landline_number(phone)`: Check if a phone number is a Chinese landline number

### Helper Functions

- `analyze_phone_patterns(phones)`: Analyze phone number patterns in a list of phone numbers
- `analyze_phone_dataset(df, phone_column)`: Analyze a dataset containing phone numbers
- `get_phone_stats(df, phone_column)`: Get statistics about phone numbers in a dataset
- `plot_phone_formats(df, phone_column)`: Create a bar chart of phone number formats
- `plot_area_code_map(df, phone_column)`: Create a bar chart of the top area codes

### Data

- `area_code_to_city`: Dictionary mapping area codes to cities
- `mobile_prefix_to_carrier`: Dictionary mapping mobile prefixes to carriers
- `get_carrier(mobile_number)`: Get the carrier from a mobile number prefix