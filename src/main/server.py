from flask import Flask, request, send_from_directory, render_template_string
import os
import csv
import pathlib as Path

UPLOAD_FOLDER = 'uploads'
SQL_FOLDER = 'sqls'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(SQL_FOLDER, exist_ok=True)

app = Flask(__name__)

HTML = '''
<!doctype html>
<title>CSV File Server</title>
<h1>CSV File Server</h1>
<button onclick="location.href='/?dev={{ '1' if not dev else '' }}'">{{ '開発者モードON' if not dev else '開発者モードOFF' }}</button>
<h2>アップロード</h2>
<form method=post enctype=multipart/form-data action="/upload">
    <input type=file name=file>
    <input type=text name=table placeholder="テーブル名">
    <input type=submit value=Upload>
</form>
<h2>ダウンロード</h2>
<ul>
{% for f in files %}
    <li><a href="/download/{{f}}">{{f}}</a></li>
{% endfor %}
</ul>
{% if dev %}
<hr>
<h2>開発者モード: SQL実行</h2>
<form method=post action="/dev/sql">
    <textarea name=sql rows=4 cols=60 placeholder="SQL文を入力"></textarea><br>
    <input type=submit value="SQL実行">
</form>
{% if sql_result is defined %}
<h3>実行結果</h3>
<pre>{{ sql_result }}</pre>
{% endif %}
{% endif %}
'''

@app.route('/')
def init():
    # データベース初期化（仮：usersテーブルを作成）
    import sqlite3
    db_path = os.path.join(SQL_FOLDER, 'dev.sqlite3')
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY,
                content TEXT
            )
        """)
        conn.commit()
    finally:
        conn.close()
    files = os.listdir(UPLOAD_FOLDER)
    dev = request.args.get('dev') == '1'
    return render_template_string(HTML, files=files, dev=dev)
import sqlite3

# 開発者モード: SQL実行
@app.route('/dev/sql', methods=['POST'])
def dev_sql():
    print("開発者モード: SQL実行")
    dev = True
    sql = request.form.get('sql', '')
    result = ''
    db_path = os.path.join(SQL_FOLDER, 'dev.sqlite3')
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        cur.execute('PRAGMA foreign_keys=ON;')
        cur.executescript(sql)
        if cur.description:
            rows = cur.fetchall()
            columns = [d[0] for d in cur.description]
            result = '\t'.join(columns) + '\n' + '\n'.join(['\t'.join(map(str, r)) for r in rows])
        else:
            result = 'SQL実行成功'
        conn.commit()
    except Exception as e:
        result = f'エラー: {e}'
    finally:
        conn.close()
    files = os.listdir(UPLOAD_FOLDER)
    return render_template_string(HTML, files=files, dev=dev, sql_result=result)

@app.route('/upload', methods=['POST'])
def upload():
    print("ファイルアップロード")
    file = request.files['file']
    table = request.form.get('table', 'my_table')
    if file and file.filename.endswith('.csv'):
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        # SQL変換
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
                print(sql)
                # out.write(sql)
        return 'アップロード＆SQL変換完了！<br><a href="/">戻る</a>'
    return 'CSVファイルを選択してください。<br><a href="/">戻る</a>'

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
