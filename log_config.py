"""
Configuration du système de logs.
Ce module définit les paramètres de configuration pour le système de logs.
"""

import logging
import os

# Configuration générale
LOG_LEVEL = logging.DEBUG  # Niveau de log par défaut (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s (%(filename)s:%(lineno)d): %(message)s"
CONSOLE_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"

# Configuration des fichiers
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
DEBUG_LOG_DIR = os.path.join(LOG_DIR, "debug")
ERROR_LOG_DIR = os.path.join(LOG_DIR, "error")
PERFORMANCE_LOG_DIR = os.path.join(LOG_DIR, "performance")

# Configuration des limites
MAX_LOG_SIZE = 10 * 1024 * 1024  # 10 Mo
MAX_DEBUG_LOG_SIZE = 20 * 1024 * 1024  # 20 Mo
MAX_ERROR_LOG_SIZE = 10 * 1024 * 1024  # 10 Mo
MAX_PERF_LOG_SIZE = 5 * 1024 * 1024  # 5 Mo

LOG_BACKUP_COUNT = 5
DEBUG_BACKUP_COUNT = 3
ERROR_BACKUP_COUNT = 10
PERF_BACKUP_COUNT = 3

# Configuration de la rétention
LOG_RETENTION_DAYS = 30  # Jours de conservation des logs

# Configuration des performances
PERFORMANCE_THRESHOLD = 0.1  # Seuil en secondes pour considérer une opération comme lente
