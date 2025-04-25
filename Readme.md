# EndoriumUtils

Bibliothèque d'utilitaires pour les projets Endorium.

## Fonctionnalités

- **Gestion des logs**: Configuration avancée du système de logs avec rotation et séparation par niveau
- **Gestion des versions**: Lecture et incrémentation automatique des versions de projet
- **Gestion des fichiers**: Lecture/écriture sécurisée de fichiers avec backup automatique
- **Gestion des configurations**: Chargement/sauvegarde de configurations en JSON et YAML

## Installation

```bash
pip install EndoriumUtils
```

Pour utiliser les fonctionnalités YAML, installez la bibliothèque avec le support YAML :

```bash
pip install EndoriumUtils[yaml]
```

Ou depuis le code source:

```bash
pip install -e .
```

## Utilisation

### Logging

```python
from EndoriumUtils import get_logger, log_function_call

# Obtenir un logger pour votre module
logger = get_logger("mon_module")
logger.info("Message d'information")
logger.debug("Message de debug")
logger.error("Message d'erreur")

# Décorateur pour logger automatiquement l'appel et le retour des fonctions
@log_function_call
def ma_fonction(param):
    return param * 2

# Mesurer la performance d'une section de code
from EndoriumUtils import log_performance
with log_performance(logger, "opération coûteuse"):
    # Code à mesurer...
    time.sleep(1)
```

### Gestion des logs avancée

```python
from EndoriumUtils import setup_logger, set_log_level, log_exceptions, purge_old_logs
import logging

# Configuration personnalisée d'un logger
logger = setup_logger("mon_application", log_level=logging.INFO, base_dir="/chemin/vers/app")

# Changer le niveau de log dynamiquement
set_log_level(logger, logging.DEBUG)  # Passer en mode debug

# Décorateur pour capturer automatiquement les exceptions
@log_exceptions
def fonction_risquee():
    # Le code peut lever des exceptions, elles seront automatiquement loggées
    return 1 / 0  # Division par zéro

# Nettoyage automatique des anciens logs
nb_logs_supprimes = purge_old_logs(days=15)  # Supprimer les logs de plus de 15 jours
print(f"{nb_logs_supprimes} fichiers de logs ont été supprimés")
```

### Gestion des versions

```python
from EndoriumUtils import get_version, increment_version, set_version

# Obtenir la version actuelle
version_str, version_list = get_version()
print(f"Version actuelle: {version_str}")  # ex: "1.0.0"

# Incrémenter la version
new_version = increment_version('minor')  # Options: 'major', 'minor', 'patch'
print(f"Nouvelle version: {new_version}")  # ex: "1.1.0"

# Définir explicitement une version
set_version("2.0.0")

# Utilisation avec un chemin de projet spécifique
version_str, version_list = get_version("/chemin/vers/autre/projet")
print(f"Version du projet spécifique: {version_str}")
```

### Gestion des fichiers

```python
from EndoriumUtils import safe_read_file, safe_write_file, get_file_hash, ensure_dir_exists, is_file_newer_than
import time

# Lecture sécurisée
content = safe_read_file("mon_fichier.txt", default_content="Contenu par défaut")

# Écriture sécurisée avec backup automatique
safe_write_file("mon_fichier.txt", "Nouveau contenu", create_backup=True)

# Vérifier l'intégrité d'un fichier
file_hash = get_file_hash("mon_fichier.txt")
print(f"Hash SHA-256 du fichier: {file_hash}")

# Hash avec algorithme personnalisé
md5_hash = get_file_hash("mon_fichier.txt", algorithm="md5")

# Créer une arborescence de dossiers
ensure_dir_exists("dossier/sous_dossier/data")

# Vérifier si un fichier est plus récent qu'une date donnée
reference_time = time.time() - 3600  # Il y a 1 heure
if is_file_newer_than("mon_fichier.txt", reference_time):
    print("Le fichier a été modifié durant la dernière heure")
```

### Gestion des configurations

```python
from EndoriumUtils import load_config, save_config, get_config_value, set_config_value

# Configuration par défaut
default_config = {
    "app": {
        "name": "MonApplication",
        "debug": False
    },
    "database": {
        "host": "localhost",
        "port": 5432
    }
}

# Charger une configuration
config = load_config("config.json", default_config)

# Accéder à une valeur (avec notation par points)
db_host = get_config_value(config, "database.host", "127.0.0.1")

# Modifier une valeur
set_config_value(config, "app.debug", True)

# Sauvegarder la configuration
save_config(config, "config.json")

# Travailler avec différents formats
yaml_config = load_config("config.yaml", default_config, file_format="yaml")
save_config(yaml_config, "config.yaml", file_format="yaml", indent=4)

# Charger avec détection automatique du format basée sur l'extension
auto_config = load_config("config.yml", default_config)  # Détectera YAML automatiquement
```

### Combinaisons pratiques

```python
from EndoriumUtils import get_logger, safe_read_file, safe_write_file, load_config

# Obtenir un logger
logger = get_logger("mon_script")

# Opération de lecture/écriture journalisée
def mise_a_jour_configuration():
    logger.info("Début de la mise à jour de configuration")
    
    try:
        # Charger la configuration
        config = load_config("config.json", {"version": "1.0.0", "settings": {}})
        logger.debug(f"Configuration chargée: {len(config)} paramètres")
        
        # Modifier la configuration
        config["settings"]["derniere_execution"] = time.strftime("%Y-%m-%d %H:%M:%S")
        
        # Sauvegarder
        if save_config(config, "config.json"):
            logger.info("Configuration mise à jour avec succès")
        else:
            logger.error("Échec de la sauvegarde de la configuration")
            
    except Exception as e:
        logger.exception(f"Erreur lors de la mise à jour: {e}")
        
    logger.info("Fin de la mise à jour de configuration")
```

### Utilisation dans des scripts automatisés

```python
from EndoriumUtils import get_logger, increment_version, purge_old_logs, log_performance

logger = get_logger("script_release")

def publier_nouvelle_version():
    # Nettoyage des logs anciens
    purge_old_logs(days=30)
    
    # Mesurer la performance du processus
    with log_performance(logger, "publication version"):
        # Incrémenter la version du projet
        new_version = increment_version('minor')
        logger.info(f"Version incrémentée à {new_version}")
        
        # Simuler des opérations de publication
        logger.info("Compilation du projet...")
        time.sleep(2)  # Opérations réelles de build ici
        
        logger.info("Tests unitaires...")
        time.sleep(1)  # Exécution des tests ici
        
        logger.info("Déploiement...")
        time.sleep(3)  # Opérations de déploiement ici
        
    logger.info(f"Version {new_version} publiée avec succès!")
    
    return new_version
```

## Licence

MIT
