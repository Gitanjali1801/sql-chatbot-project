from fastapi import FastAPI
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from llama_index.llms.groq import Groq
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings, SQLDatabase
from llama_index.core.query_engine import NLSQLTableQueryEngine

# ✅ Load environment variables
load_dotenv()
api_key = os.getenv("groqApi")

# ✅ Set embedding model (HuggingFace)
embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
Settings.embed_model = embed_model

import sqlite3

conn = sqlite3.connect("customer_data.sqlite")
cursor = conn.cursor()

# Create the table
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    gender TEXT,
    location TEXT
)
""")

# Insert sample data
cursor.executemany("""
INSERT INTO customers (name, gender, location)
VALUES (?, ?, ?)
""", [
    ("Aarav Mehta", "Male", "Mumbai"),
    ("Isha Banerjee", "Female", "Kolkata"),
    ("Neha Sharma", "Female", "Delhi"),
    ("Ravi Patel", "Male", "Ahmedabad"),
    ("Priya Reddy", "Female", "Hyderabad")
])

conn.commit()
conn.close()


# ✅ Database connection
# engine = create_engine("sqlite:///european_database.sqlite")
# engine = create_engine("sqlite:///european_teams.sqlite")
# Change the engine line:
# engine = create_engine("sqlite:///european_teams.sqlite")
# Replace old DB line
engine = create_engine("sqlite:///customer_data.sqlite")

# Update table reference:
# sql_database = SQLDatabase(engine, include_tables=["teams"])
sql_database = SQLDatabase(engine, include_tables=["customers"])
# ✅ SQLDatabase and Groq LLM setup
# sql_database = SQLDatabase(engine, include_tables=["matchs"])
llm = Groq(model="llama3-70b-8192", api_key=api_key)
# Update table name reference
query_engine = NLSQLTableQueryEngine(
    sql_database=sql_database,
    tables=["customers"],
    llm=llm
)
# query_engine = NLSQLTableQueryEngine(sql_database=sql_database, tables=["matchs"], llm=llm)
# query_engine = NLSQLTableQueryEngine(sql_database=sql_database, tables=["teams"], llm=llm)
# ✅ FastAPI app
app = FastAPI()

#This is running.
@app.get("/")
def home():
    return {"message": "✅ FastAPI is running! Use /query to ask questions."}

@app.get("/query")
def query_database(user_query: str):
    """Receive a natural language query, generate SQL, and return result.."""
    try:
        response = query_engine.query(user_query)
        return {"query": user_query, "answer": str(response)}
    except Exception as e:
        return {"error": f"Database execution failed: {str(e)}"}


