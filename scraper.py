
import os
import pandas as pd
import openpyxl
import re
from openpyxl.styles import PatternFill

def highlight_rows(file_path, sheet_name, column_name, search_values):
    """
    The function `highlight_rows` takes a file path, sheet name, column name, search values, and
    highlights rows in a specified column based on the search values, saving the modified file with a
    new name.
    
    :param file_path: The `file_path` parameter should be the path to the Excel file that you want to
    work with. This should be a string that includes the full path to the file, including the file name
    and extension. For example, it could be something like "C:/Users/username/Documents/data.xlsx"
    
    :param sheet_name: The `sheet_name` parameter refers to the name of the specific sheet within the
    Excel file where you want to highlight rows based on the search values. This function will iterate
    through the rows in the specified sheet, check the values in the specified column (if provided), and
    highlight the entire row if the value is present
    
    :param column_name: The `column_name` parameter in the `highlight_rows` function is used to specify
    the name of the column in the Excel sheet where you want to search for the values specified in the
    `search_values` list. The function will only search for the values in the specified column. If you
    want to search in all columns press 0.
    
    :param search_values: The `search_values` parameter should be a list of values that you want to
    search for in the specified column of the Excel file. For example, if you want to highlight rows
    where the value in the "Status" column is either "Pending" or "In Progress", your `search_values`
    """
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook[sheet_name]
    yellow_fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")

    col_index = None
    if column_name:
        col_index = openpyxl.utils.cell.column_index_from_string(column_name)

    for row in sheet.iter_rows():
        for cell in row:
            if col_index is None or cell.column == col_index:
                if str(cell.value) in search_values:
                    for cell in row:
                        cell.fill = yellow_fill
                    break

    dir_path, file_name = os.path.split(file_path)
    new_file_name = 'highlighted_' + file_name
    new_file_path = os.path.join(dir_path, new_file_name)
    workbook.save(new_file_path)

def main():
    """
    The main function allows the user to select a data source (Excel or logs) and search for specific
    values or identifiers within the data.
    """
    data_source = input("Select data source (1 for Excel, 2 for logs): ")

    if data_source == "1":
        file_path = input("Please enter the Excel file path: ")
        workbook = openpyxl.load_workbook(file_path)
        print("Sheets available:")
        for i, sheet in enumerate(workbook.sheetnames, start=1):
            print(f"{i}. {sheet}")

        sheet_num = input("Enter the number of the sheet you want to search: ")
        sheet_name = workbook.sheetnames[int(sheet_num) - 1]
        sheet = workbook[sheet_name]

        print("\nColumn headers in this sheet:")
        columns = [cell.value for cell in next(sheet.iter_rows(min_row=1, max_row=1))]
        for i, col in enumerate(columns, start=1):
            print(f"{i}. {col}")
        col_choice = input("Enter the column number to search in (0 for all columns): ")
        column_name = openpyxl.utils.cell.get_column_letter(int(col_choice)) if col_choice != "0" else None

        search_values = [str(value) for value in input("Please enter the values to search for, separated by commas: ").split(',')]
        highlight_rows(file_path, sheet_name, column_name, search_values)

    elif data_source == "2":
        print("Please paste the log data (Enter 'END' on a new line when done): ")
        log_data = []
        while True:
            line = input()
            if line.strip() == 'END':
                break
            log_data.append(line)
        data_frame = pd.DataFrame(log_data, columns=["Data"])

        search_type = input("Do you want to search for a value or an identifier? (1 for value, 2 for identifier) ")

        if search_type == "2":
            identifiers = input("Please enter the identifiers, separated by commas: ").split(',')
            extraction_type = input("Do you want to extract characters or words after the identifier? (1 for characters, 2 for words) ")
            num = int(input("How many characters/words after the identifier do you want to extract? "))

            if extraction_type == "1":
                data_frame['result'] = data_frame['Data'].apply(lambda x: [re.search(f"{identifier}(.{{0,{num}}})", str(x)).group(1) if re.search(f"{identifier}(.{{0,{num}}})", str(x)) else "No such result found" for identifier in identifiers])
            else:
                data_frame['result'] = data_frame['Data'].apply(lambda x: [re.search(f"{identifier}((?:\w+\s*){{0,{num}}})", str(x)).group(1) if re.search(f"{identifier}((?:\w+\s*){{0,{num}}})", str(x)) else "No such result found" for identifier in identifiers])
        else:
            search_values = [str(value) for value in input("Please enter the values to search for, separated by commas: ").split(',')]
            data_frame['result'] = data_frame['Data'].apply(lambda x: [value if value in str(x) else "No such result found" for value in search_values])

        print(data_frame['result'])

if __name__ == "__main__":
    main()
