# portfolio.py
import pandas as pd
import pysqlite3
import sys
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

import chromadb
import uuid
import os
import shutil

class Portfolio:
    def __init__(self, file_path="app/data/portfolio.csv", default_path="app/data/portfolio_default.csv"):
        self.file_path = file_path
        self.default_path = default_path
        self.chroma_client = chromadb.PersistentClient('vectorstore')
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")
        self.data = None

    def reset_to_default(self):
        """Reset the active portfolio to the default one."""
        shutil.copy(self.default_path, self.file_path)
        self.load_portfolio()

    def load_portfolio(self):
        """Load portfolio from the active file path and populate the ChromaDB collection."""
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Portfolio file not found: {self.file_path}")
        
        self.data = pd.read_csv(self.file_path)

        # Clear existing data to avoid duplicates or stale entries
        if self.collection.count():
            self.collection.delete(ids=self.collection.get()['ids'])

        for _, row in self.data.iterrows():
            self.collection.add(
                documents=row["Techstack"],
                metadatas={"links": row["Links"]},
                ids=[str(uuid.uuid4())]
            )

    def query_links(self, skills):
        return self.collection.query(query_texts=skills, n_results=2).get('metadatas', [])
