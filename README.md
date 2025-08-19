# 🤖 LangGraph Multi-Agents - Projet Académique

## 📋 Description
Système de simulation d'unification de systèmes d'information utilisant **LangGraph** pour orchestrer des agents intelligents. Ce projet démontre l'intégration de différents systèmes (CRM, RH, gestion de projets) via une interface en langage naturel.

## 🏗️ Architecture

### Agents Implémentés
- **🧠 Agent Interface** : Convertit les prompts utilisateurs en instructions JSON structurées
- **⚙️ Agent Systèmes** : Exécute les instructions sur des systèmes fictifs (CRM, RH, gestion de projets)
- **🔄 LangGraph Workflow** : Orchestration intelligente entre les agents
- **🖥️ Interface Streamlit** : Interface utilisateur conviviale

### Systèmes Simulés
- **CRM** : Gestion clients, opportunités commerciales
- **RH** : Employés, congés, évaluations
- **PROJETS** : Gestion de projets, tâches, jalons

## 🚀 Démarrage Rapide

### 1. Installation
```bash
# Cloner le projet
git clone <votre-repo>
cd v0

# Installer les dépendances (environnement virtuel déjà configuré)
pip install -r requirements.txt
```

### 2. Lancer l'Application
```bash
# Option 1: Script de lancement automatique
python run_app.py

# Option 2: Streamlit direct
streamlit run src/interface/app.py
```

### 3. Tester le Système
```bash
# Exécuter tous les scénarios de test
python tests/test_scenarios.py

# Tester le workflow directement
python src/workflows/multi_agent_workflow.py

# Tester les agents individuellement
python src/agents/interface_agent.py
python src/agents/systems_agent.py
```

## 📊 Résultats des Tests

**Taux de succès global : 92.3%** (12/13 tests réussis)

| Système | Tests Réussis | Taux |
|---------|---------------|------|
| CRM     | 5/5          | 100% ✅ |
| RH      | 5/5          | 100% ✅ |
| PROJETS | 2/3          | 67%  ⚠️ |

## 💡 Exemples d'Utilisation

### Requêtes Supportées
```
🔵 CRM
• "Montre-moi tous les clients"
• "Cherche le client TechnoPlus"
• "Statut des opportunités commerciales"
• "Ajoute un nouveau client nommé NouvelleEntreprise"

🔵 RH
• "Liste tous les employés"
• "Trouve l'employé Dubois"
• "Quel est le statut des congés?"
• "Génère un rapport RH complet"

🔵 PROJETS
• "Affiche tous les projets"
• "Statut du projet P001"
• "Progression de tous les projets"
```

## 📁 Structure du Projet
```
v0/
├── 📁 src/
│   ├── 📁 agents/          # Agents LangGraph
│   │   ├── interface_agent.py
│   │   └── systems_agent.py
│   ├── 📁 workflows/       # Orchestration LangGraph
│   │   └── multi_agent_workflow.py
│   └── 📁 interface/       # Interface Streamlit
│       └── app.py
├── 📁 data/               # Données JSON mockées
│   ├── crm_data.json     # 3 clients, 2 opportunités
│   ├── hr_data.json      # 5 employés, congés, évaluations
│   └── projects_data.json # 3 projets, tâches, jalons
├── 📁 tests/              # Tests et validation
│   ├── test_scenarios.py
│   └── test_report.json
├── config.py              # Configuration centrale
├── requirements.txt       # Dépendances Python
├── run_app.py            # Script de lancement
└── README.md             # Ce fichier
```

## 🛠️ Technologies Utilisées
- **Python 3.13** - Langage principal
- **LangGraph 0.0.26** - Orchestration multi-agents
- **LangChain 0.1.0** - Framework IA
- **Streamlit 1.29.0** - Interface utilisateur
- **Pydantic 2.5.0** - Validation des données
- **JSON** - Stockage des données mockées

## ⚡ Fonctionnalités Clés

### 🔍 Intelligence de Parsing
- Détection automatique du système cible (CRM/RH/PROJETS)
- Analyse d'intention (lister, rechercher, ajouter, statut, rapport)
- Extraction automatique des paramètres

### 🔄 Workflow LangGraph
- Pipeline orchestré : Interface → Systèmes → Formatter
- Gestion d'erreurs robuste
- Log d'exécution détaillé

### 📊 Interface Complète
- Saisie en langage naturel
- Affichage formaté des résultats
- Historique des requêtes
- Statistiques d'utilisation
- Exemples intégrés

## 🎯 Objectifs Pédagogiques Atteints

✅ **Prototypage Rapide** : Développé en 2 jours  
✅ **Code Propre** : Documentation, tests, structure modulaire  
✅ **LangGraph** : Workflow multi-agents fonctionnel  
✅ **Données Réalistes** : JSON mockés complets  
✅ **Interface Utilisateur** : Streamlit intuitif  
✅ **Tests Automatisés** : 13 scénarios de validation  

## 🔧 Développement Futur

### Améliorations Possibles
- [ ] Détection plus fine des paramètres dans les prompts
- [ ] Support de requêtes multi-systèmes
- [ ] Ajout d'un agent de synthèse pour les rapports croisés
- [ ] Intégration d'un vrai LLM (OpenAI, Anthropic)
- [ ] Persistance des données (base de données)
- [ ] API REST pour intégration externe

### Corrections Identifiées
- [ ] Améliorer la détection "statut projet spécifique" vs "progression globale"
- [ ] Enrichir les patterns de détection des noms propres
- [ ] Ajouter la validation des données d'entrée

## 🎓 Usage Académique
Ce projet est conçu comme **prototype éducatif** pour démontrer :
- L'orchestration d'agents avec LangGraph
- L'analyse de langage naturel avec des règles
- La simulation de systèmes d'information
- Le développement rapide d'interfaces utilisateur

---
*Développé avec ❤️ pour l'apprentissage de LangGraph et des systèmes multi-agents*
