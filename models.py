from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy.sql import func
from database import metadata  # Absoluter Import

# Tabelle für Notizen
notes = Table(
    'notes',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String(100)),
    Column('content', String(500)),
    Column('created_at', String, default=func.now())
)