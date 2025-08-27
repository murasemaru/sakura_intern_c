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


from openpyxl import load_workbook

def upload_controller():
    file = request.files['file']
    if not file:
        return render_template('message.html', message='ファイルを選択してください。')

    filename = file.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    db_name = safe_filename(filename) + '.sqlite3'
    db_path = os.path.join(SQL_FOLDER, db_name)

    if filename.endswith('.csv'):
        table_name = safe_filename(filename)
        with open(filepath, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            columns = next(reader)
            conn = sqlite3.connect(db_path)
            try:
                cur = conn.cursor()
                col_defs = ', '.join([f'{c} TEXT' for c in columns])
                cur.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({col_defs})')
                for row in reader:
                    values = [v if v != '' else None for v in row]
                    col_names = ', '.join(columns)
                    placeholders = ', '.join(['?' for _ in columns])
                    cur.execute(f'INSERT INTO {table_name} ({col_names}) VALUES ({placeholders})', values)
                conn.commit()
            finally:
                conn.close()
        return render_template('message.html', message=f'アップロード＆SQLite変換完了！<br>DBファイル名: {db_name}')

    elif filename.endswith('.xlsx'):
        wb = load_workbook(filepath, data_only=True)
        conn = sqlite3.connect(db_path)
        try:
            cur = conn.cursor()
            for sheet in wb.sheetnames:
                ws = wb[sheet]
                rows = list(ws.iter_rows(values_only=True))
                if not rows or not rows[0]:
                    continue
                columns = [str(c) for c in rows[0]]
                table_name = f"{safe_filename(filename)}_{safe_filename(sheet)}"
                col_defs = ', '.join([f'{c} TEXT' for c in columns])
                cur.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({col_defs})')
                for row in rows[1:]:
                    values = [v if v is not None and v != '' else None for v in row]
                    col_names = ', '.join(columns)
                    placeholders = ', '.join(['?' for _ in columns])
                    cur.execute(f'INSERT INTO {table_name} ({col_names}) VALUES ({placeholders})', values)
            conn.commit()
        finally:
            conn.close()
        return render_template('message.html', message=f'アップロード＆SQLite変換完了！<br>DBファイル名: {db_name}')

    else:
        return render_template('message.html', message='CSVまたはXLSXファイルのみ対応しています。')

def download_controller(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
