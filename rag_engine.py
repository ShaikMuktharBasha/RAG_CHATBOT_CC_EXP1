import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

class RAGEngine:
    def __init__(self, google_api_key=None, model="gemini-1.5-flash"):
        # Load environment variables
        load_dotenv()
        
        # Initialize embeddings model
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': False}
        )
        
        # Initialize Gemini LLM with API Key
        api_key = google_api_key or os.environ.get("GOOGLE_API_KEY") 
            
        if api_key:
            self.llm = ChatGoogleGenerativeAI(
                model=model,
                temperature=0.3,
                google_api_key=api_key
            )
        else:
            self.llm = None
        
        # Define prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful and professional Employee Handbook Assistant. "
                        "Answer the user's question based strictly on the provided context from the employee handbook.\n\n"
                        "Context:\n{context}\n\n"
                        "If you don't know the answer based on the context, just say you don't know "
                        "and encourage them to contact HR."),
            ("human", "{input}")
        ])
        
        self.vectorstore = None
        
    def process_document(self, file_path):
        """Load PDF, split text, and create FAISS index."""
        try:
            # Load PDF
            loader = PyPDFLoader(file_path)
            documents = loader.load()
            num_pages = len(documents)
            
            # Split text into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len
            )
            chunks = text_splitter.split_documents(documents)
            num_chunks = len(chunks)
            
            # Create FAISS vector store
            self.vectorstore = FAISS.from_documents(chunks, self.embeddings)
            
            return {
                "success": True,
                "num_pages": num_pages,
                "num_chunks": num_chunks
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
            
    def answer_question(self, query, top_k=5, language="English"):
        """Retrieve relevant context and generate answer."""
        if not self.vectorstore:
            return {"error": "Please upload and process a handbook first."}
            
        if not self.llm:
             return {"error": "LLM is not initialized (missing API key)."}
             
        try:
            # Dynamically adjust prompt if a non-English target language is specified
            if language and language.lower() != "english":
                custom_prompt = ChatPromptTemplate.from_messages([
                    ("system", "You are a helpful and professional Multilingual Employee Handbook Assistant. "
                                f"Answer the user's question based strictly on the provided context. "
                                f"IMPORTANT: You MUST write your final response entirely in {language}.\n\n"
                                "Context:\n{context}\n\n"
                                f"If you don't know the answer based on the context, say that you don't know in {language} "
                                "and encourage them to contact HR."),
                    ("human", "{input}")
                ])
                document_chain = create_stuff_documents_chain(self.llm, custom_prompt)
            else:
                document_chain = create_stuff_documents_chain(self.llm, self.prompt)
                
            retriever = self.vectorstore.as_retriever(search_kwargs={"k": top_k})
            retrieval_chain = create_retrieval_chain(retriever, document_chain)
            
            # Invoke chain
            response = retrieval_chain.invoke({"input": query})
            
            return {
                "answer": response["answer"],
                "score": 1.0, # Generative models don't return a direct score like DistilBERT, setting to 1.0 for compatibility
                "context": [
                    {
                        "content": doc.page_content,
                        "metadata": doc.metadata
                    }
                    for doc in response["context"]
                ]
            }
        except Exception as e:
            return {"error": f"Failed to generate answer: {str(e)}"}

