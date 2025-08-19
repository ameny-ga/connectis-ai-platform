"""
Script de lancement de l'application LangGraph Multi-Agents
"""

import os
import sys
from pathlib import Path

# Configuration du projet
PROJECT_ROOT = Path(__file__).parent
STREAMLIT_APP = PROJECT_ROOT / "src" / "interface" / "app.py"

def launch_app():
    """Lance l'application Streamlit"""
    print("🚀 Lancement de l'application LangGraph Multi-Agents...")
    print(f"📁 Répertoire: {PROJECT_ROOT}")
    print(f"🌐 Interface: {STREAMLIT_APP}")
    print("\n" + "="*50)
    print("💡 L'application va s'ouvrir dans votre navigateur")
    print("🔗 URL locale: http://localhost:8501")
    print("🛑 Pour arrêter: Ctrl+C dans ce terminal")
    print("="*50 + "\n")
    
    # Lancement de Streamlit
    os.system(f"streamlit run {STREAMLIT_APP}")

if __name__ == "__main__":
    launch_app()
