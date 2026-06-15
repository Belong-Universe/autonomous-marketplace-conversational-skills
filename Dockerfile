FROM python:3.12-slim

WORKDIR /site

COPY index.html styles.css script.js agent-manifest.json AGENT_HANDOFF.md README.md llms.txt llms-full.txt ./
COPY assets ./assets
COPY scripts ./scripts

ENV PORT=8080

CMD ["sh", "-c", "python3 -m http.server \"${PORT}\" --bind 0.0.0.0"]
