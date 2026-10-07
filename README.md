# AB Afric Infrastructure Asset Intelligence Platform

A single Flask + MySQL enterprise platform connecting asset records, maintenance/service operations, technical data, GIS context, vendors, parts, consumables, preventive maintenance, service history, cost/labour data, failure predictions and strategic CAPEX decisions.

## Canonical flow

**Home → Sign up / Log in → Dashboard → Asset Register / Maintenance & Services / Intelligence → Strategic Intelligence & CAPEX**

Pages **1–17 are retained as one coherent module set**. Shared navigation is implemented once in `app/templates/base.html`.

## Technology

- Python / Flask
- Flask-SQLAlchemy + PyMySQL
- MySQL database: `asset_intelligence`
- HTML / CSS / JavaScript
- QR generation with `qrcode`

## Important database synchronization fix

This version fixes the `/parts` failure caused by the Python `Part` model expecting `part.reorder_level` while an older MySQL table did not contain that column.

`db.create_all()` alone cannot update existing tables. The application now runs a **non-destructive schema synchronizer** during startup. It adds model columns missing from existing tables without dropping existing records.

For an existing database, you can also run:

```bash
python database_sync.py
```

For the immediate known `/parts` issue, `database_migrate.sql` contains a safe conditional migration for `part.reorder_level`.

## Run locally

1. Start MySQL in XAMPP.
2. Make sure the database `asset_intelligence` exists. For a new database, import `database_init.sql` in phpMyAdmin.
3. Copy `.env.example` to `.env` and set your MySQL credentials.
4. Activate the virtual environment and install dependencies:

```bash
source .venv/Scripts/activate
pip install -r requirements.txt
```

5. Synchronize an existing database:

```bash
python database_sync.py
```

6. Start Flask:

```bash
python run.py
```

7. Open `http://127.0.0.1:5000`.

## Development administrator

- Email: `admin@abafric.local`
- Password: `Admin@12345`

Change the development password before any real deployment.

## Database reset warning

`database_reset.sql` is destructive. Back up existing data before importing it. Use it only when you intentionally want a clean development database; start the Flask application afterward so SQLAlchemy creates the current tables and the schema synchronizer verifies them.

## Validation

The archive is prepared so the existing application schema is reconciled non-destructively at startup. The supplied project was not connected to the user's live XAMPP/MySQL instance from this environment, so live production-data verification must still be performed on the user's machine.
