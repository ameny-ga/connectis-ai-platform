"""
Agent Interface - Convertit les prompts utilisateurs en instructions JSON structurées
"""

import json
import re
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from langchain.schema import BaseMessage, HumanMessage, AIMessage


class UserInstruction(BaseModel):
    """Modèle Pydantic pour les instructions utilisateur structurées"""
    action: str = Field(description="Action à effectuer")
    system: str = Field(description="Système cible (CRM, RH, PROJETS)")
    operation: str = Field(description="Opération spécifique à effectuer")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Paramètres de l'opération")
    intent: str = Field(description="Intention détectée de l'utilisateur")


class InterfaceAgent:
    """
    Agent Interface - Analyse les prompts utilisateurs et les convertit en JSON structuré
    """
    
    def __init__(self):
        self.name = "Agent Interface"
        self.supported_systems = ["CRM", "RH", "PROJETS"]
        
        # Patterns pour détecter les intentions
        self.intent_patterns = {
            "lister": [
                r"(?:liste|affiche|montre|voir).*(?:clients?|employe?s?|projets?|opportunités?)",
                r"(?:tous? les?|liste de|liste des)",
                r"(?:quels? sont|qui sont)",
                r"(?:lister|énumère|répertorie)"
            ],
            "rechercher": [
                r"(?:cherche|trouve|recherche|localise)",
                r"(?:informations? sur|détails? de)",
                r"(?:où est|qui est)"
            ],
            "ajouter": [
                r"(?:ajoute|crée|nouveau|nouvelle)",
                r"(?:enregistre|sauvegarde)",
                r"(?:créer|ajouter|insérer)"
            ],
            "modifier": [
                r"(?:modifie|change|met à jour|update)",
                r"(?:corrige|rectifie)",
                r"(?:édite|modification|mise à jour)"
            ],
            "supprimer": [
                r"(?:supprime|efface|delete|remove)",
                r"(?:archive|désactive)",
                r"(?:elimine|enlève)"
            ],
            "statut": [
                r"(?:statut|état|progression|avancement)",
                r"(?:comment ça va|où en est)",
                r"(?:situation|point sur)"
            ],
            "rapport": [
                r"(?:rapport|résumé|bilan|synthèse)",
                r"(?:performance|statistiques)"
            ]
        }
        
        # Patterns pour détecter les systèmes
        self.system_patterns = {
            "CRM": [
                r"(?:client|prospect|crm|commercial|vente|chiffre)",
                r"(?:opportunités?|deals?|contrats?|affaires?)",
                r"(?:pipeline|portefeuille commercial)"
            ],
            "RH": [
                r"(?:employe?s?|salariés?|personnel|rh|ressources? humaines?)",
                r"(?:congés?|vacations?|évaluations?|formations?)",
                r"(?:équipe|staff|collaborateurs?)"
            ],
            "PROJETS": [
                r"(?:projets?|tâches?|planning|développement)",
                r"(?:deadlines?|livraisons?|jalons?|milestones?)",
                r"(?:sprints?|itérations?)"
            ]
        }

    def analyze_prompt(self, user_prompt: str) -> UserInstruction:
        """
        Analyse un prompt utilisateur et retourne une instruction structurée
        
        Args:
            user_prompt: Le prompt de l'utilisateur en langage naturel
            
        Returns:
            UserInstruction: Instruction structurée
        """
        user_prompt_lower = user_prompt.lower()
        
        # Détection de l'intention
        detected_intent = self._detect_intent(user_prompt_lower)
        
        # Détection du système cible
        detected_system = self._detect_system(user_prompt_lower)
        
        # Génération de l'opération spécifique
        operation = self._generate_operation(detected_intent, detected_system, user_prompt_lower)
        
        # Extraction des paramètres
        parameters = self._extract_parameters(user_prompt, detected_intent, detected_system)
        
        return UserInstruction(
            action=detected_intent,
            system=detected_system,
            operation=operation,
            parameters=parameters,
            intent=user_prompt
        )

    def _detect_intent(self, prompt: str) -> str:
        """Détecte l'intention à partir du prompt - ordre prioritaire"""
        # Ordre prioritaire : modifier et supprimer d'abord car plus spécifiques
        priority_intents = ["modifier", "supprimer", "rechercher", "ajouter", "lister", "statut", "rapport"]
        
        for intent in priority_intents:
            if intent in self.intent_patterns:
                patterns = self.intent_patterns[intent]
                for pattern in patterns:
                    if re.search(pattern, prompt):
                        return intent
        return "lister"  # Intention par défaut

    def _detect_system(self, prompt: str) -> str:
        """Détecte le système cible à partir du prompt"""
        for system, patterns in self.system_patterns.items():
            for pattern in patterns:
                if re.search(pattern, prompt):
                    return system
        return "CRM"  # Système par défaut

    def _generate_operation(self, intent: str, system: str, prompt: str = "") -> str:
        """Génère l'opération spécifique basée sur l'intention, le système et le prompt"""
        
        # Détection spéciale pour les opportunités
        if system == "CRM" and re.search(r"opportunités?|deals?|affaires?", prompt.lower()):
            if intent == "lister":
                return "lister_opportunites"
            elif intent == "ajouter":
                return "ajouter_opportunite"
            elif intent == "modifier":
                return "modifier_opportunite"
            elif intent == "supprimer":
                return "supprimer_opportunite"
            elif intent in ["statut", "rapport"]:
                return "statut_opportunites"
        
        operation_map = {
            "CRM": {
                "lister": "lister_clients",
                "rechercher": "rechercher_client", 
                "ajouter": "ajouter_client",
                "modifier": "modifier_client",
                "supprimer": "supprimer_client",
                "statut": "statut_opportunites",
                "rapport": "rapport_commercial"
            },
            "RH": {
                "lister": "lister_employes",
                "rechercher": "rechercher_employe",
                "ajouter": "ajouter_employe",
                "modifier": "modifier_employe",
                "supprimer": "supprimer_employe",
                "statut": "statut_conges",
                "rapport": "rapport_rh"
            },
            "PROJETS": {
                "lister": "lister_projets",
                "rechercher": "statut_projet",
                "ajouter": "creer_projet",
                "modifier": "modifier_projet",
                "supprimer": "supprimer_projet",
                "statut": "progression_projets",
                "rapport": "rapport_projets"
            }
        }
        
        return operation_map.get(system, {}).get(intent, f"{intent}_{system.lower()}")

    def _extract_parameters(self, prompt: str, intent: str, system: str) -> Dict[str, Any]:
        """Extrait les paramètres du prompt"""
        parameters = {}
        
        # Extraction de noms/titres (patterns spécifiques selon le contexte)
        if "opportunit" in prompt.lower():
            # Patterns spécifiques pour les opportunités
            opp_name_patterns = [
                # Patterns pour la création
                r"(?:opportunité|opp)\s+(?:nommée?\s+)?([A-Za-zÀ-ÿ0-9\s]+?)(?:\s+avec\s+(?:un\s+)?montant|\s+avec\s+(?:l')?ID|\s+d'|\s+pour|$)",
                r"(?:ajoute|crée|créer)\s+(?:une\s+)?(?:opportunité\s+)?(?:nommée?\s+)?([A-Za-zÀ-ÿ0-9\s]+?)(?:\s+avec\s+(?:un\s+)?montant|\s+avec\s+(?:l')?ID|\s+d'|\s+pour|$)",
                r"(?:nouvelle\s+opportunité\s+)([A-Za-zÀ-ÿ0-9\s]+?)(?:\s+avec\s+(?:un\s+)?montant|\s+avec\s+(?:l')?ID|\s+d'|\s+pour|$)",
                # Patterns pour la modification de nom/titre
                r"(?:changer|modifier|mettre à jour).*?(?:nom|titre).*?(?:en\s+|à\s+)([A-Za-zÀ-ÿ0-9]+(?:\s+[A-Za-zÀ-ÿ0-9]+)*)(?:\s*$)",
                r"(?:nom|titre).*?(?:en\s+|à\s+)([A-Za-zÀ-ÿ0-9]+(?:\s+[A-Za-zÀ-ÿ0-9]+)*)(?:\s*$)",
                r"(?:renommer|rebaptiser).*?(?:en\s+|à\s+)([A-Za-zÀ-ÿ0-9]+(?:\s+[A-Za-zÀ-ÿ0-9]+)*)(?:\s*$)",
                r"(?:change|modifie).*?(?:titre|nom).*?(?:en\s+)([A-Za-zÀ-ÿ0-9]+(?:\s+[A-Za-zÀ-ÿ0-9]+)*)(?:\s*$)"
            ]
            
            for pattern in opp_name_patterns:
                name_match = re.search(pattern, prompt, re.IGNORECASE)
                if name_match:
                    name = name_match.group(1).strip()
                    # Éviter les noms contenant des références d'ID ou de montant
                    if name and len(name) > 1 and not re.search(r'\b(?:ID|id|montant|avec|pour)\b', name):
                        parameters["titre"] = name
                        parameters["nom"] = name  # Alias pour compatibilité
                        break
        else:
            # Patterns généraux pour les autres entités
            name_patterns = [
                r"(?:nom|nommé|appelé)\s+([A-Za-zÀ-ÿ\s]+?)(?:\s+avec|$)",
                r"(?:client|employé|projet)\s+([A-Za-zÀ-ÿ\s]+?)(?:\s+avec|$)",
                # Patterns pour modifications de nom
                r"(?:changer|modifier|mettre à jour).*?(?:nom).*?(?:en\s+|à\s+)([A-Za-zÀ-ÿ\s]+?)(?:\s+|$)",
                r"(?:nom)\s+(?:en\s+|à\s+)([A-Za-zÀ-ÿ\s]+?)(?:\s+|$)"
            ]
            
            for pattern in name_patterns:
                name_match = re.search(pattern, prompt)
                if name_match:
                    parameters["nom"] = name_match.group(1).strip()
                    break
            
        # Extraction d'emails - patterns améliorés
        email_patterns = [
            r"(?:email|e-mail|mail)\s+(?:en\s+)?([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})",
            r"(?:changer|modifier|mettre à jour).*?(?:email|e-mail|mail).*?(?:en\s+)?([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})",
            r"([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})"  # Pattern général pour email
        ]
        
        for pattern in email_patterns:
            email_match = re.search(pattern, prompt)
            if email_match:
                parameters["email"] = email_match.group(1)
                break
            
        # Extraction de téléphones
        phone_match = re.search(r"(?:telephone|téléphone|tel|phone)\s+([0-9\s\-\+\(\)]+)", prompt)
        if phone_match:
            parameters["telephone"] = phone_match.group(1).strip()
            
        # Extraction de villes
        city_match = re.search(r"(?:ville|city)\s+([A-Za-zÀ-ÿ\s]+)", prompt)
        if city_match:
            parameters["ville"] = city_match.group(1).strip()
            
        # Extraction de montants (pour opportunités) - patterns améliorés
        amount_patterns = [
            r"(?:montant|prix|valeur)\s+(?:de\s+|à\s+)?([0-9\s,\.]+)",
            r"avec\s+un\s+montant\s+(?:de\s+)?([0-9\s,\.]+)",
            r"(?:changer|modifier|mettre à jour).*?(?:montant|prix|valeur).*?(?:à\s+|en\s+)?([0-9\s,\.]+)",
            r"([0-9\s,\.]+)\s*(?:euros?|€|\$)",
            r"(?:d'une\s+valeur\s+de\s+)?([0-9\s,\.]+)"
        ]
        
        for pattern in amount_patterns:
            amount_match = re.search(pattern, prompt)
            if amount_match:
                amount_str = amount_match.group(1).replace(" ", "").replace(",", "")
                try:
                    # Mappage des champs selon le contexte
                    if "opportunit" in prompt.lower():
                        parameters["valeur_prevue"] = float(amount_str)
                        parameters["valeur"] = float(amount_str)  # Alias pour compatibilité
                    else:
                        parameters["montant"] = float(amount_str)
                except ValueError:
                    pass
                break
                
        # Extraction de probabilité (pour opportunités)
        prob_patterns = [
            r"(?:probabilité|chance|prob)\s+(?:de\s+)?([0-9]+)%?",
            r"([0-9]+)%\s+(?:de\s+)?(?:probabilité|chance)",
            r"(?:avec\s+)?([0-9]+)%\s+(?:de\s+)?(?:succès|réussite)"
        ]
        
        for pattern in prob_patterns:
            prob_match = re.search(pattern, prompt)
            if prob_match:
                try:
                    parameters["probabilite"] = int(prob_match.group(1))
                except ValueError:
                    pass
                break
                    
        # Extraction d'IDs - patterns améliorés
        id_patterns = [
            r"(?:avec\s+l')?(?:id|identifiant|ID)\s*:?\s*([0-9]+)",
            r"(?:client|ID)\s+([0-9]+)",
            r"l'ID\s+([0-9]+)"
        ]
        
        for pattern in id_patterns:
            id_match = re.search(pattern, prompt)
            if id_match:
                parameters["id"] = id_match.group(1)
                break
            
        # Extraction de statuts
        status_match = re.search(r"(?:statut|état)\s+([a-zA-ZÀ-ÿ\s]+)", prompt)
        if status_match:
            parameters["statut"] = status_match.group(1).strip()
            
        # Extraction de dates
        date_match = re.search(r"(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4})", prompt)
        if date_match:
            parameters["date"] = date_match.group(1)
            
        return parameters

    def process_message(self, message: str) -> Dict[str, Any]:
        """
        Point d'entrée principal pour traiter un message utilisateur
        
        Args:
            message: Message de l'utilisateur
            
        Returns:
            Dict contenant l'instruction structurée
        """
        try:
            instruction = self.analyze_prompt(message)
            return {
                "success": True,
                "instruction": instruction.model_dump(),
                "agent": self.name
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "agent": self.name,
                "original_message": message
            }


# Fonction utilitaire pour tester l'agent
def test_interface_agent():
    """Test rapide de l'Agent Interface"""
    agent = InterfaceAgent()
    
    test_prompts = [
        "Montre-moi la liste de tous les clients",
        "Cherche les informations sur l'employé Jean Dupont",
        "Quel est le statut du projet P001?",
        "Ajoute un nouveau client nommé TechCorp",
        "Donne-moi un rapport sur les congés des employés",
        "Liste des opportunités",
        "Montre-moi toutes les opportunités commerciales",
        "Affiche les deals en cours"
    ]
    
    print("=== Test de l'Agent Interface ===")
    for prompt in test_prompts:
        result = agent.process_message(prompt)
        print(f"\nPrompt: {prompt}")
        print(f"Résultat: {json.dumps(result, indent=2, ensure_ascii=False)}")


if __name__ == "__main__":
    test_interface_agent()
