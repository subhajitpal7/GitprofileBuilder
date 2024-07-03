from langchain_community.chat_models import ChatOllama
from langchain_community.document_loaders import PyPDFium2Loader
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import retrieval_qa
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = PyPDFium2Loader(input("Path to PDF file: "))
data = loader.load()
# Define a function to create a retriever from a document
def create_retriever(document):
    # Use OpenAI embeddings for creating the retriever
    embeddings = GPT4AllEmbeddings(model_name="all-MiniLM-L6-v2.gguf2.f16.gguf")
    # Create a FAISS vector store from the document
    vector_store = FAISS.from_documents(documents=document, embedding=embeddings)
    # Create a dense retriever using the vector stor
    return vector_store
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
all_splits = text_splitter.split_documents(data)
retriever=create_retriever(all_splits)
template="""
Given a Raw text of a Resume of a person . As a Language model and retriver your task is to find out the person's name work experience summary and relevant skill sets.

The text of the resume is given below as :

{context}

Return only the name experience and skillset in json format.

"""

prompt = ChatPromptTemplate.from_template(template)

# LLM
# Select the LLM that you downloaded
ollama_llm = "llama2:7b-chat"
model = ChatOllama(model=ollama_llm)
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

chain= {"context":format_docs} | prompt | model
search="subhajit"
docs=retriever.similarity_search(query=search,k=1)
answer = chain.invoke(docs)
print(answer)