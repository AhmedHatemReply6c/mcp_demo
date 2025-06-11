FROM ollama/ollama:latest

COPY entrypoint.sh /entrypoint.sh
COPY models.txt   /models.txt
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
