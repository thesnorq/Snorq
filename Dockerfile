FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml ./
COPY snorq/ ./snorq/
RUN pip install --no-cache-dir -e .
COPY tests/ ./tests/
CMD ["python", "-m", "pytest", "tests/", "-v"]
