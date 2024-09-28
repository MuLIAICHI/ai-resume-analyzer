# AI Resume Analyzer

## 📄 About
AI Resume Analyzer is an innovative Streamlit application that leverages the power of AI to analyze resumes and provide insightful feedback. This tool uses advanced natural language processing and graph visualization techniques to extract key information from resumes and present it in an easily digestible format.

## 🌟 Features
- **PDF Resume Upload**: Easily upload PDF resumes for analysis.
- **AI-Powered Q&A**: Ask questions about the resume and get intelligent responses.
- **Visual Relationship Graphs**: Visualize connections between different elements of the resume.
- **Interactive Chat Interface**: Engage in a conversation-like interaction with the AI.
- **Persistent Graph Visualization**: Graphs are saved and displayed for each query, allowing for easy comparison and reference.

## 🛠 Technologies Used
- Streamlit
- OpenAI GPT
- Neo4j Graph Database
- LangChain
- PyViz Network

## 🚀 Getting Started

### Prerequisites
- Python 3.7+
- Neo4j Database
- OpenAI API Key

### Installation
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ai-resume-analyzer.git
   cd ai-resume-analyzer
   ```

2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the root directory and add your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key
   NEO4J_URI=your_neo4j_uri
   NEO4J_USERNAME=your_neo4j_username
   NEO4J_PASSWORD=your_neo4j_password
   ```

4. Add a background image:
   Place a file named `background.png` in the root directory of the project.

### Running the App
Run the Streamlit app:
```
streamlit run app.py
```

## 📌 Usage
1. Upload a PDF resume using the file uploader.
2. Once processed, start asking questions about the resume in the chat interface.
3. View AI-generated responses and relationship graphs for each query.
4. Explore the visual representations to gain deeper insights into the resume.

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check [issues page](https://github.com/yourusername/ai-resume-analyzer/issues).



## 🙏 Acknowledgements
- [Streamlit](https://streamlit.io/)
- [OpenAI](https://openai.com/)
- [Neo4j](https://neo4j.com/)
- [LangChain](https://langchain.com/)
- [RAG for All](https://www.ragforall.com)

---
Made with ❤️ by RAGForAll