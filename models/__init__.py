from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()
engine = create_engine("sqlite:///database.db")
