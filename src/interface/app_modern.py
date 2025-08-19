"""
Interface moderne inspirée de ClickUp Brain pour le système multi-agents
Design moderne avec dégradés et interface conversationnelle
"""

import streamlit as st
import json
import time
from pathlib import Path
import sys
import os

# Configuration de la page
st.set_page_config(
    page_title="CONNECT'IS - Assistant IA",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personnalisé pour un design moderne
st.markdown("""
<style>
    /* Import de Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Variables CSS */
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --dark-bg: #1a1d29;
        --darker-bg: #151821;
        --card-bg: rgba(255, 255, 255, 0.05);
        --text-primary: #ffffff;
        --text-secondary: #a0a9c0;
        --accent-purple: #8b5cf6;
        --accent-blue: #3b82f6;
        --border-color: rgba(255, 255, 255, 0.1);
    }
    
    /* Reset et base */
    .stApp {
        background: var(--dark-bg);
        font-family: 'Inter', sans-serif;
    }
    
    /* Header moderne */
    .modern-header {
        background: var(--primary-gradient);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
    }
    
    .logo-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        margin-bottom: 1rem;
    }
    
    .logo-circle {
        width: 80px;
        height: 80px;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        backdrop-filter: blur(10px);
        border: 2px solid rgba(255, 255, 255, 0.3);
    }
    
    .logo-brain {
        font-size: 40px;
        color: #ffffff;
    }
    
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: white;
        margin: 0;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    }
    
    .subtitle {
        font-size: 1.1rem;
        color: rgba(255, 255, 255, 0.9);
        margin-top: 0.5rem;
        font-weight: 400;
    }
    
    /* Interface de chat moderne */
    .chat-container {
        background: var(--card-bg);
        border-radius: 20px;
        padding: 2rem;
        backdrop-filter: blur(10px);
        border: 1px solid var(--border-color);
        margin-bottom: 2rem;
        min-height: 500px;
    }
    
    .chat-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .chat-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }
    
    .chat-description {
        color: var(--text-secondary);
        font-size: 1rem;
    }
    
    /* Messages de chat */
    .message {
        margin-bottom: 1.5rem;
        animation: fadeInUp 0.3s ease-out;
    }
    
    .message-user {
        text-align: right;
    }
    
    .message-assistant {
        text-align: left;
    }
    
    .message-bubble {
        display: inline-block;
        padding: 1rem 1.5rem;
        border-radius: 20px;
        max-width: 80%;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    
    .message-user .message-bubble {
        background: var(--accent-purple);
        color: white;
        border-bottom-right-radius: 5px;
    }
    
    .message-assistant .message-bubble {
        background: var(--card-bg);
        color: var(--text-primary);
        border: 1px solid var(--border-color);
        border-bottom-left-radius: 5px;
    }
    
    /* Zone de saisie moderne */
    .input-container {
        background: var(--card-bg);
        border-radius: 15px;
        padding: 1.5rem;
        border: 1px solid var(--border-color);
        backdrop-filter: blur(10px);
    }
    
    /* Suggestions */
    .suggestions-container {
        margin-top: 1rem;
    }
    
    .suggestion-chip {
        display: inline-block;
        background: rgba(139, 92, 246, 0.2);
        color: var(--accent-purple);
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.25rem;
        font-size: 0.85rem;
        cursor: pointer;
        border: 1px solid rgba(139, 92, 246, 0.3);
        transition: all 0.2s ease;
    }
    
    .suggestion-chip:hover {
        background: var(--accent-purple);
        color: white;
        transform: translateY(-1px);
    }
    
    /* Sidebar moderne */
    .sidebar-section {
        background: var(--card-bg);
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border: 1px solid var(--border-color);
        backdrop-filter: blur(10px);
    }
    
    .sidebar-title {
        color: var(--text-primary);
        font-weight: 600;
        margin-bottom: 1rem;
        font-size: 1.1rem;
    }
    
    .status-indicator {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.5rem;
    }
    
    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #10b981;
    }
    
    .status-text {
        color: var(--text-secondary);
        font-size: 0.9rem;
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2rem;
        }
        
        .chat-container {
            padding: 1rem;
        }
        
        .message-bubble {
            max-width: 90%;
        }
    }
    
    /* Cacher les éléments Streamlit par défaut */
    .stDeployButton {
        display: none;
    }
    
    #MainMenu {
        visibility: hidden;
    }
    
    footer {
        visibility: hidden;
    }
    
    header {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

def load_workflow():
    """Charge le workflow multi-agents"""
    try:
        from src.workflows.multi_agent_workflow import MultiAgentWorkflow
        return MultiAgentWorkflow()
    except Exception as e:
        st.error(f"Erreur lors du chargement du workflow: {e}")
        return None

def render_header():
    """Affiche l'en-tête moderne"""
    st.markdown("""
    <div class="modern-header">
        <div class="logo-container">
            <div class="logo-circle">
                <div class="logo-brain">🧠</div>
            </div>
        </div>
        <h1 class="main-title">CONNECT'IS</h1>
        <p class="subtitle">Assistant IA Multi-Systèmes - Connectez vos applications en toute simplicité</p>
    </div>
    """, unsafe_allow_html=True)

def render_chat_interface():
    """Affiche l'interface de chat moderne"""
    st.markdown("""
    <div class="chat-container">
        <div class="chat-header">
            <h2 class="chat-title">Bonjour! Comment puis-je vous aider aujourd'hui?</h2>
            <p class="chat-description">Posez vos questions sur le CRM, RH, ou gestion de projets. Je peux vous aider à gérer vos données.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Historique des messages
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Affichage des messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="message message-user">
                <div class="message-bubble">{message["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="message message-assistant">
                <div class="message-bubble">{message["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_input_section():
    """Affiche la zone de saisie moderne"""
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    
    # Zone de saisie principale
    user_input = st.text_input(
        "Message",
        placeholder="Demander, créer, rechercher, @ pour mentionner...",
        key="user_input",
        label_visibility="collapsed"
    )
    
    # Boutons de suggestion
    st.markdown("""
    <div class="suggestions-container">
        <span style="color: var(--text-secondary); font-size: 0.9rem; margin-right: 1rem;">Suggestions:</span>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📋 Liste des clients", key="sugg1"):
            st.session_state.user_input = "liste tous les clients"
            st.rerun()
    
    with col2:
        if st.button("💼 Opportunités", key="sugg2"):
            st.session_state.user_input = "montre-moi les opportunités"
            st.rerun()
    
    with col3:
        if st.button("👥 Employés RH", key="sugg3"):
            st.session_state.user_input = "liste des employés"
            st.rerun()
    
    with col4:
        if st.button("📊 Projets", key="sugg4"):
            st.session_state.user_input = "statut des projets"
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    return user_input

def render_sidebar():
    """Affiche la sidebar moderne"""
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-section">
            <h3 class="sidebar-title">🔌 Connexions</h3>
            <div class="status-indicator">
                <div class="status-dot"></div>
                <span class="status-text">Odoo CRM - Connecté</span>
            </div>
            <div class="status-indicator">
                <div class="status-dot"></div>
                <span class="status-text">Base RH - Connectée</span>
            </div>
            <div class="status-indicator">
                <div class="status-dot"></div>
                <span class="status-text">Gestion Projets - Connectée</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="sidebar-section">
            <h3 class="sidebar-title">📊 Statistiques</h3>
            <div style="color: var(--text-secondary); font-size: 0.9rem;">
                <p>• Sessions aujourd'hui: 12</p>
                <p>• Requêtes traitées: 84</p>
                <p>• Temps de réponse: 0.8s</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="sidebar-section">
            <h3 class="sidebar-title">🎯 Actions rapides</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 Actualiser données", use_container_width=True):
            st.success("Données actualisées!")
        
        if st.button("📥 Exporter rapport", use_container_width=True):
            st.info("Export en cours...")
        
        if st.button("⚙️ Paramètres", use_container_width=True):
            st.info("Paramètres disponibles bientôt")

def process_user_message(message: str, workflow):
    """Traite le message utilisateur avec le workflow"""
    if not workflow:
        return "❌ Erreur: Workflow non disponible"
    
    try:
        # Ajouter le message utilisateur
        st.session_state.messages.append({"role": "user", "content": message})
        
        # Simuler un délai de traitement
        with st.spinner("🤔 Réflexion en cours..."):
            time.sleep(1)
            result = workflow.process_user_request(message)
        
        # Formater la réponse
        if result.get("success"):
            response = "✅ **Opération réussie**\n\n"
            
            # Ajouter les données si disponibles
            if result.get("data"):
                data = result["data"]
                if isinstance(data, dict):
                    if data.get("count", 0) > 0:
                        response += f"📊 **{data['count']} résultat(s) trouvé(s)**\n\n"
                        
                        # Afficher un échantillon des données
                        items = data.get("data", [])[:3]  # Limiter à 3 éléments
                        for item in items:
                            if isinstance(item, dict):
                                name = item.get("nom", item.get("titre", "Element"))
                                response += f"• **{name}**"
                                if item.get("email"):
                                    response += f" - {item['email']}"
                                if item.get("id"):
                                    response += f" (ID: {item['id']})"
                                response += "\n"
                        
                        if len(data.get("data", [])) > 3:
                            response += f"\n... et {len(data.get('data', [])) - 3} autre(s)\n"
            
            # Ajouter le résumé si disponible
            summary = result.get("summary")
            if summary:
                response += f"\n💡 **Résumé**: {summary}"
            
        else:
            response = f"❌ **Erreur**: {result.get('error', 'Erreur inconnue')}"
        
        # Ajouter la réponse de l'assistant
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        return response
        
    except Exception as e:
        error_msg = f"❌ **Erreur système**: {str(e)}"
        st.session_state.messages.append({"role": "assistant", "content": error_msg})
        return error_msg

def main():
    """Fonction principale de l'application"""
    # Initialisation
    workflow = load_workflow()
    
    # Rendu de l'interface
    render_header()
    render_sidebar()
    
    # Interface principale
    render_chat_interface()
    
    # Zone de saisie
    user_input = render_input_section()
    
    # Traitement du message
    if user_input and user_input.strip():
        process_user_message(user_input, workflow)
        # Effacer le champ de saisie en réexécutant
        st.rerun()
    
    # Footer moderne
    st.markdown("""
    <div style="text-align: center; margin-top: 3rem; padding: 2rem; color: var(--text-secondary); font-size: 0.85rem;">
        🚀 Propulsé par CONNECT'IS - Assistant IA Multi-Systèmes
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
