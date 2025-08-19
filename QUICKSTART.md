# 🚀 Guide de Démarrage Rapide - LangGraph Multi-Agents

## ⚡ Lancement Immédiat

### Option 1: Script Automatique
```bash
python run_app.py
```

### Option 2: Streamlit Direct  
```bash
streamlit run src/interface/app.py
```

L'application s'ouvrira automatiquement dans votre navigateur à : http://localhost:8501

---

## 🧪 Tests et Validation

### Exécuter tous les tests
```bash
python tests/test_scenarios.py
```

### Tester les composants individuels
```bash
# Test du workflow complet
python src/workflows/multi_agent_workflow.py

# Test Agent Interface
python src/agents/interface_agent.py

# Test Agent Systèmes  
python src/agents/systems_agent.py
```

---

## 💡 Exemples de Requêtes à Tester

### 🔵 CRM (Clients & Commercial)
- "Montre-moi tous les clients"
- "Cherche le client TechnoPlus" 
- "Statut des opportunités commerciales"
- "Ajoute un nouveau client nommé TestCorp"

### 🔵 RH (Ressources Humaines)
- "Liste tous les employés"
- "Trouve l'employé Dubois"
- "Quel est le statut des congés en cours?"
- "Génère un rapport RH complet"

### 🔵 PROJETS (Gestion de Projets)
- "Affiche tous les projets"
- "Quel est le statut du projet P001?"
- "Progression de tous les projets"

---

## 📊 Résultats Attendus

**Taux de succès : 92.3%**
- ✅ CRM : 100% (5/5 tests)
- ✅ RH : 100% (5/5 tests) 
- ⚠️ PROJETS : 67% (2/3 tests)

---

## 🛠️ Structure des Données

### CRM (`data/crm_data.json`)
- 3 clients (TechnoPlus, Innovation Labs, Digital Solutions)
- 2 opportunités commerciales

### RH (`data/hr_data.json`) 
- 5 employés (IT + RH)
- Congés, évaluations

### PROJETS (`data/projects_data.json`)
- 3 projets (e-commerce, mobile, audit)
- Tâches et jalons associés

---

## 🎯 Points Clés du Projet

✅ **LangGraph** : Workflow multi-agents fonctionnel  
✅ **Agents** : Interface (parsing) + Systèmes (exécution)  
✅ **JSON** : Données mockées réalistes  
✅ **Streamlit** : Interface utilisateur complète  
✅ **Tests** : 13 scénarios automatisés  

---

## 🔧 Dépannage

### Si le port 8501 est occupé
```bash
streamlit run src/interface/app.py --server.port 8502
```

### Si erreur d'import
Vérifiez que vous êtes dans le bon répertoire :
```bash
cd c:\Users\amani\Documents\v0
```

### Si problème de modules
Réactivez l'environnement virtuel :
```bash
.\venv\Scripts\Activate.ps1
```

---

*🎓 Projet académique développé en 2 jours pour démontrer LangGraph et les systèmes multi-agents*
