from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

def create_qa_chain(documents):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(documents, embeddings)
    
    template = """
    You are an expert HR analyst specializing in resume evaluation and career counseling. Your task is to provide detailed, insightful answers to questions about the resume you've been given. Use the following context from the resume to inform your analysis.

    Resume Context: {context}

    When answering, please follow these guidelines:
    1. Provide a comprehensive analysis based on the resume content.
    2. Include specific examples or notable points from the resume.
    3. If relevant, mention any quantifiable achievements or metrics mentioned in the resume.
    4. Consider various aspects such as work experience, education, skills, projects, and any other relevant factors.
    5. If asked about career paths or potential roles, analyze the resume content to suggest suitable options.
    6. If the question cannot be fully answered with the given context, state what you can confidently say based on the resume and what additional information might be needed.

    Question: {question}

    Detailed Analysis:
    """
    
    PROMPT = PromptTemplate(template=template, input_variables=["context", "question"])
    
    llm = ChatOpenAI(model_name="gpt-4o", temperature=0)
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(),
        chain_type_kwargs={"prompt": PROMPT}
    )
    return qa_chain