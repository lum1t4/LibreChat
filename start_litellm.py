"""Normalize a Dokploy one-line OCI signing key before starting LiteLLM."""
import base64
import os
import re

key = os.environ.get('OCI_KEY', '').replace('\\n', '\n').strip()
header = '-----BEGIN PRIVATE KEY-----'
footer = '-----END PRIVATE KEY-----'
if not key.startswith(header) or not key.endswith(footer):
    raise SystemExit('OCI_KEY must contain a PEM private key')
body = re.sub(r'\s+', '', key[len(header):-len(footer)])
try:
    base64.b64decode(body, validate=True)
except ValueError as exc:
    raise SystemExit('OCI_KEY has invalid PEM base64') from exc
os.environ['OCI_KEY'] = '\n'.join([header, *(body[i:i + 64] for i in range(0, len(body), 64)), footer, ''])
os.execvp('litellm', ['litellm', '--config', '/app/config.yaml', '--port', '4000'])
