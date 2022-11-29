import sys
import csv


# Add better error handling for weirder scenarios
# Maybe expand to parse most census data, not just ours

def main():
    if len(sys.argv) == 1:
        print("Missing Arguments. Try censusParser.py -print_help")
        return
    if "-print_help" in sys.argv or "-h" in sys.argv or "-H" in sys.argv:
        print_help()
        return
    if "-keep" in sys.argv or "-k" in sys.argv or "-K" in sys.argv:
        keep = 1
    else:
        keep = 0
    try:
        raw_file = open(sys.argv[1])
        kept_categories = preprocess(raw_file)
        raw_file.close()
        raw_file = open(sys.argv[1])
        start_parsing(raw_file, kept_categories, keep)
        raw_file.close()
    except:
        print("Invalid file name argument. Try censusParser.py -print_help")
        return


def start_parsing(raw, indexed_keys, keep):
    ignored_columns = set()
    csv_reader = csv.reader(raw, delimiter=",")
    csv_reader.__next__()
    line = csv_reader.__next__()
    count = 0
    new_file = open("output/outputFile.csv", "w", newline='')
    new_file_writer = csv.writer(new_file)
    saved_columns = []
    for column in line:
        tokenized = column.split(sep="!!")
        for category in tokenized:
            if category not in indexed_keys:
                ignored_columns.add(count)
                break
        if count not in ignored_columns:
            fixed_column_name = ""
            for token in tokenized:
                fixed_column_name += token + " | "
            saved_columns.append(fixed_column_name[:-3])
        count += 1
    null_columns = []
    output_data = []
    for row in csv_reader:
        count = 0
        cleaned_row = []
        for cell in row:
            if count not in ignored_columns and cell != "null":
                cleaned_row.append(cell.strip('''"'''))
            if cell == "null":
                null_columns.append(count)
            count += 1
        output_data.append(cleaned_row)
    output_columns = []
    for column in saved_columns:
        if saved_columns.index(column) not in null_columns:
            output_columns.append(column)
    new_file_writer.writerow(output_columns)
    new_file_writer.writerows(output_data)
    new_file.close()


def preprocess(raw):
    cat_levels = {}
    csv_reader = csv.reader(raw, delimiter=",")
    csv_reader.__next__()
    line = csv_reader.__next__()
    for column in line:
        tokenized = column.split(sep="!!")
        level = 0
        for category in tokenized:
            cat_levels[category] = level
            level += 1
    indexed_categories = print_categories(cat_levels)
    removed_categories = input(
        "\nFrom the list above select all the values you want removed separated by spaces\nExample: 00 01 20 30\n")
    removed_categories = removed_categories.split(sep=" ")
    for index in removed_categories:
        try:
            index = int(index)
            indexed_categories.pop(list(indexed_categories.keys())[list(indexed_categories.values()).index(index)])
        except:
            # Bug here to recheck input
            print("Please type only numbers, try again")
            removed_categories = input(
                "\nFrom the list above select all the values you want removed separated by spaces\nExample: 00 01 20 "
                "30\n")
            removed_categories = removed_categories.split(sep=" ")
    category_keys = []
    for item in indexed_categories:
        category_keys.append(item)
    return category_keys


def print_categories(categories):
    highest_cat = 0
    indexed_categories = {}
    for cat in categories:
        if categories[cat] > highest_cat:
            highest_cat = categories[cat]
    count = 0
    while count < highest_cat:
        print(f"Level {count}".center(25, "-"))
        inner_count = 0
        for cat in categories:
            if categories[cat] == count:
                print("\t" + cat + f" [{count}{inner_count}]")
                indexed_categories[cat] = (count * 10) + inner_count
                inner_count += 1
        count += 1
    # Maybe add an index to a general level, so instead of typing N items, typing 1 index per entire level
    return indexed_categories


def print_help():
    # more print_help later
    print("Usage: censusParser.py fileName [-print_help] [-keep]")
    print("\t-print_help\t-Print out this message.")
    print("\t-keep\t-Keep all null value columns.\n\t\t (Default: Remove any columns containing only null)")


if __name__ == '__main__':
    main()
