FROM python:3.12

# Expose port you want your app on
EXPOSE 8080

# Upgrade pip and install requirements
COPY requirements.txt requirements.txt
RUN for pkg in $(cat requirements.txt); do \
    pip install "$pkg" || true; \
    done

RUN pip install streamlit
# Copy app code and set working directory
COPY . .
WORKDIR /app

# Run
ENTRYPOINT [“streamlit”, “run”, “Home.py”]