# Required libraries
import pandas as pd
from langchain.docstore.document import Document

# Step 1: Load both Excel files
df1 = pd.read_excel("file1.xlsx")  # Replace with actual file path
df2 = pd.read_excel("file2.xlsx")  # Replace with actual file path

# Step 2: Merge or link the two files (assuming they share a common key, say 'ID')
# Adjust 'ID' to the actual key column that links them
merged_df = pd.merge(df1, df2, on="ID", how="inner")

# Step 3: Convert merged rows into a list of LangChain Documents
# You can also preprocess or format content here if needed
doc_list = []
for _, row in merged_df.iterrows():
    # Combine all columns into a single text content
    content = "\n".join([f"{col}: {val}" for col, val in row.items()])
    
    # Create a Document object with metadata if needed
    doc = Document(page_content=content, metadata={"source": "excel_merge"})
    doc_list.append(doc)

# `doc_list` is now ready to be embedded or indexed in your RAG pipeline
