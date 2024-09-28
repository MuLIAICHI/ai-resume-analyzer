from langchain_community.chat_models import ChatOpenAI
from langchain_experimental.graph_transformers import LLMGraphTransformer
from pyvis.network import Network
from neo4j import GraphDatabase
import re
import streamlit as st

def create_graph_from_text(text, driver):
    llm = ChatOpenAI(temperature=0, model_name="gpt-4")
    llm_transformer = LLMGraphTransformer(llm=llm)

    # Convert text to a format that LLMGraphTransformer can process
    from langchain.docstore.document import Document
    doc = Document(page_content=text)
    graph_documents = llm_transformer.convert_to_graph_documents([doc])
    
    def escape_cypher_string(s):
        return s.replace('\\', '\\\\').replace("'", "\\'")
    
    with driver.session() as session:
        for graph_document in graph_documents:
            # Create nodes
            for node in graph_document.nodes:
                node_id = escape_cypher_string(node.id)
                node_type = escape_cypher_string(node.type)
                node_name = escape_cypher_string(node.properties.get('name', node_id))
                query = f"MERGE (n:`{node_type}` {{id: '{node_id}', name: '{node_name}'}})"
                try:
                    session.run(query)
                except Exception as e:
                    print(f"Error executing query: {query}")
                    print(f"Error message: {str(e)}")
            
            # Create relationships
            for relationship in graph_document.relationships:
                source_node = relationship.source
                target_node = relationship.target
                relationship_type = escape_cypher_string(relationship.type)
                
                query = f"""
                MATCH (source:`{escape_cypher_string(source_node.type)}` {{id: '{escape_cypher_string(source_node.id)}'}})
                MATCH (target:`{escape_cypher_string(target_node.type)}` {{id: '{escape_cypher_string(target_node.id)}'}})
                MERGE (source)-[:`{relationship_type}`]->(target)
                """
                try:
                    session.run(query)
                except Exception as e:
                    print(f"Error executing query: {query}")
                    print(f"Error message: {str(e)}")
    
    return graph_documents

def visualize_graph(text, driver):
    def escape_cypher_string(s):
        return s.replace('\\', '\\\\').replace("'", "\\'")

    words = re.findall(r'\b\w+\b', text)
    entity_names = set(words)

    escaped_entities = [f"'{escape_cypher_string(entity)}'" for entity in entity_names if entity]
    entity_list = ", ".join(escaped_entities)

    query = f"""
    MATCH (n)-[r]->(m)
    WHERE n.name IN [{entity_list}] OR m.name IN [{entity_list}]
    RETURN n, r, m
    LIMIT 100
    """
    
    try:
        with driver.session() as session:
            graph_result = session.run(query)
            records = list(graph_result)
            
            if not records:
                return None

            net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")
            node_categories = set()
            for record in records:
                node_n = record['n']
                node_m = record['m']
                relationship = record['r']
                
                node_n_type = list(node_n.labels)[0] if node_n.labels else "Unknown"
                node_m_type = list(node_m.labels)[0] if node_m.labels else "Unknown"
                
                node_categories.add(node_n_type)
                node_categories.add(node_m_type)
                
                node_n_label = f"{node_n.get('name', '')}"
                node_m_label = f"{node_m.get('name', '')}"
                
                net.add_node(node_n.id, label=node_n_label, title=f"Type: {node_n_type}")
                net.add_node(node_m.id, label=node_m_label, title=f"Type: {node_m_type}")
                net.add_edge(node_n.id, node_m.id, title=relationship.type)
            
            for category in node_categories:
                net.add_node(category, label=category, color="#00ff00", shape="diamond")
                for node in net.nodes:
                    node_type = node.get('title', '').split(': ')[-1]
                    if node_type == category:
                        net.add_edge(category, node['id'], physics=False)
            
            return net
            
    except Exception as e:
        print(f"Error executing query: {e}")
        return None