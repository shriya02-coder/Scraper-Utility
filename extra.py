def process_log_data():
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

        def find_all_matches(text, identifier, num_chars):
            pattern = f"{identifier}(.{{0,{num_chars}}})" if extraction_type == "1" else f"{identifier}((?:\\w+\\s*){{0,{num_chars}}})"
            return [match.group(1) for match in re.finditer(pattern, text)]

        data_frame['result'] = data_frame['Data'].apply(lambda x: {identifier: find_all_matches(x, identifier, num) for identifier in identifiers})
    else:
        search_values = [str(value) for value in input("Please enter the values to search for, separated by commas: ").split(',')]
        data_frame['result'] = data_frame['Data'].apply(lambda x: [value if value in str(x) else "No such result found" for value in search_values])

    print(data_frame['result'])

# The rest of the script remains unchanged