import logging, argparse, sys, os
import csv
import re


# python csv_to_sql_file.py -file file.csv -table sql_table -output output.sql -headers -auto_type -date_format
# varchar	integer	float	date	bool

DEFAULT_DATE_FORMAT = "DD/MM/YYYY"


def csv_to_file(csv_file, table, output_file, headers, auto_type, date_format):
    print(csv_file, table, output_file, headers, auto_type, date_format)


def main():
    args = set_argparse()

    CSV_FILE = args.file
    TABLE = args.table
    OUTPUT_FILE = args.output
    HEADERS = args.headers
    AUTO_TYPE = args.auto_type
    DATE_FORMAT = args.date_format

    logging.info('CSV file : %s', CSV_FILE)
    logging.info('Table : %s', TABLE)
    logging.info('Output file : %s', OUTPUT_FILE)
    logging.info('Headers : %s', HEADERS)
    logging.info('Auto type : %s', AUTO_TYPE)
    logging.info('Date Format : %s', DATE_FORMAT)

    csv_to_file(CSV_FILE, TABLE, OUTPUT_FILE, HEADERS, AUTO_TYPE, DATE_FORMAT)
    exit(0)


def set_argparse():
    parser = argparse.ArgumentParser(description='')
    parser.action_groups.pop()
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')
    required.add_argument('-f', '--file', help=' (default: None)', default=None, required=True)

    optional.add_argument('-t', '--table', help=' (default: filename)', default=None)
    optional.add_argument('-o', '--output', help=' (default: output.sql)', default='output.sql')
    optional.add_argument('-h', '--headers', help=' (default: True)', default=True)
    optional.add_argument('-at', '--auto_type', help=' (default: True)', default=True)
    optional.add_argument('-df', '--date_format', help=f' (default: {DEFAULT_DATE_FORMAT})',
                          default=DEFAULT_DATE_FORMAT)

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


if __name__ == '__main__':
    main()
