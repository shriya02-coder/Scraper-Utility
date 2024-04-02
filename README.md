# Scraper-Utility

This Python script allows users to search for specific values within an Excel file or to search for values/identifiers within log data, highlighting relevant rows in Excel and processing log data based on user input.

## Features

- **Excel Data Processing**: Search in a specific sheet of an Excel workbook and highlight rows where the specified values are found in a selected column.
- **Log Data Processing**: Allows searching within log data either by specific values or identifiers. For identifiers, you can choose to extract either a certain number of characters or words following the identifier.

## Usage

1. **Select Data Source**: Choose between processing data from an Excel file or log entries.


2. **For Excel Files**: 
   - Enter the path to the Excel file.
   - Select a specific sheet to search in.
   - Choose a column for searching or search across all columns.
   - Enter the values to search for. Rows containing these values in the specified column will be highlighted.


3. **For Log Data**: 
   - Paste the log data directly into the console.
   - Choose between searching by value or identifier.
   - For identifiers, specify whether to extract characters or words following the identifier, and the number to extract.

