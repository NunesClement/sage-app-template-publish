FROM waggle/plugin-base:1.1.1-ml

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir --requirement requirements.txt

COPY main.py .

ENTRYPOINT ["python3", "main.py"]
