FROM python:3.9-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install --yes --no-install-recommends \
    gcc \
    g++ \
    build-essential \
    python3-dev \
    vim

# ライブラリのインストール
RUN pip install --upgrade pip
RUN pip install streamlit pandas

# ソースのコピー
COPY app/ /app/

# コマンド実行
# 静的ファイルの使用するにはenableStaticServingオプションを有効にする
CMD ["streamlit", "run", "--server.port", "8501", "--server.enableStaticServing", "true", "/app/Home.py"]