

# Excelクラウドシンク

## 目的

ユーザーが持つExcelファイルのデータをクラウド上のDBに保存する。

## 対象範囲

- csvファイルからのデータ抽出
- クラウドDB（MySQL互換）への保存

## 機能要件

1. **Excelファイル入力機能**
	- ユーザーがファイルをアップロードできること
	- 対応形式: .xlsx / .xls / .csv

2. **データ抽出・変換機能**
	- Excelのセルデータを行列形式で抽出

3. **クラウドDB保存機能**
	- 抽出データをINSERT文としてクラウドDBに保存

## セットアップ
1. Python 3.8以上 & venv推奨
2. 依存パッケージのインストール
   ```bash
   pip install flask openpyxl
   ```
3. サーバ起動
   ```bash
   python app.py
   ```
4. ブラウザで `http://localhost:5000/` にアクセス

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

## 注意
- `uploads/` や `sqls/` ディレクトリは自動生成されます
- `.gitignore` でpycや__pycache__は管理対象外

## ライセンス
MIT
