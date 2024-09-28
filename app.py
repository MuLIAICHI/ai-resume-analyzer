import streamlit as st
from src.document_processor import load_and_process_pdf
from src.qa_chain import create_qa_chain
from src.graph_generator import create_graph_from_text, visualize_graph
from src.utils import set_openai_api_key, set_neo4j_connection
import base64

# Set page config
st.set_page_config(layout="wide", page_title="AI Resume Analyzer", page_icon="📄")

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #f0f2f6;
    }
    .stApp {
        max-width: auto;
        margin: 0 auto;
    }
    .css-1d391kg {
        padding-top: 3rem;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 20px;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #45a049;
        transform: scale(1.05);
    }
    .css-1v0mbdj.etr89bj1 {
        border-radius: 10px;
        border: 2px solid #4CAF50;
        padding: 20px;
        background-color: white;
    }
    .css-1v0mbdj.etr89bj1:hover {
        border-color: #45a049;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .main .block-container {
        padding-bottom: 60px;
    }
    footer {
        visibility: hidden;
    }
    .footer-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 10px;
        background-color: #f0f2f6;
        border-top: 1px solid #4CAF50;
        text-align: center;
    }
    .footer-text {
        visibility: visible;
        display: inline-block;
    }
    .footer-text a {
        color: #4CAF50;
        text-decoration: none;
        font-weight: bold;
        transition: color 0.3s ease;
    }
    .footer-text a:hover {
        color: #45a049;
        text-decoration: underline;
    }
</style>
""", unsafe_allow_html=True)

# Helper function for background image
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover;
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

# Add background image
add_bg_from_local('background.png')  # Make sure to have a background.png file in your project directory

# App Header
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>📄 AI Resume Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 20px;'>Upload a resume and get instant insights!</p>", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'documents' not in st.session_state:
    st.session_state.documents = None
if 'qa_chain' not in st.session_state:
    st.session_state.qa_chain = None
if 'graphs' not in st.session_state:
    st.session_state.graphs = []

# Set up Neo4j connection
driver = set_neo4j_connection()
if driver is None:
    st.error("Failed to connect to Neo4j database. Please check your connection settings.")
    st.stop()

# File uploader
uploaded_file = st.file_uploader("📤 Upload Resume (PDF)", type=["pdf"])

if uploaded_file is not None:
    with st.spinner("🔍 Analyzing Resume..."):
        documents, df = load_and_process_pdf(uploaded_file)
        if documents is not None and df is not None:
            st.session_state.documents = documents
            st.session_state.qa_chain = create_qa_chain(documents)
            st.success("✅ Resume processed successfully!")
            st.balloons()
        else:
            st.error("❌ Error processing PDF. Please check the file.")

# Chat interface
st.markdown("<h2 style='text-align: center; color: #4CAF50;'>💬 Chat with AI about the Resume</h2>", unsafe_allow_html=True)

for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and i < len(st.session_state.graphs):
            graph = st.session_state.graphs[i]
            if graph:
                st.subheader("🔗 Relationship Graph")
                st.markdown("""
                <div style="background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                    <h4 style="color: #4CAF50;">Graph Legend:</h4>
                    <ul>
                        <li><span style="color: #00ff00;">◆</span> Green Diamonds: Categories or Types (e.g., Person, Education, Company)</li>
                        <li><span style="color: #87CEFA;">●</span> Light Blue Circles: Specific Entities or Information</li>
                        <li><span style="color: #4CAF50;">───</span> Green Lines: Relationships between entities</li>
                    </ul>
                    <p>This graph visualizes the relationships between different elements in the resume. 
                    Categories are represented by green diamonds, while specific information is shown as light blue circles. 
                    The lines indicate how these elements are connected.</p>
                </div>
                """, unsafe_allow_html=True)
                st.components.v1.html(graph, height=600, scrolling=True)

if prompt := st.chat_input("Ask about the resume..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if st.session_state.qa_chain is None:
            st.warning("⚠️ Please upload a resume PDF first.")
        else:
            with st.spinner("🧠 Analyzing..."):
                response = st.session_state.qa_chain({"query": prompt})
                st.markdown(response['result'])
                
                # Generate and display graph
                try:
                    create_graph_from_text(response['result'], driver)
                    net = visualize_graph(response['result'], driver)
                    if net:
                        net.save_graph("graph.html")
                        graph_html = open("graph.html", 'r').read()
                        st.session_state.graphs.append(graph_html)
                        st.subheader("🔗 Relationship Graph")
                        st.markdown("""
                        <div style="background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                            <h4 style="color: #4CAF50;">Graph Legend:</h4>
                            <ul>
                                <li><span style="color: #00ff00;">◆</span> Green Diamonds: Categories or Types (e.g., Person, Education, Company)</li>
                                <li><span style="color: #87CEFA;">●</span> Light Blue Circles: Specific Entities or Information</li>
                                <li><span style="color: #4CAF50;">───</span> Green Lines: Relationships between entities</li>
                            </ul>
                            <p>This graph visualizes the relationships between different elements in the resume. 
                            Categories are represented by green diamonds, while specific information is shown as light blue circles. 
                            The lines indicate how these elements are connected.</p>
                        </div>
                        """, unsafe_allow_html=True)
                        st.components.v1.html(graph_html, height=600, scrolling=True)
                    else:
                        st.session_state.graphs.append(None)
                        st.info("ℹ️ No graph could be generated for this query.")
                except Exception as e:
                    st.session_state.graphs.append(None)
                    st.error(f"❌ Error generating graph: {str(e)}")

    st.session_state.messages.append({"role": "assistant", "content": response['result']})

# Sidebar
with st.sidebar:
    st.markdown("### 🚀 About AI Resume Analyzer")
    st.info(
        "This app uses advanced AI to analyze resumes and provide insights. "
        "Upload a PDF resume and start asking questions to get detailed analysis!"
    )
    st.markdown("### 🔑 Key Features")
    st.success("✅ PDF Resume Analysis\n✅ AI-powered Q&A\n✅ Visual Relationship Graphs")

# Footer
st.markdown(
    """
    <div class="footer-container">
        <div class="footer-text">
            Made with ❤️ by <a href="https://www.ragforall.com" target="_blank">RAG for All</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Run the Streamlit app
if __name__ == "__main__":
    set_openai_api_key()