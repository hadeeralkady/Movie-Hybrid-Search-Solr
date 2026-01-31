import pandas as pd
import pysolr

df = pd.read_csv("Data.csv")  
# Connect to Solr
solr = pysolr.Solr('http://localhost:8983/solr/movies', always_commit=True)

# Prepare documents for Solr
docs = []
for i, row in df.iterrows():
    docs.append({
        "id": str(i),  
        "title": row["Title"],
        "plot": row["Plot"],
        "genre": row.get("Genre", ""),
        "year": int(row.get("Release Year", 0)),
        "director": row.get("Director", ""), 
        "origin_ethnicity": row.get("Origin/Ethnicity", "") 
    })

solr.add(docs)
print("✅ Data successfully uploaded")
