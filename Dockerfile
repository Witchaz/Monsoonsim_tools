FROM python:3.12-slim
SHELL ["/bin/bash", "-c"]

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/Witchaz/Monsoonsim_tools.git .

# Log installation process
RUN for pkg in $(cat requirements.txt); do \
    echo "Installing $pkg"; \
    if [[ "$pkg" != *"windows"* ]]; then \
    pip install "$pkg" || true; \
    else \
    echo "Skipping $pkg"; \
    fi; \
    done

RUN pip install streamlit
EXPOSE 8501

# Check contents of the app directory
RUN ls -la /app

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Test the ENTRYPOINT command
ENTRYPOINT ["streamlit", "run", "Home.py", "--server.port=8501", "--server.address=0.0.0.0"]
