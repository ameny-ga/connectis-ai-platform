"""
Configuration centrale du projet LangGraph Multi-Agents
"""

import os
from pathlib import Path

# Chemins du projet
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
SRC_DIR = PROJECT_ROOT / "src"

# Configuration des agents
AGENT_CONFIG = {
    "interface_agent": {
        "name": "Agent Interface",
        "description": "Convertit les prompts utilisateurs en instructions JSON structurées",
        "model": "gpt-3.5-turbo"  # Peut être changé selon les besoins
    },
    "systems_agent": {
        "name": "Agent Systèmes", 
        "description": "Exécute les instructions sur les systèmes fictifs",
        "supported_systems": ["CRM", "RH", "PROJETS"]
    }
}

# Configuration des systèmes fictifs
SYSTEMS_CONFIG = {
    "CRM": {
        "data_file": DATA_DIR / "crm_data.json",
        "operations": ["lister_clients", "rechercher_client", "ajouter_client", "modifier_client"]
    },
    "RH": {
        "data_file": DATA_DIR / "hr_data.json", 
        "operations": ["lister_employes", "rechercher_employe", "gerer_conges", "evaluations"]
    },
    "PROJETS": {
        "data_file": DATA_DIR / "projects_data.json",
        "operations": ["lister_projets", "statut_projet", "gerer_taches", "rapports"]
    }
}
