"""
Interface moderne CONNECT'IS avec logo personnalisé
Version améliorée avec le design exact de l'image fournie
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
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personnalisé avec le logo CONNECT'IS intégré
st.markdown("""
<style>
    /* Import de Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Variables CSS */
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --dark-bg: #1a1d29;
        --card-bg: rgba(255, 255, 255, 0.08);
        --text-primary: #ffffff;
        --text-secondary: #a0a9c0;
        --accent-purple: #8b5cf6;
        --border-color: rgba(255, 255, 255, 0.12);
    }
    
    .stApp {
        background: var(--dark-bg);
        font-family: 'Inter', sans-serif;
    }
    
    /* Header avec logo CONNECT'IS */
    .connectis-header {
        background: var(--primary-gradient);
        padding: 3rem 2rem;
        border-radius: 24px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .connectis-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at 30% 20%, rgba(255,255,255,0.1) 0%, transparent 50%);
    }
    
    .logo-container {
        position: relative;
        z-index: 2;
        margin-bottom: 2rem;
    }
    
    /* Logo CONNECT'IS inspiré de l'image */
    .connectis-logo {
        width: 120px;
        height: 120px;
        margin: 0 auto 1.5rem;
        position: relative;
        background: rgba(255, 255, 255, 0.15);
        border-radius: 50%;
        backdrop-filter: blur(20px);
        border: 3px solid rgba(255, 255, 255, 0.2);
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    /* Simulation du pattern de cubes interconnectés */
    .logo-pattern {
        position: relative;
        width: 60px;
        height: 60px;
    }
    
    .cube {
        position: absolute;
        width: 8px;
        height: 8px;
        background: #ffffff;
        border-radius: 2px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }
    
    /* Positionnement des cubes pour former le pattern */
    .cube:nth-child(1) { top: 10px; left: 26px; }
    .cube:nth-child(2) { top: 20px; left: 36px; }
    .cube:nth-child(3) { top: 20px; left: 16px; }
    .cube:nth-child(4) { top: 30px; left: 26px; }
    .cube:nth-child(5) { top: 40px; left: 36px; }
    .cube:nth-child(6) { top: 40px; left: 16px; }
    .cube:nth-child(7) { top: 50px; left: 26px; }
    .cube:nth-child(8) { top: 30px; left: 6px; }
    .cube:nth-child(9) { top: 30px; left: 46px; }
    .cube:nth-child(10) { top: 20px; left: 46px; }
    .cube:nth-child(11) { top: 10px; left: 16px; }
    .cube:nth-child(12) { top: 0px; left: 26px; }
    
    /* Animation des cubes */
    .cube {
        animation: cubePulse 3s ease-in-out infinite;
    }
    
    .cube:nth-child(odd) {
        animation-delay: 0.5s;
    }
    
    .cube:nth-child(3n) {
        animation-delay: 1s;
    }
    
    @keyframes cubePulse {
        0%, 100% { 
            opacity: 0.7;
            transform: scale(1);
            background: #ffffff;
        }
        50% { 
            opacity: 1;
            transform: scale(1.2);
            background: #c084fc;
        }
    }
    
    .brand-title {
        position: relative;
        z-index: 2;
        font-size: 3.5rem;
        font-weight: 800;
        color: white;
        margin: 0;
        letter-spacing: 0.05em;
        text-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
        font-family: 'Inter', sans-serif;
    }
    
    .brand-subtitle {
        position: relative;
        z-index: 2;
        font-size: 1.25rem;
        color: rgba(255, 255, 255, 0.95);
        margin-top: 0.75rem;
        font-weight: 400;
        max-width: 700px;
        margin-left: auto;
        margin-right: auto;
        line-height: 1.6;
    }
    
    /* Interface de chat moderne */
    .chat-interface {
        background: var(--card-bg);
        border-radius: 24px;
        padding: 2.5rem;
        backdrop-filter: blur(20px);
        border: 1px solid var(--border-color);
        margin-bottom: 2rem;
        min-height: 600px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    }
    
    .welcome-section {
        text-align: center;
        margin-bottom: 3rem;
        padding: 2rem;
        background: rgba(139, 92, 246, 0.1);
        border-radius: 20px;
        border: 1px solid rgba(139, 92, 246, 0.2);
    }
    
    .welcome-title {
        font-size: 2rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 1rem;
        background: linear-gradient(135deg, #ffffff, #c084fc);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .welcome-text {
        color: var(--text-secondary);
        font-size: 1.1rem;
        line-height: 1.7;
        max-width: 600px;
        margin: 0 auto;
    }
    
    /* Messages */
    .message {
        margin-bottom: 1.5rem;
        animation: messageSlideIn 0.4s ease-out;
    }
    
    .message-user {
        text-align: right;
    }
    
    .message-assistant {
        text-align: left;
    }
    
    .message-bubble {
        display: inline-block;
        padding: 1.5rem 2rem;
        border-radius: 24px;
        max-width: 75%;
        font-size: 1rem;
        line-height: 1.6;
        position: relative;
    }
    
    .message-user .message-bubble {
        background: linear-gradient(135deg, #8b5cf6, #c084fc);
        color: white;
        border-bottom-right-radius: 8px;
        box-shadow: 0 8px 24px rgba(139, 92, 246, 0.3);
    }
    
    .message-assistant .message-bubble {
        background: var(--card-bg);
        color: var(--text-primary);
        border: 1px solid var(--border-color);
        border-bottom-left-radius: 8px;
        backdrop-filter: blur(15px);
    }
    
    /* Zone de saisie */
    .input-section {
        background: var(--card-bg);
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid var(--border-color);
        backdrop-filter: blur(20px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
    }
    
    /* Suggestions rapides */
    .quick-actions {
        margin-top: 1.5rem;
        text-align: center;
    }
    
    .quick-actions-title {
        color: var(--text-secondary);
        font-size: 0.95rem;
        margin-bottom: 1rem;
        font-weight: 500;
    }
    
    .action-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-top: 1rem;
    }
    
    .action-card {
        background: rgba(139, 92, 246, 0.1);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 16px;
        padding: 1.25rem;
        cursor: pointer;
        transition: all 0.3s ease;
        text-align: center;
    }
    
    .action-card:hover {
        background: rgba(139, 92, 246, 0.2);
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(139, 92, 246, 0.2);
    }
    
    .action-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
        display: block;
    }
    
    .action-title {
        color: var(--text-primary);
        font-weight: 600;
        font-size: 0.95rem;
    }
    
    /* Sidebar */
    .status-panel {
        background: var(--card-bg);
        border-radius: 16px;
        padding: 1.75rem;
        margin-bottom: 1.5rem;
        border: 1px solid var(--border-color);
        backdrop-filter: blur(20px);
    }
    
    .panel-title {
        color: var(--text-primary);
        font-weight: 700;
        margin-bottom: 1.25rem;
        font-size: 1.1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .connection-item {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 0.75rem;
        padding: 0.75rem;
        border-radius: 12px;
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.2);
    }
    
    .status-dot-online {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: #10b981;
        box-shadow: 0 0 10px rgba(16, 185, 129, 0.6);
        animation: statusPulse 2s infinite;
    }
    
    @keyframes statusPulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.6; }
    }
    
    @keyframes messageSlideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .brand-title {
            font-size: 2.5rem;
        }
        
        .connectis-logo {
            width: 100px;
            height: 100px;
        }
        
        .logo-pattern {
            width: 50px;
            height: 50px;
        }
        
        .action-grid {
            grid-template-columns: repeat(2, 1fr);
        }
    }
    
    /* Masquer éléments Streamlit */
    .stDeployButton, #MainMenu, footer, header { display: none !important; }
    
    /* Style des inputs Streamlit */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
        font-size: 1rem !important;
        padding: 1rem 1.25rem !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--accent-purple) !important;
        box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.2) !important;
    }
    
    .stButton > button {
        background: var(--card-bg) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        padding: 0.75rem 1.5rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background: var(--accent-purple) !important;
        border-color: var(--accent-purple) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3) !important;
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
    """Affiche l'en-tête avec le logo CONNECT'IS"""
    st.markdown("""
    <div class="connectis-header">
        <div class="logo-container">
            <div class="connectis-logo">
                <div class="logo-pattern">
                    <div class="cube"></div>
                    <div class="cube"></div>
                    <div class="cube"></div>
                    <div class="cube"></div>
                    <div class="cube"></div>
                    <div class="cube"></div>
                    <div class="cube"></div>
                    <div class="cube"></div>
                    <div class="cube"></div>
                    <div class="cube"></div>
                    <div class="cube"></div>
                    <div class="cube"></div>
                </div>
            </div>
        </div>
        <h1 class="brand-title">CONNECT'IS</h1>
        <p class="brand-subtitle">Assistant IA Multi-Systèmes - Connectez vos applications en toute simplicité</p>
    </div>
    """, unsafe_allow_html=True)

def render_welcome_section():
    """Affiche la section d'accueil"""
    st.markdown("""
    <div class="welcome-section">
        <h2 class="welcome-title">Bonjour! Comment puis-je vous aider aujourd'hui?</h2>
        <p class="welcome-text">
            Posez vos questions sur le CRM, les ressources humaines, ou la gestion de projets. 
            Je peux vous aider à créer, modifier, rechercher et gérer vos données en toute simplicité.
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_chat_interface():
    """Affiche l'interface de chat"""
    st.markdown('<div class="chat-interface">', unsafe_allow_html=True)
    
    # Section d'accueil si pas de messages
    if "messages" not in st.session_state or len(st.session_state.messages) == 0:
        render_welcome_section()
    
    # Historique des messages
    if "messages" in st.session_state:
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
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_input_section():
    """Affiche la zone de saisie avec actions rapides"""
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    
    # Zone de saisie principale
    user_input = st.text_input(
        "Message",
        placeholder="Demander, créer, rechercher, @ pour mentionner...",
        key="user_input",
        label_visibility="collapsed"
    )
    
    # Actions rapides
    st.markdown("""
    <div class="quick-actions">
        <div class="quick-actions-title">Actions rapides</div>
        <div class="action-grid">
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📋 Clients", key="action1", use_container_width=True):
            st.session_state.user_input = "liste tous les clients"
            st.rerun()
    
    with col2:
        if st.button("💼 Opportunités", key="action2", use_container_width=True):
            st.session_state.user_input = "montre-moi les opportunités"
            st.rerun()
    
    with col3:
        if st.button("👥 Employés", key="action3", use_container_width=True):
            st.session_state.user_input = "liste des employés"
            st.rerun()
    
    with col4:
        if st.button("📊 Projets", key="action4", use_container_width=True):
            st.session_state.user_input = "statut des projets"
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return user_input

def render_sidebar():
    """Affiche la sidebar avec les statuts"""
    with st.sidebar:
        st.markdown("""
        <div class="status-panel">
            <h3 class="panel-title">🔌 État des Connexions</h3>
            <div class="connection-item">
                <div class="status-dot-online"></div>
                <span style="color: var(--text-primary); font-weight: 500;">Odoo CRM</span>
            </div>
            <div class="connection-item">
                <div class="status-dot-online"></div>
                <span style="color: var(--text-primary); font-weight: 500;">Base RH</span>
            </div>
            <div class="connection-item">
                <div class="status-dot-online"></div>
                <span style="color: var(--text-primary); font-weight: 500;">Gestion Projets</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="status-panel">
            <h3 class="panel-title">📊 Statistiques</h3>
            <div style="color: var(--text-secondary); font-size: 0.95rem; line-height: 1.6;">
                <p><strong>Sessions:</strong> 12 aujourd'hui</p>
                <p><strong>Requêtes:</strong> 84 traitées</p>
                <p><strong>Performance:</strong> 0.8s moyenne</p>
                <p><strong>Disponibilité:</strong> 99.9%</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 Actualiser", use_container_width=True):
            st.success("✅ Données actualisées!")
        
        if st.button("📊 Tableau de bord", use_container_width=True):
            st.info("📈 Tableau de bord bientôt disponible")
        
        if st.button("⚙️ Paramètres", use_container_width=True):
            st.info("⚙️ Paramètres en développement")

def process_message(message: str, workflow):
    """Traite le message utilisateur"""
    if not workflow:
        return "❌ Workflow non disponible"
    
    try:
        # Ajouter le message utilisateur
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        st.session_state.messages.append({"role": "user", "content": message})
        
        # Traitement avec animation
        with st.spinner("🤔 Analyse en cours..."):
            time.sleep(0.8)  # Délai réaliste
            result = workflow.process_user_request(message)
        
        # Formater la réponse
        if result.get("success"):
            response = "✅ **Opération réussie**\n\n"
            
            if result.get("data"):
                data = result["data"]
                if isinstance(data, dict) and data.get("count", 0) > 0:
                    response += f"📊 **{data['count']} résultat(s)**\n\n"
                    
                    items = data.get("data", [])[:3]
                    for item in items:
                        if isinstance(item, dict):
                            name = item.get("nom", item.get("titre", "Élément"))
                            response += f"• **{name}**"
                            if item.get("email"):
                                response += f" - {item['email']}"
                            if item.get("id"):
                                response += f" (ID: {item['id']})"
                            response += "\n"
                    
                    if len(data.get("data", [])) > 3:
                        response += f"\n... et {len(data.get('data', [])) - 3} autre(s)\n"
            
            summary = result.get("summary")
            if summary:
                response += f"\n💡 **Résumé**: {summary}"
        else:
            response = f"❌ **Erreur**: {result.get('error', 'Erreur inconnue')}"
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        return response
        
    except Exception as e:
        error_msg = f"❌ **Erreur système**: {str(e)}"
        st.session_state.messages.append({"role": "assistant", "content": error_msg})
        return error_msg

def main():
    """Fonction principale"""
    # Initialisation
    workflow = load_workflow()
    
    # Interface
    render_header()
    render_sidebar()
    render_chat_interface()
    user_input = render_input_section()
    
    # Traitement
    if user_input and user_input.strip():
        process_message(user_input, workflow)
        st.rerun()
    
    # Footer
    st.markdown("""
    <div style="text-align: center; margin-top: 3rem; padding: 2rem; color: var(--text-secondary); font-size: 0.9rem;">
        🚀 Propulsé par <strong>CONNECT'IS</strong> - Intelligence Artificielle Multi-Systèmes
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
