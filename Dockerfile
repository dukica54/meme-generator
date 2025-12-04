# Uporabi uradno Python sliko kot osnovo
FROM python:3.12-slim

# Nastavi delovni direktorij v kontejnerju
WORKDIR /app

# Instaliraj sistemske odvisnosti za Pillow in fonte
RUN apt-get update && apt-get install -y \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

# Kopiraj requirements.txt in instaliraj Python odvisnosti
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiraj vse datoteke projekta v kontejner
COPY . .

# Ustvari potrebne direktorije
RUN mkdir -p static/uploads fonts

# Nastavi okoljsko spremenljivko za port
ENV PORT=5000

# Odpri port 5000
EXPOSE 5000

# Zaženi aplikacijo
CMD ["python", "app.py"]