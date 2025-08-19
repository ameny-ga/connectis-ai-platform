"""
Connecteur Odoo - Interface pour communiquer avec l'API XML-RPC d'Odoo
"""

import xmlrpc.client
import json
import sys
import os
from typing import Dict, Any, List, Optional, Union

# Ajouter le répertoire racine au path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from config_odoo import get_odoo_config, validate_odoo_config, ODOO_MODELS, ODOO_FIELDS


class OdooConnector:
    """
    Connecteur pour l'API XML-RPC d'Odoo
    """
    
    def __init__(self, use_test: bool = False):
        """
        Initialise la connexion à Odoo
        
        Args:
            use_test: Si True, utilise la configuration de test
        """
        self.config = get_odoo_config(use_test)
        self.uid = None
        self.models = None
        self.common = None
        self.is_connected = False
        
        # Valider la configuration
        if not validate_odoo_config(self.config):
            raise ValueError("Configuration Odoo invalide")
    
    def connect(self) -> bool:
        """
        Établit la connexion avec Odoo
        
        Returns:
            True si connexion réussie, False sinon
        """
        try:
            # URLs des services Odoo
            common_url = f"{self.config['url']}/xmlrpc/2/common"
            object_url = f"{self.config['url']}/xmlrpc/2/object"
            
            # Connexion au service commun
            self.common = xmlrpc.client.ServerProxy(common_url)
            
            # Test de version
            version_info = self.common.version()
            print(f"🔗 Connexion à Odoo {version_info['server_version']}")
            
            # Authentification
            self.uid = self.common.authenticate(
                self.config['database'],
                self.config['username'], 
                self.config['password'],
                {}
            )
            
            if not self.uid:
                print("❌ Échec de l'authentification")
                return False
            
            # Connexion au service des objets
            self.models = xmlrpc.client.ServerProxy(object_url)
            
            print(f"✅ Connexion réussie - UID: {self.uid}")
            self.is_connected = True
            return True
            
        except Exception as e:
            print(f"❌ Erreur de connexion: {str(e)}")
            self.is_connected = False
            return False
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test la connexion et retourne des informations
        
        Returns:
            Dict avec les informations de connexion
        """
        if not self.is_connected:
            if not self.connect():
                return {
                    "success": False,
                    "error": "Impossible de se connecter à Odoo"
                }
        
        try:
            # Test simple : récupérer le nom de l'utilisateur
            user_info = self.models.execute_kw(
                self.config['database'], self.uid, self.config['password'],
                'res.users', 'read',
                [self.uid], {'fields': ['name', 'login', 'email']}
            )
            
            return {
                "success": True,
                "connection_info": {
                    "url": self.config['url'],
                    "database": self.config['database'],
                    "user": user_info[0] if user_info else {},
                    "uid": self.uid
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Test de connexion échoué: {str(e)}"
            }
    
    def search_records(self, model: str, domain: List = None, fields: List[str] = None, 
                      limit: int = 100) -> Dict[str, Any]:
        """
        Recherche des enregistrements dans Odoo
        
        Args:
            model: Nom du modèle Odoo (ex: 'res.partner')
            domain: Domaine de recherche (filtres)
            fields: Champs à récupérer
            limit: Nombre maximum d'enregistrements
            
        Returns:
            Dict avec les résultats
        """
        if not self.is_connected:
            return {"success": False, "error": "Non connecté à Odoo"}
        
        try:
            domain = domain or []
            fields = fields or ODOO_FIELDS.get(model, [])
            
            # Recherche des IDs
            record_ids = self.models.execute_kw(
                self.config['database'], self.uid, self.config['password'],
                model, 'search',
                [domain], {'limit': limit}
            )
            
            if not record_ids:
                return {
                    "success": True,
                    "count": 0,
                    "records": []
                }
            
            # Lecture des enregistrements
            records = self.models.execute_kw(
                self.config['database'], self.uid, self.config['password'],
                model, 'read',
                [record_ids], {'fields': fields}
            )
            
            return {
                "success": True,
                "count": len(records),
                "records": records
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur lors de la recherche: {str(e)}"
            }
    
    def get_clients(self, limit: int = 50) -> Dict[str, Any]:
        """
        Récupère la liste des clients depuis Odoo
        
        Args:
            limit: Nombre maximum de clients
            
        Returns:
            Dict avec les clients
        """
        if not self.is_connected:
            return {"success": False, "error": "Non connecté à Odoo"}
        
        try:
            # Utiliser search_read directement pour plus d'efficacité
            records = self.models.execute_kw(
                self.config['database'], self.uid, self.config['password'],
                'res.partner', 'search_read',
                [[]],  # Domain vide = tous les enregistrements
                {
                    'fields': ['id', 'name', 'email', 'phone', 'street', 'city', 
                              'country_id', 'is_company'],  # Enlever mobile et customer_rank qui n'existent pas
                    'limit': limit
                }
            )
            
            # Formatage pour compatibilité avec notre interface
            formatted_clients = []
            for record in records:
                # Gérer les valeurs False d'Odoo
                email = record.get("email")
                if email is False:
                    email = ""
                
                phone = record.get("phone")
                if phone is False:
                    phone = ""
                
                street = record.get("street") or ""
                city = record.get("city") or ""
                
                client = {
                    "id": record.get("id"),
                    "nom": record.get("name", ""),
                    "email": email,
                    "telephone": phone,
                    "mobile": "",  # Pas disponible dans cette version
                    "adresse": f"{street} {city}".strip(),
                    "pays": record.get("country_id", [None, ""])[1] if record.get("country_id") else "",
                    "est_entreprise": record.get("is_company", False),
                    "rang_client": 0,  # Pas disponible
                    "rang_fournisseur": 0,  # Pas disponible
                    "statut": "Actif",
                    "source": "Odoo CRM"
                }
                formatted_clients.append(client)
            
            return {
                "success": True,
                "count": len(formatted_clients),
                "clients": formatted_clients
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur lors de la récupération des clients: {str(e)}"
            }
    
    def get_opportunites(self, limit: int = 50) -> Dict[str, Any]:
        """
        Récupère la liste des opportunités depuis Odoo
        
        Args:
            limit: Nombre maximum d'opportunités
            
        Returns:
            Dict avec les opportunités
        """
        # Domain pour les opportunités (type = 'opportunity')
        domain = [('type', '=', 'opportunity')]
        
        result = self.search_records('crm.lead', domain, limit=limit)
        
        if result["success"]:
            # Formatage pour compatibilité
            formatted_opps = []
            for record in result["records"]:
                opp = {
                    "id": record.get("id"),
                    "titre": record.get("name", ""),
                    "client_nom": record.get("partner_id", [None, ""])[1] if record.get("partner_id") else "",
                    "client_id": record.get("partner_id", [None])[0] if record.get("partner_id") else None,
                    "email": record.get("email_from", ""),
                    "telephone": record.get("phone", ""),
                    "etape": record.get("stage_id", [None, ""])[1] if record.get("stage_id") else "",
                    "probabilite": record.get("probability", 0),
                    "valeur_prevue": record.get("expected_revenue", 0),
                    "date_echeance": record.get("date_deadline", ""),
                    "date_creation": record.get("create_date", ""),
                    "responsable": record.get("user_id", [None, ""])[1] if record.get("user_id") else "",
                    "equipe": record.get("team_id", [None, ""])[1] if record.get("team_id") else "",
                    "description": record.get("description", "")
                }
                formatted_opps.append(opp)
            
            return {
                "success": True,
                "count": len(formatted_opps),
                "opportunites": formatted_opps
            }
        
        return result
    
    def create_client(self, client_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crée un nouveau client dans Odoo
        
        Args:
            client_data: Données du client
            
        Returns:
            Dict avec le résultat
        """
        if not self.is_connected:
            return {"success": False, "error": "Non connecté à Odoo"}
        
        try:
            # Mapping des champs (utilisation uniquement des champs disponibles)
            odoo_data = {
                'name': client_data.get('nom', ''),
                'email': client_data.get('email', ''),
                'phone': client_data.get('telephone', ''),
                'is_company': client_data.get('est_entreprise', False)
            }
            
            # Ajout de l'adresse si fournie
            if client_data.get('adresse'):
                odoo_data['street'] = client_data['adresse']
            
            # Création
            new_id = self.models.execute_kw(
                self.config['database'], self.uid, self.config['password'],
                'res.partner', 'create',
                [odoo_data]
            )
            
            return {
                "success": True,
                "client_id": new_id,
                "message": f"Client créé avec l'ID {new_id}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur lors de la création: {str(e)}"
            }
    
    def update_client(self, client_id: int, client_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Met à jour un client existant dans Odoo
        
        Args:
            client_id: ID du client à modifier
            client_data: Nouvelles données du client
            
        Returns:
            Dict avec le résultat
        """
        if not self.is_connected:
            return {"success": False, "error": "Non connecté à Odoo"}
        
        try:
            # Mapping des champs (seulement les champs fournis)
            odoo_data = {}
            if 'nom' in client_data:
                odoo_data['name'] = client_data['nom']
            if 'email' in client_data:
                odoo_data['email'] = client_data['email']
            if 'telephone' in client_data:
                odoo_data['phone'] = client_data['telephone']
            if 'adresse' in client_data:
                odoo_data['street'] = client_data['adresse']
            if 'est_entreprise' in client_data:
                odoo_data['is_company'] = client_data['est_entreprise']
            
            # Modification
            self.models.execute_kw(
                self.config['database'], self.uid, self.config['password'],
                'res.partner', 'write',
                [[client_id], odoo_data]
            )
            
            return {
                "success": True,
                "client_id": client_id,
                "message": f"Client {client_id} modifié avec succès"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur lors de la modification: {str(e)}"
            }
    
    def delete_client(self, client_id: int) -> Dict[str, Any]:
        """
        Supprime un client dans Odoo (archive en réalité)
        
        Args:
            client_id: ID du client à supprimer
            
        Returns:
            Dict avec le résultat
        """
        if not self.is_connected:
            return {"success": False, "error": "Non connecté à Odoo"}
        
        try:
            # Archiver plutôt que supprimer (bonne pratique Odoo)
            self.models.execute_kw(
                self.config['database'], self.uid, self.config['password'],
                'res.partner', 'write',
                [[client_id], {'active': False}]
            )
            
            return {
                "success": True,
                "client_id": client_id,
                "message": f"Client {client_id} archivé avec succès"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur lors de l'archivage: {str(e)}"
            }
    
    def create_opportunite(self, opp_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crée une nouvelle opportunité dans Odoo
        
        Args:
            opp_data: Données de l'opportunité
            
        Returns:
            Dict avec le résultat
        """
        if not self.is_connected:
            return {"success": False, "error": "Non connecté à Odoo"}
        
        try:
            # Mapping des champs
            odoo_data = {
                'name': opp_data.get('titre', ''),
                'type': 'opportunity',  # Important pour les opportunités
                'probability': opp_data.get('probabilite', 50),
                'expected_revenue': opp_data.get('valeur_prevue', 0),
                'description': opp_data.get('description', ''),
                'email_from': opp_data.get('email', ''),
                'phone': opp_data.get('telephone', '')
            }
            
            # Si un client_id est fourni, l'associer
            if 'client_id' in opp_data:
                odoo_data['partner_id'] = opp_data['client_id']
            
            # Création
            new_id = self.models.execute_kw(
                self.config['database'], self.uid, self.config['password'],
                'crm.lead', 'create',
                [odoo_data]
            )
            
            return {
                "success": True,
                "opportunite_id": new_id,
                "message": f"Opportunité créée avec l'ID {new_id}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur lors de la création: {str(e)}"
            }
    
    def update_opportunite(self, opp_id: int, opp_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Met à jour une opportunité existante dans Odoo
        
        Args:
            opp_id: ID de l'opportunité à modifier
            opp_data: Nouvelles données de l'opportunité
            
        Returns:
            Dict avec le résultat
        """
        if not self.is_connected:
            return {"success": False, "error": "Non connecté à Odoo"}
        
        try:
            # Mapping des champs (seulement les champs fournis)
            odoo_data = {}
            if 'titre' in opp_data:
                odoo_data['name'] = opp_data['titre']
            if 'probabilite' in opp_data:
                odoo_data['probability'] = opp_data['probabilite']
            if 'valeur_prevue' in opp_data:
                odoo_data['expected_revenue'] = opp_data['valeur_prevue']
            if 'description' in opp_data:
                odoo_data['description'] = opp_data['description']
            if 'email' in opp_data:
                odoo_data['email_from'] = opp_data['email']
            if 'telephone' in opp_data:
                odoo_data['phone'] = opp_data['telephone']
            
            # Modification
            self.models.execute_kw(
                self.config['database'], self.uid, self.config['password'],
                'crm.lead', 'write',
                [[opp_id], odoo_data]
            )
            
            return {
                "success": True,
                "opportunite_id": opp_id,
                "message": f"Opportunité {opp_id} modifiée avec succès"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur lors de la modification: {str(e)}"
            }
    
    def delete_opportunite(self, opp_id: int) -> Dict[str, Any]:
        """
        Supprime une opportunité dans Odoo
        
        Args:
            opp_id: ID de l'opportunité à supprimer
            
        Returns:
            Dict avec le résultat
        """
        if not self.is_connected:
            return {"success": False, "error": "Non connecté à Odoo"}
        
        try:
            # Supprimer définitivement l'opportunité
            self.models.execute_kw(
                self.config['database'], self.uid, self.config['password'],
                'crm.lead', 'unlink',
                [[opp_id]]
            )
            
            return {
                "success": True,
                "opportunite_id": opp_id,
                "message": f"Opportunité {opp_id} supprimée avec succès"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur lors de la suppression: {str(e)}"
            }
    
    def search_clients(self, search_criteria: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recherche des clients selon des critères
        
        Args:
            search_criteria: Critères de recherche
            
        Returns:
            Dict avec les résultats
        """
        if not self.is_connected:
            return {"success": False, "error": "Non connecté à Odoo"}
        
        try:
            # Construire le domain de recherche
            domain = []
            
            if 'nom' in search_criteria:
                domain.append(('name', 'ilike', search_criteria['nom']))
            if 'email' in search_criteria:
                domain.append(('email', 'ilike', search_criteria['email']))
            if 'telephone' in search_criteria:
                domain.append(('phone', 'ilike', search_criteria['telephone']))
            if 'est_entreprise' in search_criteria:
                domain.append(('is_company', '=', search_criteria['est_entreprise']))
            
            # Recherche
            records = self.models.execute_kw(
                self.config['database'], self.uid, self.config['password'],
                'res.partner', 'search_read',
                [domain],
                {
                    'fields': ['id', 'name', 'email', 'phone', 'street', 'city', 
                              'country_id', 'is_company'],
                    'limit': 50
                }
            )
            
            # Formatage
            formatted_clients = []
            for record in records:
                client = {
                    "id": record.get("id"),
                    "nom": record.get("name", ""),
                    "email": record.get("email", "") or "",
                    "telephone": record.get("phone", "") or "",
                    "adresse": f"{record.get('street', '') or ''} {record.get('city', '') or ''}".strip(),
                    "pays": record.get("country_id", [None, ""])[1] if record.get("country_id") else "",
                    "est_entreprise": record.get("is_company", False),
                    "source": "Odoo CRM"
                }
                formatted_clients.append(client)
            
            return {
                "success": True,
                "count": len(formatted_clients),
                "clients": formatted_clients
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur lors de la recherche: {str(e)}"
            }
    
    def disconnect(self):
        """Ferme la connexion"""
        self.is_connected = False
        self.uid = None
        self.models = None
        self.common = None
        print("🔌 Déconnexion d'Odoo")


def test_odoo_connector():
    """Test du connecteur Odoo"""
    print("🧪 Test du Connecteur Odoo")
    print("=" * 50)
    
    try:
        # Création du connecteur
        connector = OdooConnector()
        
        # Test de connexion
        result = connector.test_connection()
        print(f"Test de connexion: {result}")
        
        if result["success"]:
            print(f"✅ Connecté en tant que: {result['connection_info']['user']['name']}")
            
            # Test récupération clients
            print("\n📋 Test récupération clients...")
            clients = connector.get_clients(limit=5)
            print(f"Résultat clients: {clients}")
            if clients.get("success"):
                print(f"Clients trouvés: {clients.get('count', 0)}")
                for client in clients.get('clients', [])[:3]:
                    print(f"  - {client.get('nom')} ({client.get('email')})")
            else:
                print(f"Erreur clients: {clients.get('error', 'Inconnue')}")
            
            # Test récupération opportunités
            print("\n💼 Test récupération opportunités...")
            opps = connector.get_opportunites(limit=5)
            print(f"Opportunités trouvées: {opps.get('count', 0)}")
            
        connector.disconnect()
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")


if __name__ == "__main__":
    test_odoo_connector()
