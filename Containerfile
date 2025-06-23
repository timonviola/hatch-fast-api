FROM python:3.11 AS python_with_hatch
ARG \
  UV_VERSION=0.7.13

ENV PYTHONUNBUFFERED=1

RUN python -m pip install --no-cache-dir "uv==$UV_VERSION"

FROM python_with_hatch AS dependencies
COPY . /app/
WORKDIR /app/
RUN uv pip install --system -r pyproject.toml
EXPOSE 8000
CMD ["python", "-m", "fastapi", "run", "--workers", "1","--port", "8000", "src/fibonacci_api/main.py"]
