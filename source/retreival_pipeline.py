from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage


class Retrieve:
    def __init__(self, query:str):
        load_dotenv()
        self.query = query
        self.persistent_directory = "db/chroma_db"
        self.embedding_model = OpenAIEmbeddings(model = "text-embedding-3-small")
        db = Chroma(
            persist_directory=self.persistent_directory,
            embedding_function=self.embedding_model,
            collection_metadata={"hnsw:space":"cosine"}
        )
        self.retreiver = db.as_retriever(search_type = "mmr", 
                            search_kwargs = {"k": 3, "score_threshold": 0.3})
        self.model = ChatOpenAI(model="gpt-4o")

    def retreive_docs(self):
        docs = self.retreiver.invoke(self.query)

        print("---- Context ----")
        for i, doc in enumerate(docs, 1):
            print(f"Document {i}:\n{doc.page_content}\n")

        return docs

    def input_for_llm(self):
        docs = self.retreive_docs()
        combined_input = f"""Based on the following documents, please answer this question: {self.query}

        Documents:
        {
            chr(10).join([f"-{doc.page_content}" for doc in docs])
        }

        Please provide a clear, helpful answer using only the information from the documents. If you can't find the answer, say did not find info"""

        print(f"\nCombined input: {combined_input}")
        return combined_input

    def llm_response(self):
        print(f"\nUser Query: {self.query}")
        combined_input = self.input_for_llm()
        print(f"\n---- Combined Input: {combined_input} ---")
        messages = [
            SystemMessage(content="You are analyzing a conversation transcript. The text may be informal, fragmented, or lack punctuation. \
                        Answer the question based only on the provided transcript excerpts."),
            HumanMessage(content=combined_input),
        ]
        result = self.model.invoke(messages)
        print("\n---- Generated Response ---")
        print(result.content)
        return result.content


# query = "Provide details about attention head of the transformer?"

# # retreiver = db.as_retriever(search_kwargs = {"k": 3})
# # retreiver = db.as_retriever(search_type = "similarity_score_threshold", 
# #                             search_kwargs = {"k": 3, "score_threshold": 0.3})

# if __name__ == "__main__":
#     retrieve_pipe = Retrieve(query=query)
#     retrieve_pipe.llm_response()













