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
```

### Gestion des fichiers

```python
from EndoriumUtils import safe_read_file, safe_write_file, get_file_hash

# Lecture sécurisée
content = safe_read_file("mon_fichier.txt", default_content="Contenu par défaut")

# Écriture sécurisée avec backup automatique
safe_write_file("mon_fichier.txt", "Nouveau contenu", create_backup=True)

# Vérifier l'intégrité d'un fichier
file_hash = get_file_hash("mon_fichier.txt")
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
```

## Licence

MIT
