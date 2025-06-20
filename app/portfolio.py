# portfolio.py
# import pandas as pd
# from langchain.vectorstores import Chroma
# from langchain.embeddings import HuggingFaceEmbeddings
# import pysqlite3
# import sys
# sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

# import chromadb
# import uuid
# import os
# import shutil

# class Portfolio:
#     def __init__(self, file_path="app/data/portfolio.csv", default_path="app/data/portfolio_default.csv"):
#         self.file_path = file_path
#         self.default_path = default_path
#         embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
#         self.chroma_client = chromadb.PersistentClient('vectorstore')
#         # self.collection = self.chroma_client.get_or_create_collection(
#         #     name="portfolio",
#         #     embedding_function=self.embedding_function
#         # )
#         self.collection = Chroma(
#             collection_name="portfolio",
#             embedding_function=embedding_function,
#             persist_directory="vectorstore"
#         )
#         self.data = None

#     def reset_to_default(self):
#         """Reset the active portfolio to the default one."""
#         shutil.copy(self.default_path, self.file_path)
#         self.load_portfolio()

#     def load_portfolio(self):
#         """Load portfolio from the active file path and populate the ChromaDB collection."""
#         if not os.path.exists(self.file_path):
#             raise FileNotFoundError(f"Portfolio file not found: {self.file_path}")
        
#         self.data = pd.read_csv(self.file_path)

#         # Clear existing data to avoid duplicates or stale entries
#         if self.collection.count():
#             self.collection.delete(ids=self.collection.get()['ids'])

#         for _, row in self.data.iterrows():
#             # self.collection.add(
#             #     documents=row["Techstack"],
#             #     metadatas={"links": row["Links"]},
#             #     ids=[str(uuid.uuid4())]
#             # )
#             self.collection.add_texts(
#                 texts=[row["Techstack"]],
#                 metadatas=[{"links": row["Links"]}]
#             )


#     def query_links(self, skills):
#         # return self.collection.query(query_texts=skills, n_results=2).get('metadatas', [])
#         results = self.collection.similarity_search(query=skills, k=2)
#         return [doc.metadata for doc in results]

import os
import shutil
import uuid
import pandas as pd

from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

class Portfolio:
    def __init__(self, file_path="app/data/portfolio.csv", default_path="app/data/portfolio_default.csv"):
        self.file_path = file_path
        self.default_path = default_path

        self.embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        self.collection = Chroma(
            collection_name="portfolio",
            embedding_function=self.embedding_function,
            persist_directory="vectorstore"
        )

        self.data = None

    def reset_to_default(self):
        """Reset the active portfolio to the default one."""
        shutil.copy(self.default_path, self.file_path)
        self.load_portfolio()

    def load_portfolio(self):
        """Load portfolio from CSV and populate the vectorstore."""
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Portfolio file not found: {self.file_path}")

        self.data = pd.read_csv(self.file_path)

        self.collection = Chroma(
            collection_name="portfolio",
            embedding_function=self.embedding_function,
            persist_directory="vectorstore"
        )
        self.collection.delete_collection()
        self.collection = Chroma(
            collection_name="portfolio",
            embedding_function=self.embedding_function,
            persist_directory="vectorstore"
        )

        for _, row in self.data.iterrows():
            techstack = str(row["Techstack"])
            link = str(row["Links"])
            self.collection.add_texts(texts=[techstack], metadatas=[{"links": link}])

    def query_links(self, skills):
        """Query vectorstore to find top matching portfolio items."""
        try:
            results = self.collection.similarity_search(query=skills, k=2)
            return [doc.metadata for doc in results]
        except Exception as e:
            print("Vector query failed:", e)
            return []



