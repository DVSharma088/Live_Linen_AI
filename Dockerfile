# ====================================================
# 🐍 Base Image (Python 3.12, slim)
# ====================================================
FROM python:3.12-slim

# ====================================================
# 🧱 System dependencies (required for CV)
# ====================================================
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# ====================================================
# 📂 Set working directory
# ====================================================
WORKDIR /app

# ====================================================
# 📦 Copy requirements first (Docker cache)
# ====================================================
COPY requirements.txt .

# ====================================================
# 📦 Install Python dependencies (CPU PyTorch)
# ====================================================
RUN pip install --upgrade pip && \
    pip install -r requirements.txt \
    --extra-index-url https://download.pytorch.org/whl/cpu

# ====================================================
# 📁 Copy full project
# ====================================================
COPY . .

# ====================================================
# 🌐 Expose Flask port
# ====================================================
EXPOSE 5000

# ====================================================
# 🚀 Run the app
# ====================================================
CMD ["python", "app.py"]
