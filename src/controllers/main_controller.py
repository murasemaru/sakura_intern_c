from flask import render_template_string, request, send_from_directory
import os
import csv
from models.user_model import UserModel

UPLOAD_FOLDER = 'uploads'
SQL_FOLDER = 'sqls'

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

def index_controller():
    UserModel.init_db()
    files = os.listdir(UPLOAD_FOLDER)
    dev = request.args.get('dev') == '1'
    return render_template_string(HTML, files=files, dev=dev)

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
        return 'アップロード＆SQL変換完了！<br><a href="/">戻る</a>'
    return 'CSVファイルを選択してください。<br><a href="/">戻る</a>'

def download_controller(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
