FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
        git curl && \
    rm -rf /var/lib/apt/lists/*

COPY server.py requirements.txt llms-small.txt mcp_documentation.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

WORKDIR /app
EXPOSE 8000
ENTRYPOINT ["python", "server.py"]
