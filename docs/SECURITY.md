# Security

CaptionMan avoids storing secrets in repository files, redacts sensitive values from logs, blocks obvious private-network downloads, and writes official results atomically.

Do not log:

- API keys
- Authorization headers
- signed URLs
- full base64 images
- provider response headers
- stack traces in official output
