"""
Interface Streamlit pour le système LangGraph Multi-Agents - Connect'IS
"""

import streamlit as st
import sys
import os
import json
from datetime import datetime

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.workflows.multi_agent_workflow import MultiAgentWorkflow

# Configuration de la page Streamlit
st.set_page_config(
    page_title="🔗 Connect'IS",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personnalisé pour Connect'IS avec textes visibles
st.markdown("""
<style>
    /* Masquer complètement la sidebar */
    .css-1d391kg, .css-1lcbmhc, .css-1outpf7, section[data-testid="stSidebar"] {
        display: none !important;
        width: 0 !important;
    }
    
    /* Arrière-plan général blanc */
    .main, .stApp {
        background-color: white !important;
    }
    
    .block-container {
        background-color: white !important;
        padding-top: 2rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 100%;
    }
    
    /* En-tête principal avec dégradé bleu */
    .main-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #60a5fa 100%);
        padding: 2.5rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(59, 130, 246, 0.3);
        text-align: center;
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        color: white !important;
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
        margin: 0;
        color: #e1e7ff !important;
    }
    
    /* FORCER TOUS LES TEXTES À ÊTRE VISIBLES - CONTRASTE MAXIMUM */
    .stMarkdown, .stMarkdown p, .stMarkdown div, .stText, p, div, span,
    [data-testid="stMarkdownContainer"], [data-testid="stMarkdownContainer"] *,
    .element-container, .element-container *,
    .css-1dp5vir, .css-1dp5vir * {
        color: #111827 !important;
    }
    
    /* Titres en bleu foncé avec contraste élevé */
    h1, h2, h3, h4, h5, h6 {
        color: #1e3a8a !important;
        font-weight: 600 !important;
    }
    
    /* Cartes pour les résultats avec texte bien visible */
    .result-card {
        background: white !important;
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid #e5e7eb;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    
    .result-card * {
        color: #111827 !important;
    }
    
    .result-card h4 {
        color: #1e3a8a !important;
        margin-bottom: 1rem;
    }
    
    .result-card:hover {
        border-color: #3b82f6;
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.15);
        transform: translateY(-2px);
    }
    
    /* Items de détail avec contraste élevé */
    .detail-item {
        background: #f8fafc !important;
        padding: 0.8rem;
        border-radius: 6px;
        margin: 0.5rem 0;
        border-left: 3px solid #3b82f6;
    }
    
    .detail-item * {
        color: #374151 !important;
    }
    
    .detail-item strong {
        color: #1f2937 !important;
    }
    
    /* Messages de succès */
    .success-message {
        background: linear-gradient(90deg, #ecfdf5 0%, #f0fdf4 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #10b981;
        color: #065f46 !important;
        margin: 1rem 0;
    }
    
    .success-message * {
        color: #065f46 !important;
    }
    
    /* Messages d'erreur */
    .error-message {
        background: linear-gradient(90deg, #fef2f2 0%, #fef7f7 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #ef4444;
        color: #991b1b !important;
        margin: 1rem 0;
    }
    
    .error-message * {
        color: #991b1b !important;
    }
    
    /* Boutons personnalisés */
    .stButton > button {
        background: linear-gradient(90deg, #1e40af 0%, #3b82f6 100%);
        color: white !important;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #1e3a8a 0%, #2563eb 100%);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 2px solid #e5e7eb;
        transition: border-color 0.3s ease;
        color: white !important;
        background-color: #374151 !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    /* Cache le menu Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Force les couleurs dans les onglets */
    .stTabs [data-baseweb="tab-list"] {
        background-color: white !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #374151 !important;
    }
    
    .stTabs [aria-selected="true"] {
        color: #1e3a8a !important;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialise l'état de session Streamlit"""
    if 'workflow' not in st.session_state:
        st.session_state.workflow = MultiAgentWorkflow()
    if 'history' not in st.session_state:
        st.session_state.history = []

def display_header():
    """Affiche l'en-tête de l'application"""
    st.markdown("""
    <div class="main-header">
        <h1>🔗 Connect'IS</h1>
        <p>Plateforme d'unification intelligente des systèmes d'information</p>
    </div>
    """, unsafe_allow_html=True)

def display_main_interface():
    """Interface principale de saisie et résultats"""
    st.markdown("### 💬 Interface de Requête Intelligente")
    
    # Zone de saisie avec design amélioré
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input(
            "Posez votre question en langage naturel :",
            placeholder="Ex: Montre-moi tous les clients actifs ou Liste des opportunités",
            key="user_input"
        )
    
    with col2:
        st.write("")  # Espacement
        process_button = st.button("🚀 Analyser", type="primary")
    
    # Traitement de la requête
    if process_button and user_input:
        with st.spinner("🔄 Analyse en cours..."):
            result = st.session_state.workflow.process_user_request(user_input)
            
            # Ajouter à l'historique
            st.session_state.history.append({
                "timestamp": datetime.now(),
                "query": user_input,
                "result": result
            })
            
            # Affichage du résultat
            display_result(result)
    
    elif process_button and not user_input:
        st.warning("⚠️ Veuillez saisir une requête.")

def display_result(result):
    """Affiche le résultat d'une requête de manière attractive"""
    st.markdown("### 📊 Résultats")
    
    if result["success"]:
        # Résultat réussi avec design moderne
        st.markdown(f"""
        <div class="success-message">
            <h4>✅ Requête traitée avec succès</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Affichage enrichi du résultat
        display_enhanced_result(result)
        
    else:
        # Erreur avec design moderne
        st.markdown(f"""
        <div class="error-message">
            <h4>❌ Erreur lors du traitement</h4>
            <p><strong>Détails :</strong> {result.get("error", "Erreur inconnue")}</p>
        </div>
        """, unsafe_allow_html=True)

def display_enhanced_result(result):
    """Affiche les résultats de manière enrichie et compréhensible"""
    result_data = result.get("result", {}).get("result", {}) if result.get("result") else {}
    instruction = result.get("instruction", {})
    
    # Extraction des informations clés
    title = result_data.get("title", "Résultat")
    summary = result_data.get("summary", "")
    count = result_data.get("count", 0)
    data = result_data.get("data", [])
    metrics = result_data.get("metrics", {})
    system = instruction.get("system", "")
    
    # Titre avec icône selon le système
    system_icons = {"CRM": "👥", "RH": "🏢", "PROJETS": "📋"}
    icon = system_icons.get(system, "📊")
    
    st.markdown(f"""
    <div style="background: linear-gradient(145deg, #f0f9ff 0%, #e0f2fe 100%); 
                padding: 1.5rem; border-radius: 12px; border-left: 5px solid #0284c7; 
                margin: 1rem 0;">
        <h3 style="color: #0c4a6e !important; margin: 0 0 1rem 0;">{icon} {title}</h3>
        <p style="color: #0369a1 !important; font-size: 1.1rem; margin: 0;">{summary}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Métriques si disponibles
    if metrics:
        st.markdown("#### 📈 Métriques clés")
        cols = st.columns(min(len(metrics), 4))
        for i, (key, value) in enumerate(metrics.items()):
            with cols[i % 4]:
                metric_name = key.replace('_', ' ').title()
                st.metric(metric_name, value)
    
    # Données détaillées selon le type
    if isinstance(data, list) and len(data) > 0:
        st.markdown("#### 📝 Données détaillées")
        
        if system == "CRM":
            display_crm_data(data)
        elif system == "RH":
            display_hr_data(data)
        elif system == "PROJETS":
            display_project_data(data)
        else:
            display_generic_data(data)

def display_crm_data(data):
    """Affichage spécialisé pour les données CRM"""
    for item in data:
        if "nom" in item:  # Client
            # Affichage de l'ID si disponible
            id_display = f" (ID: {item.get('id', 'N/A')})" if item.get('id') else ""
            st.markdown(f"""
            <div class="result-card">
                <h4>🏢 {item.get('nom', 'N/A')}{id_display}</h4>
                <div class="detail-item">
                    <strong>📧 Email:</strong> {item.get('email', 'N/A')}
                </div>
                <div class="detail-item">
                    <strong>📞 Téléphone:</strong> {item.get('telephone', 'N/A')}
                </div>
                <div class="detail-item">
                    <strong>🏢 Type:</strong> {'Entreprise' if item.get('est_entreprise', False) else 'Particulier'}
                </div>
                <div class="detail-item">
                    <strong>🆔 ID pour suppression:</strong> <span style="background: #fef3c7; padding: 2px 6px; border-radius: 4px; font-family: monospace; font-weight: bold;">{item.get('id', 'N/A')}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        elif "titre" in item:  # Opportunité
            id_display = f" (ID: {item.get('id', 'N/A')})" if item.get('id') else ""
            st.markdown(f"""
            <div class="result-card">
                <h4>💼 {item.get('titre', 'N/A')}{id_display}</h4>
                <div class="detail-item">
                    <strong>💰 Valeur:</strong> {item.get('valeur', 0):,}€ | <strong>📊 Probabilité:</strong> {item.get('probabilite', 0)}%
                </div>
                <div class="detail-item">
                    <strong>📈 Étape:</strong> {item.get('etape', 'N/A')}
                </div>
                <div class="detail-item">
                    <strong>🆔 ID pour suppression:</strong> <span style="background: #fef3c7; padding: 2px 6px; border-radius: 4px; font-family: monospace; font-weight: bold;">{item.get('id', 'N/A')}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

def display_hr_data(data):
    """Affichage spécialisé pour les données RH"""
    for item in data:
        if "prenom" in item:  # Employé
            st.markdown(f"""
            <div class="result-card">
                <h4>👤 {item.get('prenom', '')} {item.get('nom', 'N/A')}</h4>
                <div class="detail-item">
                    <strong>💼 Poste:</strong> {item.get('poste', 'N/A')} - {item.get('departement', 'N/A')}
                </div>
                <div class="detail-item">
                    <strong>📧 Email:</strong> {item.get('email', 'N/A')} | <strong>💰 Salaire:</strong> {item.get('salaire', 0):,}€
                </div>
            </div>
            """, unsafe_allow_html=True)
        elif "type" in item:  # Congé
            st.markdown(f"""
            <div class="result-card">
                <h4>🏖️ {item.get('type', 'N/A')}</h4>
                <div class="detail-item">
                    <strong>📅 Période:</strong> Du {item.get('date_debut', 'N/A')} au {item.get('date_fin', 'N/A')}
                </div>
                <div class="detail-item">
                    <strong>🔖 Statut:</strong> {item.get('statut', 'N/A')} | <strong>⏱️ Durée:</strong> {item.get('nb_jours', 0)} jour(s)
                </div>
            </div>
            """, unsafe_allow_html=True)

def display_project_data(data):
    """Affichage spécialisé pour les données Projets"""
    for item in data:
        if "nom" in item:  # Projet
            progress = item.get('progression', 0)
            st.markdown(f"""
            <div class="result-card">
                <h4>📋 {item.get('nom', 'N/A')}</h4>
                <div class="detail-item">
                    <strong>📊 Progression:</strong> {progress}% | <strong>🎯 Statut:</strong> {item.get('statut', 'N/A')}
                </div>
                <div class="detail-item">
                    <strong>💰 Budget:</strong> {item.get('budget_consomme', 0):,}€ / {item.get('budget', 0):,}€
                </div>
                <div class="detail-item">
                    <strong>📅 Échéance:</strong> {item.get('date_fin_prevue', 'N/A')}
                </div>
            </div>
            """, unsafe_allow_html=True)
        elif "titre" in item:  # Tâche
            st.markdown(f"""
            <div class="result-card">
                <h4>✅ {item.get('titre', 'N/A')}</h4>
                <div class="detail-item">
                    <strong>👤 Assigné à:</strong> {item.get('assignee', 'N/A')} | <strong>🔖 Statut:</strong> {item.get('statut', 'N/A')}
                </div>
                <div class="detail-item">
                    <strong>⏱️ Temps:</strong> {item.get('temps_passe', 0)}h / {item.get('estimation', 0)}h estimées
                </div>
            </div>
            """, unsafe_allow_html=True)

def display_generic_data(data):
    """Affichage générique pour les autres types de données"""
    for i, item in enumerate(data[:5]):  # Limiter à 5 éléments
        if isinstance(item, dict):
            name = item.get("nom", item.get("titre", item.get("id", f"Élément {i+1}")))
            st.markdown(f"""
            <div class="result-card">
                <h4>📄 {name}</h4>
            </div>
            """, unsafe_allow_html=True)
    
    if len(data) > 5:
        st.info(f"... et {len(data) - 5} élément(s) supplémentaire(s)")

def display_history():
    """Affiche l'historique des requêtes"""
    if st.session_state.history:
        st.header("📚 Historique des Requêtes")
        
        # Option pour vider l'historique
        if st.button("🗑️ Vider l'historique"):
            st.session_state.history = []
            st.rerun()
        
        # Affichage de l'historique (plus récent en premier)
        for i, entry in enumerate(reversed(st.session_state.history)):
            with st.expander(f"🕐 {entry['timestamp'].strftime('%H:%M:%S')} - {entry['query'][:50]}..."):
                st.markdown(f"**Requête:** {entry['query']}")
                
                if entry['result']['success']:
                    st.markdown("**Statut:** ✅ Succès")
                    st.markdown("**Réponse:**")
                    st.markdown(entry['result']['formatted_response'])
                else:
                    st.markdown("**Statut:** ❌ Erreur")
                    st.error(entry['result'].get('error', 'Erreur inconnue'))
    else:
        st.info("📝 Aucune requête dans l'historique")

def display_statistics():
    """Affiche des statistiques d'utilisation"""
    if st.session_state.history:
        st.header("📈 Statistiques d'Utilisation")
        
        total_queries = len(st.session_state.history)
        successful_queries = sum(1 for entry in st.session_state.history if entry['result']['success'])
        success_rate = (successful_queries / total_queries) * 100 if total_queries > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📊 Total Requêtes", total_queries)
        
        with col2:
            st.metric("✅ Requêtes Réussies", successful_queries)
        
        with col3:
            st.metric("📈 Taux de Succès", f"{success_rate:.1f}%")
        
        # Répartition par système
        systems_count = {}
        for entry in st.session_state.history:
            if entry['result']['success'] and entry['result'].get('instruction'):
                system = entry['result']['instruction'].get('system', 'Inconnu')
                systems_count[system] = systems_count.get(system, 0) + 1
        
        if systems_count:
            st.subheader("📊 Répartition par Système")
            for system, count in systems_count.items():
                st.markdown(f"• **{system}**: {count} requête(s)")
    else:
        st.info("📊 Aucune statistique disponible")

def main():
    """Fonction principale de l'application Streamlit"""
    initialize_session_state()
    display_header()
    
    # Onglets principaux
    tab1, tab2, tab3 = st.tabs(["💬 Requêtes", "📚 Historique", "📈 Analytics"])
    
    with tab1:
        display_main_interface()
    
    with tab2:
        display_history()
    
    with tab3:
        display_statistics()
    
    # Footer moderne
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #64748b !important; padding: 1.5rem; background: #f8fafc; border-radius: 8px; margin-top: 2rem;">
        🔗 <strong style="color: #1e3a8a !important;">Connect'IS</strong> - Plateforme d'unification intelligente des systèmes d'information<br>
        <small style="color: #64748b !important;">Propulsé par LangGraph, LangChain et Streamlit | © 2025</small>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
