import os
import time
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH", "document.pdf")
DATABASE_URL = os.environ["DATABASE_URL"]
COLLECTION_NAME = os.environ["PG_VECTOR_COLLECTION_NAME"]
EMBEDDING_MODEL = os.getenv("GOOGLE_EMBEDDING_MODEL", "models/gemini-embedding-001")


def ingest_pdf():
    pdf = Path(PDF_PATH)
    if not pdf.is_absolute():
        pdf = Path(__file__).resolve().parent.parent / pdf

    docs = PyPDFLoader(str(pdf)).load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = splitter.split_documents(docs)

    chunks = [
        Document(
            page_content=c.page_content,
            metadata={k: v for k, v in c.metadata.items() if v not in ("", None)},
        )
        for c in chunks
    ]

    store = PGVector(
        embeddings=GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL),
        collection_name=COLLECTION_NAME,
        connection=DATABASE_URL,
        use_jsonb=True,
    )

    # gambiarra do tpm: gemini free aceita 30k token/min, se mandar tudo de uma vez estoura
    batch_size = 30
    for i in range(0, len(chunks), batch_size):
        store.add_documents(chunks[i:i+batch_size])
        print(f"  {min(i+batch_size, len(chunks))}/{len(chunks)} chunks")
        if i + batch_size < len(chunks):
            time.sleep(60)  # respira pra resetar o limite

    print(f"{len(chunks)} chunks ingeridos em '{COLLECTION_NAME}'.")


if __name__ == "__main__":
    ingest_pdf()
