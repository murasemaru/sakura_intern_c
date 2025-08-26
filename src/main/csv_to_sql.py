import csv
import sys

if len(sys.argv) != 3:
    print(f"Usage: python {sys.argv[0]} <csv_file> <table_name>")
    sys.exit(1)

csv_file = sys.argv[1]
table_name = sys.argv[2]

with open(csv_file, newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    columns = next(reader)
    for row in reader:
        values = []
        for v in row:
            if v == '':
                values.append('NULL')
            else:
                values.append(f"'{v.replace("'", "''")}" )
        sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(values)});"
        print(sql)
