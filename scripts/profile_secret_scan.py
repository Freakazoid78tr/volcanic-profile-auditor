#!/usr/bin/env python3
"""Public profile distribution secret/private-state scanner."""
from pathlib import Path
import re
import sys

root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
forbidden_names = {
    '.env', '.env.local', '.env.production', 'auth.json',
    'state.db', 'state.db-shm', 'state.db-wal'
}
forbidden_dirs = {
    'memories', 'sessions', 'logs', 'workspace', 'home', 'cache',
    'image_cache', 'audio_cache', 'browser_screenshots', 'checkpoints',
    'local', 'sandboxes', 'wallets', 'keystores'
}
secret_patterns = [
    re.compile(r'ghp_[A-Za-z0-9_]{20,}'),
    re.compile(r'github_pat_[A-Za-z0-9_]{20,}'),
    re.compile(r'sk-[A-Za-z0-9_-]{20,}'),
    re.compile(r'(OPENAI|ANTHROPIC|OPENROUTER|GITHUB|GOOGLE|GEMINI|SERPAPI|FAL)_API_KEY\s*=\s*[^#\s].+', re.I),
    re.compile(r'(token|password|secret|private[_-]?key)\s*[:=]\s*[^#\s]{12,}', re.I),
    re.compile(r'-----BEGIN (RSA |EC |OPENSSH |)?PRIVATE KEY-----'),
]
problems = []
for p in root.rglob('*'):
    rel = p.relative_to(root)
    if '.git' in rel.parts:
        continue
    if p.name in forbidden_names:
        problems.append(f'forbidden file: {rel}')
    if p.is_dir() and p.name in forbidden_dirs:
        problems.append(f'forbidden directory: {rel}')
        continue
    if p.is_file():
        try:
            text = p.read_text(errors='ignore')
        except Exception:
            continue
        for pat in secret_patterns:
            if pat.search(text):
                # Allow empty placeholder lines in env examples.
                if p.name.lower() in {'.env.example', '.env.example', '.env_example', '.env-example', '.env.example'}:
                    continue
                problems.append(f'possible secret pattern in: {rel}')
                break
if problems:
    print('Secret/private-state scan failed:')
    for item in problems:
        print(' -', item)
    sys.exit(1)
print(f'Secret/private-state scan passed: {root}')
