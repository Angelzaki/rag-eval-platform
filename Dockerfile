FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src
COPY samples ./samples
COPY scripts ./scripts
COPY tests ./tests

RUN pip install --no-cache-dir -e . \
 && mkdir -p results

ENTRYPOINT ["python", "-m", "rag_eval"]
CMD ["--scenario", "scenario_a"]
