"""
Configuration Odoo pour CONNECT'IS

SÉCURITÉ : Ce fichier ne contient PAS de données sensibles.
Les vraies identifiants sont stockés dans le fichier .env (non versionné).

Pour configurer votre connexion Odoo, créez un fichier .env avec :
ODOO_URL=https://votre-instance.odoo.com
ODOO_DATABASE=votre-base
ODOO_USERNAME=votre-email@domain.com
ODOO_PASSWORD=votre-mot-de-passe
"""

import os
from typing import Dict, Any, Optional

# Configuration Odoo - Chargée depuis variables d'environnement (.env)
ODOO_CONFIG = {
    # URL de votre instance Odoo
    "url": os.getenv("ODOO_URL", "https://your-instance.odoo.com"),
    
    # Base de données Odoo
    "database": os.getenv("ODOO_DATABASE", "your-database"),
    
    # Identifiants de connexion (chargés depuis .env)
    "username": os.getenv("ODOO_USERNAME", "your-email@domain.com"),
    "password": os.getenv("ODOO_PASSWORD", "your-password"),
    
    # Version d'API (généralement 2)
    "api_version": 2
}

# Configuration de test (pour développement local)
ODOO_TEST_CONFIG = {
    "url": "http://localhost:8069",
    "database": "test_db", 
    "username": "admin",
    "password": "admin",
    "api_version": 2
}

# Mapping des modèles Odoo
ODOO_MODELS = {
    "clients": "res.partner",
    "opportunites": "crm.lead",
    "contacts": "res.partner",
    "produits": "product.product",
    "commandes": "sale.order"
}

# Champs à récupérer pour chaque modèle
ODOO_FIELDS = {
    "res.partner": [
        "id", "name", "email", "phone", "mobile",
        "street", "city", "country_id", "category_id",
        "is_company", "customer_rank", "supplier_rank",
        "active", "create_date", "write_date"
    ],
    "crm.lead": [
        "id", "name", "partner_id", "email_from", "phone",
        "stage_id", "probability", "expected_revenue",
        "date_deadline", "create_date", "user_id",
        "team_id", "description", "type"
    ]
}

def get_odoo_config(use_test: bool = False) -> Dict[str, Any]:
    """
    Retourne la configuration Odoo appropriée
    
    Args:
        use_test: Si True, utilise la config de test
        
    Returns:
        Dict avec la configuration Odoo
    """
    if use_test:
        return ODOO_TEST_CONFIG.copy()
    
    # Priorité aux variables d'environnement
    config = ODOO_CONFIG.copy()
    
    # Surcharger avec les variables d'environnement si disponibles
    config["url"] = os.getenv("ODOO_URL", config["url"])
    config["database"] = os.getenv("ODOO_DATABASE", config["database"])
    config["username"] = os.getenv("ODOO_USERNAME", config["username"])
    config["password"] = os.getenv("ODOO_PASSWORD", config["password"])
    
    return config

def validate_odoo_config(config: Dict[str, Any]) -> bool:
    """
    Valide la configuration Odoo
    
    Args:
        config: Configuration à valider
        
    Returns:
        True si valide, False sinon
    """
    required_fields = ["url", "database", "username", "password"]
    
    for field in required_fields:
        if not config.get(field):
            print(f"❌ Champ manquant dans la configuration Odoo: {field}")
            return False
    
    return True

# Instructions pour la configuration
SETUP_INSTRUCTIONS = """
🔧 CONFIGURATION ODOO REQUISE :

1. Modifiez les valeurs dans ODOO_CONFIG :
   - url: L'URL de votre instance Odoo
   - database: Le nom de votre base de données
   - username: Votre nom d'utilisateur Odoo
   - password: Votre mot de passe

2. Alternative avec variables d'environnement :
   - ODOO_URL=https://votre-instance.odoo.com
   - ODOO_DATABASE=votre_db
   - ODOO_USERNAME=votre_email@domain.com
   - ODOO_PASSWORD=votre_mot_de_passe

3. Pour tester en local :
   - Installez Odoo localement sur le port 8069
   - Utilisez ODOO_TEST_CONFIG

⚠️ SÉCURITÉ : Ne jamais commiter les vraies identifiants !
"""

if __name__ == "__main__":
    print("📋 Configuration Odoo")
    print("=" * 50)
    print(SETUP_INSTRUCTIONS)
    
    config = get_odoo_config()
    print(f"\n🔍 Configuration actuelle :")
    print(f"URL: {config['url']}")
    print(f"Database: {config['database']}")
    print(f"Username: {config['username']}")
    print(f"Password: {'*' * len(config['password'])}")
    
    if validate_odoo_config(config):
        print("\n✅ Configuration valide")
    else:
        print("\n❌ Configuration invalide")
