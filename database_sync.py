"""Run the non-destructive AB Afric database schema synchronization.

Use this when an existing asset_intelligence database was created by an older
version of the project. It adds missing model columns without dropping data.
"""

from app import create_app
from app import db
from app.schema_sync import synchronize_schema

app = create_app()

with app.app_context():
    added = synchronize_schema(db)
    if added:
        print("Added missing columns:")
        for item in added:
            print(f"  - {item}")
    else:
        print("Database schema is already synchronized with the current models.")
