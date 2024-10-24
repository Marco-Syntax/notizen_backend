from sqlalchemy import create_engine, MetaData
from databases import Database

# SQLite Datenbankpfad
DATABASE_URL = "sqlite:///./notizen.db"

# Initialisierung der Datenbank
database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)

# MetaData für die Tabellen
metadata = MetaData()