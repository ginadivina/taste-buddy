from app import app
from app.database import create_connection
db_file = "db.db"

create_connection(db_file)