from contextlib import asynccontextmanager
from fastapi import FastAPI
from typing import List
from pydantic import BaseModel
import os
import ollama
import chromadb

from langchain_community.document_loaders import Docx2txtLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

client = chromadb.Client()
collection = client.create_collection(name="docs")

def load_documents(folder_path: str) -> List[Document]:
    documents = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if filename.endswith('.pdf'):
            loader = PyPDFLoader(file_path)
        elif filename.endswith('.docx'):
            loader = Docx2txtLoader(file_path)
        else:
            print(f"unsupported file type: {filename}")
            continue
        documents.extend(loader.load())
    return documents

def split_documents(documents: List[Document]) -> List[Document]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=150,
        chunk_overlap=50,
        length_function=len
    )
    return text_splitter.split_documents(documents)

def embednstore(splits, collection):
    for i, doc in enumerate(splits):
        text = doc.page_content
        response = ollama.embed(model="mxbai-embed-large", input=text)
        embeddings = response["embeddings"]

        collection.add(
            ids=[str(i)],
            embeddings=embeddings,
            documents=[text]
        )

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    documents = load_documents("/home/ruta/irishep/test_files")
    splits = split_documents(documents)
    embednstore(splits, collection)
    yield
    # Shutdown code (if any) goes here, for now nothing

app = FastAPI(lifespan=lifespan)

# Pydantic model for input query
class Query(BaseModel):
    question: str

@app.post("/query")
async def query_rag(query: Query):
    input_text = query.question
    resp = ollama.embed(model="mxbai-embed-large", input=input_text)
    query_embedding = resp["embeddings"][0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=2
    )

    data = results['documents'][0][0]

    output = ollama.generate(
        model="llama3",
        prompt=f"""You are a helpful assistant with access to this data: {data}
            Only use the above data to answer the following question, without hallucinating or making up your own statements: {input_text}
            If the answer is not in the provided data, say "I don't know based on the available information"
        """
    )

    return {"response": output['response']}
