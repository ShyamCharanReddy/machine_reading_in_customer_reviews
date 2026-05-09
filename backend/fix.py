import os

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    if '\\"' in content:
        print(f"Fixing {filepath}")
        content = content.replace('\\"', '"')
        with open(filepath, 'w') as f:
            f.write(content)

for root, dirs, files in os.walk('.'):
    if 'venv' in root:
        continue
    for f in files:
        if f.endswith('.py') or f.endswith('.jsx') or f.endswith('.js'):
            fix_file(os.path.join(root, f))
