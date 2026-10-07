from pathlib import Path
import ast
ROOT = Path(__file__).resolve().parent
errors=[]
for path in [ROOT/'run.py',ROOT/'config.py',ROOT/'database_sync.py',ROOT/'app/__init__.py',ROOT/'app/schema_sync.py',ROOT/'app/models.py',ROOT/'app/routes.py',ROOT/'app/seed.py']:
    try: ast.parse(path.read_text(encoding='utf-8'))
    except Exception as exc: errors.append(f'{path}: {exc}')
for item in ['run.py','config.py','requirements.txt','database_init.sql','database_migrate.sql','database_sync.py','app/__init__.py','app/schema_sync.py','app/models.py','app/routes.py','app/seed.py','app/templates/base.html']:
    if not (ROOT/item).exists(): errors.append(f'Missing: {item}')
if errors:
    print('FAILED'); print('\n'.join(errors)); raise SystemExit(1)
print('PROJECT VALIDATION PASSED')
