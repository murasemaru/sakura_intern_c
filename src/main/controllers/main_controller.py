from flask import render_template, request, send_from_directory
import os
import csv
from models.user_model import UserModel

UPLOAD_FOLDER = 'uploads'
SQL_FOLDER = 'sqls'


def index_controller():
    UserModel.init_db()
    files = os.listdir(UPLOAD_FOLDER)
    dev = request.args.get('dev') == '1'
    return render_template('index.html', files=files, dev=dev)

def upload_controller():
    file = request.files['file']
    table = request.form.get('table', 'my_table')
    if file and file.filename.endswith('.csv'):
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        sqlpath = os.path.join(SQL_FOLDER, file.filename + '.sql')
        with open(filepath, newline='', encoding='utf-8') as f, open(sqlpath, 'w', encoding='utf-8') as out:
            reader = csv.reader(f)
            columns = next(reader)
            for row in reader:
                values = []
                for v in row:
                    if v == '':
                        values.append('NULL')
                    else:
                        safe_v = v.replace("'", "''")
                        values.append(f"'{safe_v}'")
                sql = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(values)});\n"
                out.write(sql)
        return render_template('message.html', message='アップロード＆SQL変換完了！')
    return render_template('message.html', message='CSVファイルを選択してください。')

def download_controller(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
