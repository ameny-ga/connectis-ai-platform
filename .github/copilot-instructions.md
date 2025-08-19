# Projet LangGraph Multi-Agents

## Description
Système multi-agents utilisant LangGraph pour simuler l'unification de systèmes d'information (CRM, RH, gestion de projets).

## Architecture
- **Agent Interface** : Analyse les prompts utilisateurs et les convertit en JSON structuré
- **Agent Systèmes** : Exécute les instructions sur des systèmes fictifs (données JSON mockées)
- **LangGraph** : Orchestration du workflow entre les agents
- **Interface Streamlit** : Interface utilisateur pour les tests

## Structure du projet
- `src/agents/` : Implémentation des agents (Interface + Systèmes)
- `src/workflows/` : Workflow LangGraph orchestrant les agents
- `src/interface/` : Interface utilisateur Streamlit
- `data/` : Données JSON mockées (CRM, RH, projets)
- `tests/` : Tests et scénarios de validation

## Technologies
- Python 3.13+
- LangGraph 0.0.26+
- LangChain 0.1.0+
- Streamlit 1.29.0+
- Pydantic 2.5.0+

## État du Projet
✅ - [x] Copilot instructions créées
✅ - [x] Structure du projet créée
✅ - [x] Dependencies installées
✅ - [x] Agent Interface implémenté et testé
✅ - [x] Agent Systèmes implémenté et testé
✅ - [x] Workflow LangGraph configuré et fonctionnel
✅ - [x] Interface Streamlit créée
✅ - [x] Tests et scénarios ajoutés (92.3% de réussite)

## Démarrage Rapide
1. `python run_app.py` - Lance l'interface Streamlit
2. `python tests/test_scenarios.py` - Exécute les tests
3. `python src/workflows/multi_agent_workflow.py` - Test du workflow

## Résultats des Tests
- ✅ **CRM**: 5/5 tests réussis (100%)
- ✅ **RH**: 5/5 tests réussis (100%) 
- ⚠️ **PROJETS**: 2/3 tests réussis (67%) - Amélioration détection nécessaire
- 📊 **Global**: 12/13 tests réussis (**92.3%**)
