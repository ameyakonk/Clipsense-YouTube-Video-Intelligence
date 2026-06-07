import streamlit as st
from ingestion_pipeline import Ingest
from retreival_pipeline import Retrieve

st.title("ClipSense - Youtube")

url = st.text_input("Youtube url")
question = st.text_input("Ask a question")

if st.button("Ask"):
    if url and question:
        
        with st.spinner("Ingesting video..."):
            ingest_pipe = Ingest(url)
            ingest_pipe.ingestion()
        
        with st.spinner("Thinking..."):
            retrieve_pipe = Retrieve(query=question)
            answer = retrieve_pipe.llm_response()
        st.write(answer)