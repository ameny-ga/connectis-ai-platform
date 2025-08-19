"""
Interface Streamlit pour le système LangGraph Multi-Agents
"""

import streamlit as st
import sys
import os
import json
from datetime import datetime

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.workflows.multi_agent_workflow import MultiAgentWorkflow


# Configuration de la page Streamlit sans sidebar
st.set_page_config(
    page_title="🔗 Connect'IS",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personnalisé pour un design moderne en bleu et blanc
st.markdown("""
<style>
    /* Masquer complètement la sidebar */
    .css-1d391kg, .css-1lcbmhc, .css-1outpf7, section[data-testid="stSidebar"] {
        display: none !important;
        width: 0 !important;
    }
    
    /* Arrière-plan général blanc */
    .main {
        background-color: white;
    }
    
    .block-container {
        background-color: white;
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
    
    /* FORCER TOUS LES TEXTES À ÊTRE VISIBLES (NOIR/FONCÉ) */
    .stMarkdown, .stMarkdown p, .stMarkdown div, .stText, p, div, span, 
    .result-card, .result-card *, .detail-item, .detail-item *,
    [data-testid="stMarkdownContainer"], [data-testid="stMarkdownContainer"] *,
    .element-container, .element-container * {
        color: #1f2937 !important;
    }
    
    /* Titres en bleu foncé */
    h1, h2, h3, h4, h5, h6 {
        color: #1e3a8a !important;
    }
    
    /* Forcer le contraste dans les cartes de résultats */
    .result-card h4, .result-card strong, .result-card b {
        color: #1e3a8a !important;
    }
    
    /* Texte des détails */
    .detail-item, .detail-item *, .detail-item strong {
        color: #374151 !important;
    }
    
    /* Cartes pour les résultats */
    .result-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid #e5e7eb;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    
    .result-card:hover {
        border-color: #3b82f6;
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.15);
        transform: translateY(-2px);
    }
    
    /* Messages de succès */
    .success-message {
        background: linear-gradient(90deg, #ecfdf5 0%, #f0fdf4 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #10b981;
        color: #065f46;
        margin: 1rem 0;
    }
    
    /* Messages d'erreur */
    .error-message {
        background: linear-gradient(90deg, #fef2f2 0%, #fef7f7 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #ef4444;
        color: #991b1b;
        margin: 1rem 0;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f8fafc;
    }
    
    /* Boutons personnalisés */
    .stButton > button {
        background: linear-gradient(90deg, #1e40af 0%, #3b82f6 100%);
        color: white;
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
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    /* Métriques styling */
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e5e7eb;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    /* Items de détail */
    .detail-item {
        background: #f8fafc;
        padding: 0.8rem;
        border-radius: 6px;
        margin: 0.5rem 0;
        border-left: 3px solid #3b82f6;
    }
    
    /* Cache le menu Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
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


def display_sidebar():
    """Affiche la barre latérale avec les informations"""
    with st.sidebar:
        st.markdown("### � Tableau de Bord Connect'IS")
        
        # Informations sur le workflow
        workflow_info = st.session_state.workflow.get_workflow_info()
        
        st.markdown("#### 🤖 Agents Intelligents")
        for agent in workflow_info["agents"]:
            st.markdown(f"• **{agent}**")
        
        st.markdown("#### 🏢 Systèmes Connectés")
        system_icons = {"CRM": "💼", "RH": "👥", "PROJETS": "📋"}
        for system in workflow_info["systems"]:
            icon = system_icons.get(system, "⚙️")
            st.markdown(f"• {icon} **{system}**")
            
        st.markdown("#### 💡 Exemples de Requêtes")
        examples = [
            "📋 Montre-moi tous les clients",
            "💰 Liste des opportunités",
            "📊 Statut du projet P001",
            "👤 Cherche l'employé Dubois",
            "📈 Rapport sur les congés"
        ]
        
        for example in examples:
            if st.button(f"📝 {example}", key=f"example_{example}"):
                st.session_state.example_query = example


def display_main_interface():
    """Interface principale de saisie et résultats"""
    st.markdown("### 💬 Interface de Requête Intelligente")
    
    # Zone de saisie avec design amélioré
    col1, col2 = st.columns([4, 1])
    
    with col1:
        # Utiliser l'exemple si sélectionné
        default_query = st.session_state.get('example_query', '')
        user_input = st.text_input(
            "Posez votre question en langage naturel :",
            value=default_query,
            placeholder="Ex: Montre-moi tous les clients actifs ou Liste des opportunités",
            key="user_input"
        )
        
        # Réinitialiser l'exemple après utilisation
        if 'example_query' in st.session_state:
            del st.session_state.example_query
    
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
    title = result_data.get("title", "Résultat")
    summary = result_data.get("summary", "")
    count = result_data.get("count", 0)
    data = result_data.get("data", [])
    metrics = result_data.get("metrics", {})
    
    # En-tête du résultat
    st.markdown(f"#### {title}")
    
    if summary:
        st.info(f"📋 {summary}")
    
    # Affichage des métriques s'il y en a
    if metrics:
        st.markdown("##### 📈 Indicateurs Clés")
        
        # Créer des colonnes pour les métriques
        metric_cols = st.columns(min(len(metrics), 4))
        for i, (key, value) in enumerate(metrics.items()):
            with metric_cols[i % 4]:
                # Formatage intelligent des métriques
                if isinstance(value, (int, float)):
                    if "budget" in key.lower() or "valeur" in key.lower():
                        formatted_value = f"{value:,}€".replace(",", " ")
                    elif "pourcentage" in key.lower() or "progression" in key.lower():
                        formatted_value = f"{value}%"
                    else:
                        formatted_value = str(value)
                else:
                    formatted_value = str(value)
                
                metric_name = key.replace('_', ' ').title()
                st.metric(metric_name, formatted_value)
    
    # Affichage des données détaillées
    if isinstance(data, list) and len(data) > 0:
        st.markdown("##### 📝 Détails")
        
        # Déterminer le type de données pour un affichage adapté
        system = result.get("result", {}).get("system", "")
        
        if system == "CRM":
            display_crm_data(data, result_data.get("title", ""))
        elif system == "RH":
            display_hr_data(data, result_data.get("title", ""))
        elif system == "PROJETS":
            display_projects_data(data, result_data.get("title", ""))
        else:
            # Affichage générique pour les autres cas
            display_generic_data(data)
    
    elif count == 0:
        st.warning("🔍 Aucun résultat trouvé pour cette recherche.")


def display_crm_data(data, title):
    """Affichage spécialisé pour les données CRM"""
    if "client" in title.lower():
        for client in data:
            with st.container():
                st.markdown(f"""
                <div class="result-card">
                    <h4>🏢 {client.get('nom', 'Client inconnu')}</h4>
                    <div class="detail-item">
                        <strong>👤 Contact :</strong> {client.get('contact', 'N/A')} | 
                        <strong>📧 Email :</strong> {client.get('email', 'N/A')}
                    </div>
                    <div class="detail-item">
                        <strong>🏭 Secteur :</strong> {client.get('secteur', 'N/A')} | 
                        <strong>📊 Statut :</strong> <span style="color: {'green' if client.get('statut') == 'Actif' else 'orange'}">{client.get('statut', 'N/A')}</span>
                    </div>
                    <div class="detail-item">
                        <strong>💰 Chiffre d'affaires :</strong> {client.get('chiffre_affaires', 0):,}€ | 
                        <strong>📅 Dernière interaction :</strong> {client.get('derniere_interaction', 'N/A')}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
    elif "opportunité" in title.lower():
        for opp in data:
            with st.container():
                st.markdown(f"""
                <div class="result-card">
                    <h4>💼 {opp.get('titre', 'Opportunité inconnue')}</h4>
                    <div class="detail-item">
                        <strong>💰 Valeur :</strong> {opp.get('valeur', 0):,}€ | 
                        <strong>🎯 Probabilité :</strong> {opp.get('probabilite', 0)}%
                    </div>
                    <div class="detail-item">
                        <strong>📈 Étape :</strong> {opp.get('etape', 'N/A')} | 
                        <strong>🏢 Client :</strong> {opp.get('client_id', 'N/A')}
                    </div>
                    <div class="detail-item">
                        <strong>📅 Création :</strong> {opp.get('date_creation', 'N/A')} | 
                        <strong>🎯 Clôture prévue :</strong> {opp.get('date_cloture_prevue', 'N/A')}
                    </div>
                </div>
                """, unsafe_allow_html=True)


def display_hr_data(data, title):
    """Affichage spécialisé pour les données RH"""
    if "employé" in title.lower():
        for emp in data:
            with st.container():
                st.markdown(f"""
                <div class="result-card">
                    <h4>👤 {emp.get('prenom', '')} {emp.get('nom', 'Employé inconnu')}</h4>
                    <div class="detail-item">
                        <strong>💼 Poste :</strong> {emp.get('poste', 'N/A')} | 
                        <strong>🏢 Département :</strong> {emp.get('departement', 'N/A')}
                    </div>
                    <div class="detail-item">
                        <strong>📧 Email :</strong> {emp.get('email', 'N/A')} | 
                        <strong>📅 Embauche :</strong> {emp.get('date_embauche', 'N/A')}
                    </div>
                    <div class="detail-item">
                        <strong>💰 Salaire :</strong> {emp.get('salaire', 0):,}€ | 
                        <strong>📊 Statut :</strong> <span style="color: {'green' if emp.get('statut') == 'Actif' else 'red'}">{emp.get('statut', 'N/A')}</span>
                    </div>
                    {f'<div class="detail-item"><strong>🎯 Compétences :</strong> {", ".join(emp.get("competences", []))}</div>' if emp.get("competences") else ''}
                </div>
                """, unsafe_allow_html=True)
                
    elif "congé" in title.lower():
        for conge in data:
            with st.container():
                st.markdown(f"""
                <div class="result-card">
                    <h4>🏖️ Congés - {conge.get('employe_id', 'N/A')}</h4>
                    <div class="detail-item">
                        <strong>📋 Type :</strong> {conge.get('type', 'N/A')} | 
                        <strong>📊 Statut :</strong> <span style="color: {'green' if conge.get('statut') == 'Approuvé' else 'orange'}">{conge.get('statut', 'N/A')}</span>
                    </div>
                    <div class="detail-item">
                        <strong>📅 Période :</strong> du {conge.get('date_debut', 'N/A')} au {conge.get('date_fin', 'N/A')} | 
                        <strong>📊 Durée :</strong> {conge.get('nb_jours', 0)} jours
                    </div>
                </div>
                """, unsafe_allow_html=True)


def display_projects_data(data, title):
    """Affichage spécialisé pour les données Projets"""
    for projet in data:
        status_color = {
            "En cours": "blue",
            "Terminé": "green", 
            "Planifié": "orange"
        }.get(projet.get('statut', ''), "gray")
        
        with st.container():
            st.markdown(f"""
            <div class="result-card">
                <h4>📋 {projet.get('nom', 'Projet inconnu')}</h4>
                <div class="detail-item">
                    <strong>📝 Description :</strong> {projet.get('description', 'N/A')}
                </div>
                <div class="detail-item">
                    <strong>📊 Statut :</strong> <span style="color: {status_color}">{projet.get('statut', 'N/A')}</span> | 
                    <strong>⚡ Priorité :</strong> {projet.get('priorite', 'N/A')} | 
                    <strong>📈 Progression :</strong> {projet.get('progression', 0)}%
                </div>
                <div class="detail-item">
                    <strong>💰 Budget :</strong> {projet.get('budget_consomme', 0):,}€ / {projet.get('budget', 0):,}€ | 
                    <strong>👥 Chef de projet :</strong> {projet.get('chef_projet', 'N/A')}
                </div>
                <div class="detail-item">
                    <strong>📅 Début :</strong> {projet.get('date_debut', 'N/A')} | 
                    <strong>🎯 Fin prévue :</strong> {projet.get('date_fin_prevue', 'N/A')}
                </div>
                {f'<div class="detail-item"><strong>👥 Équipe :</strong> {", ".join(projet.get("equipe", []))}</div>' if projet.get("equipe") else ''}
            </div>
            """, unsafe_allow_html=True)


def display_generic_data(data):
    """Affichage générique pour les autres types de données"""
    for i, item in enumerate(data[:5]):  # Limiter à 5 éléments
        if isinstance(item, dict):
            with st.expander(f"📄 Élément {i+1}"):
                for key, value in item.items():
                    st.write(f"**{key.replace('_', ' ').title()}:** {value}")
        else:
            st.write(f"• {item}")


def display_history():
    """Affiche l'historique des requêtes"""
    if st.session_state.history:
        st.header("📚 Historique des Requêtes")
        
        # Options d'affichage
        col1, col2 = st.columns([3, 1])
        with col1:
            show_details = st.checkbox("Afficher les détails techniques")
        with col2:
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
                    
                    if show_details and entry['result'].get('instruction'):
                        st.json(entry['result']['instruction'])
                else:
                    st.markdown("**Statut:** ❌ Erreur")
                    st.error(entry['result'].get('error', 'Erreur inconnue'))


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
    <div style="text-align: center; color: #64748b; padding: 1.5rem; background: #f8fafc; border-radius: 8px; margin-top: 2rem;">
        🔗 <strong>Connect'IS</strong> - Plateforme d'unification intelligente des systèmes d'information<br>
        <small>Propulsé par LangGraph, LangChain et Streamlit | © 2025</small>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
