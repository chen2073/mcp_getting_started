FROM ghcr.io/astral-sh/uv:debian-slim

RUN apt-get update && apt-get install -y \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN uv sync

CMD ["npx", "-y", "@modelcontextprotocol/inspector", "uv", "run web_search.py"]