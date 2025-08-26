
# Sakura Intern C - CSVファイルサーバ & SQL変換

## 概要

このプロジェクトは、CSVファイルのアップロード・ダウンロード機能と、アップロード時のSQL（INSERT文）自動変換機能を持つWebアプリケーションです。Flask（Python）を用い、MVCモデルに基づいて設計されています。

## 主な機能
- CSVファイルのアップロード（SQLファイル自動生成）
- CSVファイルのダウンロード
- 開発者モードによるSQL文の直接実行（SQLite）
- Bootstrapによるシンプルで見やすいUI

## ディレクトリ構成
```
├── app.py                # アプリのエントリポイント
├── controllers/          # コントローラ
│   └── main_controller.py
├── models/               # モデル
│   └── user_model.py
├── templates/            # テンプレート（HTML）
│   ├── index.html
│   └── message.html
├── uploads/              # アップロードファイル保存先
├── sqls/                 # SQLファイル・DB保存先
├── .gitignore
└── README.md
```

## セットアップ
1. Python 3.8以上 & venv推奨
2. 依存パッケージのインストール
	```bash
	pip install flask
	```
3. サーバ起動
	```bash
	python app.py
	```
4. ブラウザで `http://localhost:5000/` にアクセス

## 開発者モード
- 画面上部の「開発者モードON」ボタンで切り替え
- SQL文を直接入力・実行可能（SQLite）

## 注意
- `uploads/` や `sqls/` ディレクトリは自動生成されます
- `.gitignore` でpycや__pycache__は管理対象外

## ライセンス
MIT
