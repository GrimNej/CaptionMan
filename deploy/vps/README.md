# CaptionMan VPS Demo Deploy

This folder contains non-secret deployment templates for the public demo at
`captionman.grimnej.com`.

Secrets are not stored here. The server reads runtime credentials from:

```text
/opt/captionman/secrets/api.env
```

The demo runs as three containers:

- `api`: source-built API image, launched as the FastAPI demo server with runtime-only credentials.
- `web`: production Next.js Studio build.
- `caddy`: reverse proxy for `/api/*` and the frontend.

The DNS record for the domain must point to the VPS public IP:

```text
captionman.grimnej.com A 193.122.147.68
```
