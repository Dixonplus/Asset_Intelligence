"""Non-destructive schema synchronization for the AB Afric application.

SQLAlchemy's db.create_all() creates missing tables but does not add columns to
existing tables. This module adds any columns present in the Python models but
missing from the existing MySQL tables. Missing columns are initially added as
NULL so existing production/development rows are never invalidated; the Python
model defaults continue to apply to new records.
"""

from sqlalchemy import inspect, text


def synchronize_schema(db):
    """Add model columns missing from existing tables without dropping data."""
    inspector = inspect(db.engine)
    existing_tables = set(inspector.get_table_names())
    added = []

    for table in db.metadata.sorted_tables:
        if table.name not in existing_tables:
            continue

        existing_columns = {c["name"] for c in inspector.get_columns(table.name)}

        for column in table.columns:
            if column.name in existing_columns:
                continue

            # Compile the SQLAlchemy type using the active database dialect.
            type_sql = column.type.compile(dialect=db.engine.dialect)
            sql = (
                f"ALTER TABLE `{table.name}` "
                f"ADD COLUMN `{column.name}` {type_sql} NULL"
            )
            db.session.execute(text(sql))
            added.append(f"{table.name}.{column.name}")

    if added:
        db.session.commit()

    return added
