from flask import Flask
from controllers.main_controller import index_controller, upload_controller, download_controller, sql_execute_controller
import os

app = Flask(__name__)

@app.route('/')
def index():
    return index_controller()

@app.route('/upload', methods=['POST'])
def upload():
    return upload_controller()

@app.route('/download/<filename>')
def download(filename):
    return download_controller(filename)

@app.route('/dev/sql', methods=['POST'])
def dev_sql():
    return sql_execute_controller()

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('sqls', exist_ok=True)
    app.run(debug=True)
