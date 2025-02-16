# AI proposal generator

# Load libraries
import streamlit as st
import PyPDF2
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
from langchain_ollama import OllamaEmbeddings
#from langchain.chains.question_answering import load_qa_chain
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage

# Run app in terminal
# python -m streamlit run app.py

# Define model and embeddings
MODEL = Ollama(model="llama3.2")
embeddings = OllamaEmbeddings(model= "llama3.2")

# Function to extract text from PDF
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text()
    return text

# Define streamlit app
def proposal_writer():
    st.set_page_config(page_title="Grants Assistant App", page_icon="📄")
    st.title("Grants Assistant App")
    st.write("Upload a PDF and ask questions about its content using an AI model (Llama 3.2).")

    # Upload PDF file
    pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if pdf_file is not None:
        # Extract text from PDF
        text = extract_text_from_pdf(pdf_file)
        
        # Display extracted text (optional)
        if st.checkbox("Show extracted text"):
            st.write(text)
        
        if text.strip():
            # Create embeddings and Llama model
            st.write("[DEBUG] Creating embeddings...")
            embeddings = OllamaEmbeddings(model= "llama3.2")
            st.write("[DEBUG] Embeddings created successfully.")
            
            st.write("[DEBUG] Loading Llama model...")
            llama = MODEL
            st.write("[DEBUG] Llama model loaded successfully.")
            
            # Create a FAISS vector store
            st.write("[DEBUG] Creating FAISS vector store...")
            vector_store = FAISS.from_texts([text], embeddings)
            st.write("[DEBUG] FAISS vector store created successfully.")
            
            # Create a QA chain
            st.write("[DEBUG] Creating QA chain...")
            template = """
            You assist grant-makers and program managers at nonprofit organizations in streamlining their grant-making process and generates rapid insights for their day-to-day operations. You will serve as an assistant agent as such you will use friendly but professional tone. 
        
            Answer the question based on the context  and the history below. You will recommend and give feedback on best practices to get their grant applications accepted. 
            You will avoid being too general, providing context, when appropriate based on the question, to answers and market trend analysis based on the nonprofit space the user is in. 

            If you cannot answer the question, you will ask questions to understand the nonprofit organization and its programs for which the grant is being applied. 

            You may also ask what the user needs help with. Some conversation starters might be around grant applications, internal resource allocations help, program development, fundraising options or match with a private funder.
            
            Chat history: {chat_history}

            Context: {context}

            Question: {question}
            """
            parser = StrOutputParser()
            prompt = PromptTemplate.from_template(template)
            #qa = RetrievalQA(llm=llama, retriever=vector_store.as_retriever())
            #qa_chain = load_qa_chain(llama, chain_type="stuff")
            chain = prompt | llama | parser
            st.write("[DEBUG] QA chain created successfully.")
            
            # Question input and chat history
            # neither chat history nor huma/ai appear
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = []
            
            question = st.chat_input("Type your message here")     

            #question = st.text_input("Ask a question about the document:")

            if question is not None and question != "":
                st.session_state.chat_history.append(HumanMessage(question))
                context = vector_store.similarity_search(question, k=1)[0].page_content
                st.write(f"[DEBUG] Received question: {question}")

                with st.chat_message("Human"):
                    st.markdown(question)

                with st.chat_message("AI"):
                    answer = st.write_stream(chain.stream({"chat_history": st.session_state.chat_history,"context": context, "question": question}) )
                    st.write("[DEBUG] Answer generated successfully.")
                    st.write("Answer:", answer)
                st.session_state.chat_history.append(AIMessage(content=answer))
                # Get answer from the Llama model
                #answer = qa.run(question)
                #answer = qa_chain.run(input_documents=[text], question=question)
                
        else:
            st.write("[DEBUG] No text extracted from the PDF.")


