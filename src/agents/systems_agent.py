"""
Agent Systèmes - Exécute les instructions sur les systèmes (Odoo + JSON)
Mode Hybride : CRM via Odoo, RH/Projets via JSON
"""

import json
import os
import sys
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime, date

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from config import SYSTEMS_CONFIG, DATA_DIR

# Import du connecteur Odoo
try:
    from src.connectors.odoo_connector import OdooConnector
    ODOO_AVAILABLE = True
    print("✅ Connecteur Odoo disponible")
except ImportError as e:
    ODOO_AVAILABLE = False
    print(f"⚠️ Connecteur Odoo indisponible: {e}")


class SystemsAgent:
    """
    Agent Systèmes - Mode Hybride
    - CRM : Odoo (temps réel)
    - RH/Projets : JSON (données mockées)
    """
    
    def __init__(self, use_odoo: bool = True):
        self.name = "Agent Systèmes (Hybride)"
        self.systems_config = SYSTEMS_CONFIG
        self.use_odoo = use_odoo and ODOO_AVAILABLE
        
        # Initialiser le connecteur Odoo si disponible
        self.odoo_connector = None
        if self.use_odoo:
            try:
                self.odoo_connector = OdooConnector()
                if self.odoo_connector.connect():
                    print("✅ Connecteur Odoo initialisé")
                else:
                    print("⚠️ Échec connexion Odoo - mode JSON utilisé")
                    self.use_odoo = False
            except Exception as e:
                print(f"⚠️ Erreur Odoo: {e} - mode JSON utilisé")
                self.use_odoo = False
        
        # Charger les données JSON (toujours nécessaires pour RH/Projets)
        self._load_system_data()

    def _load_system_data(self):
        """Charge les données de tous les systèmes JSON"""
        self.system_data = {}
        
        for system_name, config in self.systems_config.items():
            try:
                with open(config["data_file"], 'r', encoding='utf-8') as f:
                    self.system_data[system_name] = json.load(f)
                print(f"✅ Données {system_name} chargées")
            except FileNotFoundError:
                print(f"⚠️ Fichier {config['data_file']} non trouvé pour {system_name}")
                self.system_data[system_name] = {}
            except json.JSONDecodeError as e:
                print(f"❌ Erreur JSON dans {config['data_file']}: {e}")
                self.system_data[system_name] = {}

    def get_system_status(self) -> Dict[str, Any]:
        """Retourne le statut du système hybride"""
        return {
            "mode": "Hybride" if self.use_odoo else "JSON",
            "odoo_available": ODOO_AVAILABLE,
            "odoo_connected": self.use_odoo and self.odoo_connector and self.odoo_connector.is_connected,
            "systems": {
                "CRM": "Odoo" if self.use_odoo else "JSON",
                "RH": "JSON",
                "PROJETS": "JSON"
            }
        }

    def execute_instruction(self, instruction: Dict[str, Any]) -> Dict[str, Any]:
        """
        Exécute une instruction structurée sur le système approprié
        
        Args:
            instruction: Instruction structurée depuis l'Agent Interface
            
        Returns:
            Dict contenant le résultat de l'exécution
        """
        try:
            system = instruction.get("system", "").upper()
            operation = instruction.get("operation", "")
            parameters = instruction.get("parameters", {})
            
            if system not in self.system_data:
                return {
                    "success": False,
                    "error": f"Système {system} non supporté",
                    "agent": self.name
                }
            
            # Routage vers la méthode appropriée
            method_name = f"_execute_{system.lower()}_{operation}"
            if hasattr(self, method_name):
                result = getattr(self, method_name)(parameters)
            else:
                result = self._execute_generic_operation(system, operation, parameters)
            
            return {
                "success": True,
                "result": result,
                "system": system,
                "operation": operation,
                "agent": self.name
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "agent": self.name,
                "instruction": instruction
            }

    # === OPÉRATIONS CRM (Mode Hybride : Odoo + JSON) ===
    
    def _execute_crm_lister_clients(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Liste tous les clients CRM - Odoo en priorité"""
        if self.use_odoo and self.odoo_connector:
            try:
                result = self.odoo_connector.get_clients(limit=50)
                if result["success"]:
                    return {
                        "title": "Liste des clients (Odoo)",
                        "count": result["count"],
                        "data": result["clients"],
                        "summary": f"{result['count']} clients trouvés depuis Odoo CRM",
                        "source": "Odoo"
                    }
            except Exception as e:
                print(f"⚠️ Erreur Odoo, fallback JSON: {e}")
        
        # Fallback vers JSON si Odoo échoue
        clients = self.system_data["CRM"].get("clients", [])
        return {
            "title": "Liste des clients (JSON)",
            "count": len(clients),
            "data": clients,
            "summary": f"{len(clients)} clients trouvés depuis les données JSON",
            "source": "JSON"
        }

    def _execute_crm_rechercher_client(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Recherche un client spécifique - Odoo en priorité"""
        if self.use_odoo and self.odoo_connector:
            try:
                # Récupérer tous les clients d'Odoo et filtrer
                result = self.odoo_connector.get_clients(limit=100)
                if result["success"]:
                    nom = parameters.get("nom", "").lower()
                    client_id = parameters.get("id", "")
                    
                    filtered_clients = []
                    for client in result["clients"]:
                        if (nom and nom in client.get("nom", "").lower()) or \
                           (client_id and str(client.get("id")) == str(client_id)):
                            filtered_clients.append(client)
                    
                    return {
                        "title": "Recherche de clients (Odoo)",
                        "count": len(filtered_clients),
                        "data": filtered_clients,
                        "summary": f"{len(filtered_clients)} client(s) correspondant(s) trouvé(s) dans Odoo",
                        "source": "Odoo"
                    }
            except Exception as e:
                print(f"⚠️ Erreur Odoo, fallback JSON: {e}")
        
        # Fallback vers JSON
        clients = self.system_data["CRM"].get("clients", [])
        nom = parameters.get("nom", "").lower()
        client_id = parameters.get("id", "")
        
        results = []
        for client in clients:
            if (nom and nom in client.get("nom", "").lower()) or \
               (client_id and client.get("id") == client_id):
                results.append(client)
        
        return {
            "title": "Recherche de clients (JSON)",
            "count": len(results),
            "data": results,
            "summary": f"{len(results)} client(s) correspondant(s) trouvé(s) dans JSON",
            "source": "JSON"
        }

    def _execute_crm_lister_opportunites(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Liste toutes les opportunités commerciales - Odoo en priorité"""
        if self.use_odoo and self.odoo_connector:
            try:
                result = self.odoo_connector.get_opportunites(limit=50)
                if result["success"]:
                    return {
                        "title": "Liste des opportunités (Odoo)",
                        "count": result["count"],
                        "data": result["opportunites"],
                        "summary": f"{result['count']} opportunités trouvées depuis Odoo CRM",
                        "source": "Odoo",
                        "metrics": {
                            "total_opportunites": result["count"],
                            "valeur_totale": sum(opp.get("valeur_prevue", 0) for opp in result["opportunites"]),
                            "probabilite_moyenne": round(sum(opp.get("probabilite", 0) for opp in result["opportunites"]) / max(1, result["count"]), 1)
                        }
                    }
            except Exception as e:
                print(f"⚠️ Erreur Odoo, fallback JSON: {e}")
        
        # Fallback vers JSON
        opportunites = self.system_data["CRM"].get("opportunites", [])
        return {
            "title": "Liste des opportunités (JSON)",
            "count": len(opportunites),
            "data": opportunites,
            "summary": f"{len(opportunites)} opportunités trouvées depuis les données JSON",
            "source": "JSON",
            "metrics": {
                "total_opportunites": len(opportunites),
                "valeur_totale": sum(opp.get("valeur", 0) for opp in opportunites)
            }
        }
        opportunites = self.system_data["CRM"].get("opportunites", [])
        
        return {
            "title": "Liste des opportunités commerciales",
            "count": len(opportunites),
            "data": opportunites,
            "summary": f"{len(opportunites)} opportunités en cours de gestion"
        }

    def _execute_crm_statut_opportunites(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Statut des opportunités commerciales"""
        opportunites = self.system_data["CRM"].get("opportunites", [])
        
        total_valeur = sum(opp.get("valeur", 0) for opp in opportunites)
        prob_moyenne = sum(opp.get("probabilite", 0) for opp in opportunites) / len(opportunites) if opportunites else 0
        
        return {
            "title": "Statut des opportunités",
            "count": len(opportunites),
            "data": opportunites,
            "summary": f"{len(opportunites)} opportunités - Valeur totale: {total_valeur}€ - Probabilité moyenne: {prob_moyenne:.1f}%",
            "metrics": {
                "total_valeur": total_valeur,
                "probabilite_moyenne": round(prob_moyenne, 1),
                "nb_opportunites": len(opportunites)
            }
        }

    def _execute_crm_ajouter_client(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Ajoute un nouveau client via Odoo"""
        if not self.odoo_connector:
            return self._fallback_error("Connecteur Odoo non disponible pour ajouter un client")
        
        # Données du client à partir des paramètres
        client_data = {
            "nom": parameters.get("nom", ""),
            "email": parameters.get("email", ""),
            "telephone": parameters.get("telephone", ""),
            "adresse": parameters.get("adresse", ""),
            "est_entreprise": parameters.get("est_entreprise", True)
        }
        
        result = self.odoo_connector.create_client(client_data)
        
        if result["success"]:
            return {
                "success": True,
                "data": {"id": result["client_id"], **client_data},
                "message": f"Client '{client_data['nom']}' créé avec l'ID {result['client_id']}",
                "client_id": result["client_id"]
            }
        else:
            return {
                "success": False,
                "error": result.get('error', 'Erreur inconnue lors de la création'),
                "message": f"Impossible d'ajouter le client: {result.get('error', 'Erreur inconnue')}"
            }
    
    def _execute_crm_modifier_client(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Modifie un client existant via Odoo"""
        if not self.odoo_connector:
            return self._fallback_error("Connecteur Odoo non disponible pour modifier un client")
        
        client_id = parameters.get("id") or parameters.get("client_id")
        if not client_id:
            return {
                "title": "Erreur de modification",
                "count": 0,
                "data": [],
                "summary": "ID du client requis pour la modification"
            }
        
        # Données à modifier (seulement les champs fournis)
        client_data = {}
        for field in ["nom", "email", "telephone", "adresse", "est_entreprise"]:
            if field in parameters:
                client_data[field] = parameters[field]
        
        result = self.odoo_connector.update_client(int(client_id), client_data)
        
        if result["success"]:
            return {
                "title": "Client modifié avec succès",
                "count": 1,
                "data": [{"id": client_id, **client_data}],
                "summary": f"Client ID {client_id} mis à jour avec succès",
                "metrics": {"client_modifie": client_id}
            }
        else:
            return {
                "title": "Erreur lors de la modification",
                "count": 0,
                "data": [],
                "summary": f"Impossible de modifier le client: {result['error']}"
            }
    
    def _execute_crm_supprimer_client(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Supprime (archive) un client via Odoo"""
        if not self.odoo_connector:
            return self._fallback_error("Connecteur Odoo non disponible pour supprimer un client")
        
        client_id = parameters.get("id") or parameters.get("client_id")
        if not client_id:
            return {
                "title": "Erreur de suppression",
                "count": 0,
                "data": [],
                "summary": "ID du client requis pour la suppression"
            }
        
        result = self.odoo_connector.delete_client(int(client_id))
        
        if result["success"]:
            return {
                "title": "Client archivé avec succès",
                "count": 1,
                "data": [{"id": client_id, "statut": "archivé"}],
                "summary": f"Client ID {client_id} archivé avec succès",
                "metrics": {"client_archive": client_id}
            }
        else:
            return {
                "title": "Erreur lors de l'archivage",
                "count": 0,
                "data": [],
                "summary": f"Impossible d'archiver le client: {result['error']}"
            }
    
    def _execute_crm_ajouter_opportunite(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Ajoute une nouvelle opportunité via Odoo"""
        if not self.odoo_connector:
            return self._fallback_error("Connecteur Odoo non disponible pour ajouter une opportunité")
        
        # Données de l'opportunité à partir des paramètres
        opp_data = {
            "titre": parameters.get("titre", parameters.get("nom", "")),
            "probabilite": parameters.get("probabilite", 50),
            "valeur_prevue": parameters.get("valeur", parameters.get("valeur_prevue", 0)),
            "description": parameters.get("description", ""),
            "email": parameters.get("email", ""),
            "telephone": parameters.get("telephone", "")
        }
        
        # Si un client_id est fourni
        if "client_id" in parameters:
            opp_data["client_id"] = parameters["client_id"]
        
        result = self.odoo_connector.create_opportunite(opp_data)
        
        if result["success"]:
            return {
                "title": "Opportunité ajoutée avec succès",
                "count": 1,
                "data": [{"id": result["opportunite_id"], **opp_data}],
                "summary": f"Opportunité '{opp_data['titre']}' créée avec l'ID {result['opportunite_id']}",
                "metrics": {"nouvelle_opportunite_id": result["opportunite_id"]}
            }
        else:
            return {
                "title": "Erreur lors de l'ajout de l'opportunité",
                "count": 0,
                "data": [],
                "summary": f"Impossible d'ajouter l'opportunité: {result['error']}"
            }
    
    def _execute_crm_modifier_opportunite(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Modifie une opportunité existante via Odoo"""
        if not self.odoo_connector:
            return self._fallback_error("Connecteur Odoo non disponible pour modifier une opportunité")
        
        opp_id = parameters.get("id") or parameters.get("opportunite_id")
        if not opp_id:
            return {
                "title": "Erreur de modification",
                "count": 0,
                "data": [],
                "summary": "ID de l'opportunité requis pour la modification"
            }
        
        # Données à modifier (seulement les champs fournis)
        opp_data = {}
        field_mapping = {
            "titre": "titre", "nom": "titre",
            "probabilite": "probabilite",
            "valeur": "valeur_prevue", "valeur_prevue": "valeur_prevue",
            "description": "description",
            "email": "email",
            "telephone": "telephone"
        }
        
        for param_field, opp_field in field_mapping.items():
            if param_field in parameters:
                opp_data[opp_field] = parameters[param_field]
        
        result = self.odoo_connector.update_opportunite(int(opp_id), opp_data)
        
        if result["success"]:
            return {
                "title": "Opportunité modifiée avec succès",
                "count": 1,
                "data": [{"id": opp_id, **opp_data}],
                "summary": f"Opportunité ID {opp_id} mise à jour avec succès",
                "metrics": {"opportunite_modifiee": opp_id}
            }
        else:
            return {
                "title": "Erreur lors de la modification",
                "count": 0,
                "data": [],
                "summary": f"Impossible de modifier l'opportunité: {result['error']}"
            }
    
    def _execute_crm_supprimer_opportunite(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Supprime une opportunité via Odoo"""
        if not self.odoo_connector:
            return self._fallback_error("Connecteur Odoo non disponible pour supprimer une opportunité")
        
        opp_id = parameters.get("id") or parameters.get("opportunite_id")
        if not opp_id:
            return {
                "title": "Erreur de suppression",
                "count": 0,
                "data": [],
                "summary": "ID de l'opportunité requis pour la suppression"
            }
        
        result = self.odoo_connector.delete_opportunite(int(opp_id))
        
        if result["success"]:
            return {
                "title": "Opportunité supprimée avec succès",
                "count": 1,
                "data": [{"id": opp_id, "statut": "supprimée"}],
                "summary": f"Opportunité ID {opp_id} supprimée avec succès",
                "metrics": {"opportunite_supprimee": opp_id}
            }
        else:
            return {
                "title": "Erreur lors de la suppression",
                "count": 0,
                "data": [],
                "summary": f"Impossible de supprimer l'opportunité: {result['error']}"
            }

    # === OPÉRATIONS RH ===
    
    def _execute_rh_lister_employes(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Liste tous les employés"""
        employes = self.system_data["RH"].get("employes", [])
        
        return {
            "title": "Liste des employés",
            "count": len(employes),
            "data": employes,
            "summary": f"{len(employes)} employés dans l'entreprise"
        }

    def _execute_rh_rechercher_employe(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Recherche un employé spécifique"""
        employes = self.system_data["RH"].get("employes", [])
        nom = parameters.get("nom", "").lower()
        employe_id = parameters.get("id", "")
        
        results = []
        for employe in employes:
            if (nom and (nom in employe.get("nom", "").lower() or nom in employe.get("prenom", "").lower())) or \
               (employe_id and employe.get("id") == employe_id):
                results.append(employe)
        
        return {
            "title": "Recherche d'employés",
            "count": len(results),
            "data": results,
            "summary": f"{len(results)} employé(s) correspondant(s) trouvé(s)"
        }

    def _execute_rh_statut_conges(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Statut des congés"""
        conges = self.system_data["RH"].get("conges", [])
        
        approuves = [c for c in conges if c.get("statut") == "Approuvé"]
        en_attente = [c for c in conges if c.get("statut") == "En attente"]
        
        return {
            "title": "Statut des congés",
            "count": len(conges),
            "data": conges,
            "summary": f"{len(conges)} demandes de congés - {len(approuves)} approuvées, {len(en_attente)} en attente",
            "metrics": {
                "total_demandes": len(conges),
                "approuvees": len(approuves),
                "en_attente": len(en_attente)
            }
        }

    def _execute_rh_rapport_rh(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Génère un rapport RH général"""
        employes = self.system_data["RH"].get("employes", [])
        conges = self.system_data["RH"].get("conges", [])
        evaluations = self.system_data["RH"].get("evaluations", [])
        
        # Statistiques par département
        departements = {}
        salaire_total = 0
        
        for employe in employes:
            dept = employe.get("departement", "Non défini")
            if dept not in departements:
                departements[dept] = {"count": 0, "salaires": []}
            departements[dept]["count"] += 1
            departements[dept]["salaires"].append(employe.get("salaire", 0))
            salaire_total += employe.get("salaire", 0)
        
        return {
            "title": "Rapport RH Global",
            "data": {
                "employes": len(employes),
                "departements": departements,
                "conges_actifs": len(conges),
                "evaluations": len(evaluations),
                "masse_salariale": salaire_total
            },
            "summary": f"Entreprise: {len(employes)} employés, {len(departements)} départements, masse salariale: {salaire_total}€"
        }

    # === OPÉRATIONS PROJETS ===
    
    def _execute_projets_lister_projets(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Liste tous les projets"""
        projets = self.system_data["PROJETS"].get("projets", [])
        
        return {
            "title": "Liste des projets",
            "count": len(projets),
            "data": projets,
            "summary": f"{len(projets)} projets en cours de gestion"
        }

    def _execute_projets_statut_projet(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Statut d'un projet spécifique"""
        projets = self.system_data["PROJETS"].get("projets", [])
        taches = self.system_data["PROJETS"].get("taches", [])
        
        projet_id = parameters.get("id", "")
        nom = parameters.get("nom", "").lower()
        
        # Recherche du projet
        projet = None
        for p in projets:
            if (projet_id and p.get("id") == projet_id) or \
               (nom and nom in p.get("nom", "").lower()):
                projet = p
                break
        
        if not projet:
            return {
                "title": "Projet non trouvé",
                "count": 0,
                "data": [],
                "summary": "Aucun projet correspondant trouvé"
            }
        
        # Tâches du projet
        taches_projet = [t for t in taches if t.get("projet_id") == projet.get("id")]
        
        return {
            "title": f"Statut du projet {projet.get('nom')}",
            "count": 1,
            "data": [projet],
            "taches": taches_projet,
            "summary": f"Projet {projet.get('nom')} - Statut: {projet.get('statut')} - Progression: {projet.get('progression', 0)}%",
            "metrics": {
                "progression": projet.get("progression", 0),
                "budget_consomme": projet.get("budget_consomme", 0),
                "budget_total": projet.get("budget", 0),
                "nb_taches": len(taches_projet)
            }
        }

    def _execute_projets_progression_projets(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Vue d'ensemble de la progression des projets"""
        projets = self.system_data["PROJETS"].get("projets", [])
        
        en_cours = [p for p in projets if p.get("statut") == "En cours"]
        termines = [p for p in projets if p.get("statut") == "Terminé"]
        planifies = [p for p in projets if p.get("statut") == "Planifié"]
        
        progression_moyenne = sum(p.get("progression", 0) for p in projets) / len(projets) if projets else 0
        budget_total = sum(p.get("budget", 0) for p in projets)
        budget_consomme = sum(p.get("budget_consomme", 0) for p in projets)
        
        return {
            "title": "Progression globale des projets",
            "count": len(projets),
            "data": projets,
            "summary": f"{len(projets)} projets - {len(en_cours)} en cours, {len(termines)} terminés - Progression moyenne: {progression_moyenne:.1f}%",
            "metrics": {
                "total_projets": len(projets),
                "en_cours": len(en_cours),
                "termines": len(termines),
                "planifies": len(planifies),
                "progression_moyenne": round(progression_moyenne, 1),
                "budget_total": budget_total,
                "budget_consomme": budget_consomme,
                "pourcentage_budget": round((budget_consomme / budget_total * 100) if budget_total > 0 else 0, 1)
            }
        }

    def _execute_generic_operation(self, system: str, operation: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Opération générique pour les cas non couverts"""
        data = self.system_data.get(system, {})
        
        return {
            "title": f"Opération {operation} sur {system}",
            "data": data,
            "summary": f"Opération {operation} exécutée sur le système {system}",
            "note": "Opération générique - implémentation spécifique à développer"
        }


# Fonction utilitaire pour tester l'agent
def test_systems_agent():
    """Test rapide de l'Agent Systèmes"""
    agent = SystemsAgent()
    
    test_instructions = [
        {
            "system": "CRM",
            "operation": "lister_clients",
            "parameters": {}
        },
        {
            "system": "RH", 
            "operation": "rechercher_employe",
            "parameters": {"nom": "Dubois"}
        },
        {
            "system": "PROJETS",
            "operation": "statut_projet",
            "parameters": {"id": "P001"}
        },
        {
            "system": "CRM",
            "operation": "statut_opportunites",
            "parameters": {}
        }
    ]
    
    print("=== Test de l'Agent Systèmes ===")
    for instruction in test_instructions:
        result = agent.execute_instruction(instruction)
        print(f"\nInstruction: {instruction}")
        print(f"Résultat: {json.dumps(result, indent=2, ensure_ascii=False)}")


if __name__ == "__main__":
    test_systems_agent()
