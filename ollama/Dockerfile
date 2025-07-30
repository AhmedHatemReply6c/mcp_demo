FROM ollama/ollama:0.9.6

COPY models.txt entrypoint.sh readiness_check.sh /
RUN chmod +x /entrypoint.sh /readiness_check.sh

ENTRYPOINT ["/entrypoint.sh"]
