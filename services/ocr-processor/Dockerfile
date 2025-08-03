# Pythonの公式イメージをベースにする
FROM python:3.9-slim

# デバッグツールをインストール
RUN apt-get update && apt-get install -y curl

# 作業ディレクトリを設定
WORKDIR /code

# 依存関係をrequirements.txtからインストール
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# アプリケーションのコードをコピー
COPY ./app /code/app

# uvicornを起動してアプリケーションを実行
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
