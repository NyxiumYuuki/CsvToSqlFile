import argparse
import csv
import logging
import re
import sys
import os


# varchar integer float date bool

DEFAULT_CSV_FILE = None
DEFAULT_DELIMITER = ';'
DEFAULT_TABLE = None
DEFAULT_OUTPUT_FILE = 'output.sql'
DEFAULT_HEADERS = True
DEFAULT_DATE_FORMAT = 'DD/MM/YYYY'
DEFAULT_DATE_PATTERN = 'r(\d+/\d+/\d+)'


def main():

    args = set_argparse()
    csv_to_file(
        args.file,
        args.delimiter,
        args.table,
        args.output,
        args.headers,
        args.date_format,
        args.date_pattern
    )

    exit(0)


def set_argparse():
    parser = argparse.ArgumentParser(description='Data from CSV file to SQL INSERT INTO table')
    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')
    required.add_argument('-f', '--file', help=f' (default: {DEFAULT_CSV_FILE})', default=DEFAULT_CSV_FILE, required=True)

    optional.add_argument('-del', '--delimiter', help=f'Csv file to transform (default: {DEFAULT_DELIMITER})', default=DEFAULT_DELIMITER)
    optional.add_argument('-t', '--table', help=f'Table (default: filename)', default=DEFAULT_TABLE)
    optional.add_argument('-o', '--output', help=f'Output file (default: {DEFAULT_OUTPUT_FILE})', default=DEFAULT_OUTPUT_FILE)
    optional.add_argument('-head', '--headers', help=f'Headers in csv file (default: {DEFAULT_HEADERS})', default=DEFAULT_HEADERS)
    optional.add_argument('-df', '--date_format', help=f'Date format to consider (default: {DEFAULT_DATE_FORMAT})',
                          default=DEFAULT_DATE_FORMAT)
    optional.add_argument('-dp', '--date_pattern', help=f'Date pattern to recognize (default: {DEFAULT_DATE_PATTERN})',
                          default=DEFAULT_DATE_PATTERN)

    optional.add_argument('-i', '--info', help='Info mode (default: True)', default=True, action='store_false')
    optional.add_argument('-d', '--debug', help='Debug mode (default: False)', default=False, action='store_true')

    try:
        args = parser.parse_args()
    except argparse.ArgumentError as error:
        logging.error('Catching an argumentError {}'.format(error))
        sys.exit('Catching an argumentError {}'.format(error))

    if args.debug:
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    elif args.info:
        logging.basicConfig(stream=sys.stderr, level=logging.INFO)
    else:
        logging.basicConfig(stream=sys.stderr, level=logging.ERROR)

    return args


def csv_to_file(csv_file, delimiter, table, output_file, headers, date_format, date_pattern):
    if table is None:
        table = os.path.basename(csv_file).split('.')[0]

    logging.info('CSV file : %s', csv_file)
    logging.info('Delimiter : %s', delimiter)
    logging.info('Table : %s', table)
    logging.info('Output file : %s', output_file)
    logging.info('Headers : %s', headers)
    logging.info('Date Format : %s', date_format)
    logging.info('Date Pattern : %s', date_pattern)

    openFile = open(csv_file, 'r')
    csvFile = csv.reader(openFile, delimiter=delimiter)

    if headers:
        headersRow = next(csvFile)
        logging.info('Headers : %s', headersRow)

    insert = f'INSERT INTO {table}\n VALUES '
    with open(output_file, 'w') as outputFile:
        valuesString = ""
        for row in csvFile:
            values = []
            for value in map((lambda x: x), row):
                if value == "":
                    values.append("NULL")
                elif re.search(date_pattern, value):
                    values.append(f"TO_DATE('{value}','{date_format}')")
                elif value.isnumeric() or value.isdecimal() or value.isdigit():
                    values.append(value)
                elif value.lower() in ['true', 'false', 'True', 'False', 'TRUE', 'FALSE']:
                    values.append(value.capitalize())
                else:
                    values.append(f"'{value}'")
                print(re.search(date_pattern, value))
            valuesString += f"({','.join(values)}),\n"

        print(valuesString)
        valuesString = insert + valuesString[0:-2] + ";"
        outputFile.writelines(valuesString)
        outputFile.close()
    openFile.close()


if __name__ == '__main__':
    main()
