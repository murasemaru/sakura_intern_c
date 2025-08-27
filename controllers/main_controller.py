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

import re
import sqlite3

def safe_filename(filename):
    # 半角英数字とアンダースコアのみ許可
    name, _ = os.path.splitext(filename)
    return re.sub(r'[^A-Za-z0-9_]', '_', name)

def upload_controller():
    file = request.files['file']
    if file and file.filename.endswith('.csv'):
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        # SQLiteファイル名をCSV名に対応
        db_name = safe_filename(file.filename) + '.sqlite3'
        db_path = os.path.join(SQL_FOLDER, db_name)
        # テーブル名も安全化
        table_name = safe_filename(file.filename)
        with open(filepath, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            columns = next(reader)
            # SQLite DB作成・テーブル作成
            conn = sqlite3.connect(db_path)
            try:
                cur = conn.cursor()
                col_defs = ', '.join([f'{c} TEXT' for c in columns])
                cur.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({col_defs})')
                for row in reader:
                    values = []
                    for v in row:
                        if v == '':
                            values.append(None)
                        else:
                            values.append(v)
                    col_names = ', '.join(columns)
                    placeholders = ', '.join(['?' for _ in columns])
                    cur.execute(f'INSERT INTO {table_name} ({col_names}) VALUES ({placeholders})', values)
                conn.commit()
            finally:
                conn.close()
        return render_template('message.html', message=f'アップロード＆SQLite変換完了！<br>DBファイル名: {db_name}')
    return render_template('message.html', message='CSVファイルを選択してください。')

def download_controller(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
