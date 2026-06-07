import os
from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader, DirectoryLoader  #load directories
from langchain_text_splitters import RecursiveCharacterTextSplitter  #text splitter
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_openai import OpenAIEmbeddings  #Embedding model
from langchain_chroma import Chroma  #Vector DB
from dotenv import load_dotenv
import re

url = "https://www.youtube.com/watch?v=bCz4OMemCcA"

class Ingest:

    def __init__(self, url:str):
        load_dotenv()
        self.url = url

    def fetch_video_id(self, url:str):
        video_id = url.split("v=")[-1]
        print(f"--- Video ID: {video_id} ---")
        return video_id

    def sanitize_text(self, text):
        text = re.sub(r'\[.*?\]', '', text)
        text = re.sub(r' +', ' ', text)
        text = text.strip()
        return text

    def sanitize_build_documents(self, video_id:str):
        ytt = YouTubeTranscriptApi()
        segments = ytt.fetch(video_id)

        # Sanitize + build Documents
        docs = []
        text = ""
        start_time = segments[0].start
        for seg in segments:
            text += " " + self.sanitize_text(seg.text)

            if not text or text.startswith("["):
                continue

        print(text)
        docs.append(Document(
                page_content=text,
                metadata={"video_id": video_id, "start": start_time, "source": url}
            ))
        print(f"{len(docs)} documents created")
        return docs

    def ingestion(self):
        video_id = self.fetch_video_id(self.url)
        docs = self.sanitize_build_documents(video_id)

        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
        chunks = splitter.split_documents(docs)

        print(f"\n--- Len chunks {len(chunks)} ---")
        print(f"\n--- chunk {chunks[1]}")

        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory="db/chroma_db",
            collection_metadata={"hnsw:space": "cosine"}
        )

# if __name__ == "__main__":
#     ingest_pipe = Ingest(url)
#     docs = ingest_pipe.ingestion()

# # vectorstore = Chroma(
# #         persist_directory="db/chroma_db",
# #         embedding_function=embeddings,
# #         collection_metadata={"hnsw:space": "cosine"}
# #     )



