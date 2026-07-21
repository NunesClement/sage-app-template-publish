FROM waggle/sage-thor-base:0.1.0

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir --requirement requirements.txt

COPY main.py .

ENTRYPOINT ["python3", "main.py"]
