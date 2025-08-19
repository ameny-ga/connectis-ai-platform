"""
Workflow LangGraph - Orchestration des agents Interface et Systèmes (Mode Hybride)
"""

import json
import sys
import os
from typing import Dict, Any, TypedDict, List
from langgraph.graph import StateGraph, END

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.agents.interface_agent import InterfaceAgent
from src.agents.systems_agent import SystemsAgent


class WorkflowState(TypedDict):
    """État du workflow partagé entre les agents"""
    user_input: str
    instruction: Dict[str, Any]
    result: Dict[str, Any]
    formatted_response: str
    error: str
    execution_log: List[str]


class MultiAgentWorkflow:
    """
    Workflow LangGraph orchestrant les agents Interface et Systèmes (Mode Hybride)
    CRM via Odoo + RH/Projets via JSON
    """
    
    def __init__(self, use_odoo: bool = True):
        self.interface_agent = InterfaceAgent()
        self.systems_agent = SystemsAgent(use_odoo=use_odoo)  # Mode hybride
        self.graph = self._build_graph()
        
        # Informations sur le workflow
        self.workflow_info = {
            "agents": ["Agent Interface", "Agent Systèmes (Hybride)"],
            "systems": ["CRM (Odoo)", "RH (JSON)", "PROJETS (JSON)"],
            "mode": self.systems_agent.get_system_status()["mode"]
        }

    def _build_graph(self) -> StateGraph:
        """Construit le graphe LangGraph"""
        workflow = StateGraph(WorkflowState)
        
        # Ajout des nœuds
        workflow.add_node("interface_agent", self._interface_node)
        workflow.add_node("systems_agent", self._systems_node)
        workflow.add_node("formatter", self._formatter_node)
        
        # Définition du flux
        workflow.set_entry_point("interface_agent")
        workflow.add_edge("interface_agent", "systems_agent")
        workflow.add_edge("systems_agent", "formatter")
        workflow.add_edge("formatter", END)
        
        return workflow.compile()

    def _interface_node(self, state: WorkflowState) -> WorkflowState:
        """Nœud Agent Interface - Analyse du prompt utilisateur"""
        try:
            user_input = state.get("user_input", "")
            if not user_input:
                raise ValueError("Aucun input utilisateur fourni")
            
            # Traitement par l'Agent Interface
            interface_result = self.interface_agent.process_message(user_input)
            
            if not interface_result.get("success", False):
                state["error"] = interface_result.get("error", "Erreur Agent Interface")
                return state
            
            state["instruction"] = interface_result["instruction"]
            state["execution_log"] = state.get("execution_log", []) + [
                f"Interface Agent: Instruction analysée - {interface_result['instruction']['operation']} sur {interface_result['instruction']['system']}"
            ]
            
        except Exception as e:
            state["error"] = f"Erreur dans interface_node: {str(e)}"
        
        return state

    def _systems_node(self, state: WorkflowState) -> WorkflowState:
        """Nœud Agent Systèmes - Exécution sur les systèmes"""
        try:
            instruction = state.get("instruction")
            if not instruction:
                raise ValueError("Aucune instruction fournie")
            
            # Exécution par l'Agent Systèmes
            systems_result = self.systems_agent.execute_instruction(instruction)
            
            if not systems_result.get("success", False):
                state["error"] = systems_result.get("error", "Erreur Agent Systèmes")
                return state
            
            state["result"] = systems_result
            state["execution_log"] = state.get("execution_log", []) + [
                f"Systems Agent: Opération exécutée sur {systems_result['system']} - {systems_result.get('result', {}).get('summary', 'Opération terminée')}"
            ]
            
        except Exception as e:
            state["error"] = f"Erreur dans systems_node: {str(e)}"
        
        return state

    def _formatter_node(self, state: WorkflowState) -> WorkflowState:
        """Nœud Formatter - Formatage de la réponse finale"""
        try:
            result = state.get("result")
            user_input = state.get("user_input", "")
            
            if state.get("error"):
                state["formatted_response"] = f"❌ Erreur: {state['error']}"
                return state
            
            if not result or not result.get("success"):
                state["formatted_response"] = "❌ Aucun résultat obtenu"
                return state
            
            # Formatage de la réponse
            result_data = result.get("result", {})
            title = result_data.get("title", "Résultat")
            summary = result_data.get("summary", "")
            count = result_data.get("count", 0)
            data = result_data.get("data", [])
            metrics = result_data.get("metrics", {})
            
            formatted_response = f"✅ **{title}**\n\n"
            formatted_response += f"📋 {summary}\n\n"
            
            if metrics:
                formatted_response += "📊 **Métriques:**\n"
                for key, value in metrics.items():
                    formatted_response += f"• {key.replace('_', ' ').title()}: {value}\n"
                formatted_response += "\n"
            
            # Limitation de l'affichage des données pour éviter la surcharge
            if isinstance(data, list) and len(data) > 0:
                if len(data) <= 3:
                    formatted_response += "📝 **Détails:**\n"
                    for item in data:
                        if isinstance(item, dict):
                            nom = item.get("nom", item.get("titre", item.get("id", "Item")))
                            formatted_response += f"• {nom}\n"
                else:
                    formatted_response += f"📝 **{count} éléments trouvés** (affichage limité pour la lisibilité)\n"
            
            state["formatted_response"] = formatted_response
            state["execution_log"] = state.get("execution_log", []) + [
                "Formatter: Réponse formatée pour l'utilisateur"
            ]
            
        except Exception as e:
            state["formatted_response"] = f"❌ Erreur de formatage: {str(e)}"
        
        return state

    def process_user_request(self, user_input: str) -> Dict[str, Any]:
        """
        Point d'entrée principal pour traiter une demande utilisateur
        
        Args:
            user_input: Demande de l'utilisateur en langage naturel
            
        Returns:
            Dict contenant la réponse formatée et les métadonnées
        """
        try:
            # État initial
            initial_state = WorkflowState(
                user_input=user_input,
                instruction={},
                result={},
                formatted_response="",
                error="",
                execution_log=[]
            )
            
            # Exécution du workflow
            final_state = self.graph.invoke(initial_state)
            
            return {
                "success": not bool(final_state.get("error")),
                "user_input": user_input,
                "formatted_response": final_state.get("formatted_response", ""),
                "instruction": final_state.get("instruction", {}),
                "result": final_state.get("result", {}),
                "execution_log": final_state.get("execution_log", []),
                "error": final_state.get("error", "")
            }
            
        except Exception as e:
            return {
                "success": False,
                "user_input": user_input,
                "formatted_response": f"❌ Erreur du workflow: {str(e)}",
                "error": str(e)
            }

    def get_workflow_info(self) -> Dict[str, Any]:
        """Informations sur le workflow hybride"""
        return self.workflow_info


# Fonction utilitaire pour tester le workflow
def test_workflow():
    """Test complet du workflow LangGraph"""
    workflow = MultiAgentWorkflow()
    
    test_requests = [
        "Montre-moi tous les clients",
        "Quel est le statut du projet P001?",
        "Cherche l'employé Dubois",
        "Donne-moi un rapport sur les opportunités commerciales",
        "Liste tous les projets en cours",
        "Liste des opportunités"
    ]
    
    print("=== Test du Workflow LangGraph Multi-Agents ===")
    print(f"Workflow configuré avec: {workflow.get_workflow_info()}")
    print("\n" + "="*50 + "\n")
    
    for request in test_requests:
        print(f"🔵 **Demande**: {request}")
        result = workflow.process_user_request(request)
        
        if result["success"]:
            print(f"✅ **Réponse**:\n{result['formatted_response']}")
        else:
            print(f"❌ **Erreur**: {result['error']}")
        
        print("\n" + "-"*40 + "\n")


if __name__ == "__main__":
    test_workflow()
