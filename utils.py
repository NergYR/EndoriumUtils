import re
import os
import logging
import sys
import datetime
import traceback
import time
import functools
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from contextlib import contextmanager

# S'assurer que le logging de base est configuré (pour éviter les messages d'avertissement)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Configuration de log étendue
def setup_logger(name, log_level=logging.DEBUG):
    """Configure et renvoie un logger avec des handlers pour la console et les fichiers
    
    Args:
        name (str): Nom du logger (généralement __name__ du module)
        log_level (int): Niveau de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        
    Returns:
        logging.Logger: Logger configuré
    """
    # Déterminer le répertoire de base en fonction du contexte d'exécution
    if getattr(sys, 'frozen', False):
        # Si on est dans un exécutable (PyInstaller)
        base_dir = os.path.dirname(sys.executable)
    else:
        # En développement
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Création des répertoires de logs
    log_date = datetime.datetime.now().strftime("%Y-%m-%d")
    log_folder = os.path.join(base_dir, "logs")
    debug_folder = os.path.join(log_folder, "debug")
    error_folder = os.path.join(log_folder, "error")
    perf_folder = os.path.join(log_folder, "performance")
    
    # Créer les dossiers s'ils n'existent pas
    for folder in [log_folder, debug_folder, error_folder, perf_folder]:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Dossier de logs créé: {folder}")
    
    # Chemins des fichiers de logs
    log_file_path = os.path.join(log_folder, f"{log_date}.txt")
    debug_file_path = os.path.join(debug_folder, f"{log_date}_debug.txt")
    error_file_path = os.path.join(error_folder, f"{log_date}_error.txt")
    perf_file_path = os.path.join(perf_folder, f"{log_date}_performance.txt")
    
    print(f"Configuration des logs dans: {log_file_path}")
    
    # Création du logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    logger.propagate = False
    
    # Si ce logger a déjà des handlers, on les supprime pour éviter les duplications
    if logger.handlers:
        logger.handlers.clear()
    
    # Formats détaillés pour les logs
    console_format = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    file_format = "%(asctime)s [%(levelname)s] %(name)s (%(filename)s:%(lineno)d): %(message)s"
    perf_format = "%(asctime)s [PERF] %(name)s: %(message)s"
    
    # Configuration du formatter
    console_formatter = logging.Formatter(console_format)
    file_formatter = logging.Formatter(file_format)
    perf_formatter = logging.Formatter(perf_format)
    
    # Handler pour la console (stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # Handler pour le fichier de log général (avec rotation par taille)
    try:
        file_handler = RotatingFileHandler(
            log_file_path, 
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding="utf-8"
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        print(f"Handler de fichier ajouté: {log_file_path}")
    except Exception as e:
        print(f"Erreur lors de la création du handler de fichier: {str(e)}")
    
    # Handler pour les logs de debug (DEBUG et au-dessus)
    try:
        debug_handler = RotatingFileHandler(
            debug_file_path,
            maxBytes=20*1024*1024,  # 20MB
            backupCount=3,
            encoding="utf-8"
        )
        debug_handler.setLevel(logging.DEBUG)
        debug_handler.setFormatter(file_formatter)
        logger.addHandler(debug_handler)
    except Exception as e:
        print(f"Erreur lors de la création du handler de debug: {str(e)}")
    
    # Handler pour les erreurs (ERROR et CRITICAL)
    try:
        error_handler = RotatingFileHandler(
            error_file_path,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=10,
            encoding="utf-8"
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(file_formatter)
        logger.addHandler(error_handler)
    except Exception as e:
        print(f"Erreur lors de la création du handler d'erreur: {str(e)}")
    
    # Handler pour les performances
    try:
        perf_handler = RotatingFileHandler(
            perf_file_path,
            maxBytes=5*1024*1024,  # 5MB
            backupCount=3,
            encoding="utf-8"
        )
        # Créer un filtre personnalisé pour les logs de performances
        class PerformanceFilter(logging.Filter):
            def filter(self, record):
                return hasattr(record, 'performance')
        
        perf_handler.addFilter(PerformanceFilter())
        perf_handler.setFormatter(perf_formatter)
        logger.addHandler(perf_handler)
    except Exception as e:
        print(f"Erreur lors de la création du handler de performance: {str(e)}")
    
    # Vérifier que le logger a bien des handlers
    if not logger.handlers:
        print("ATTENTION: Le logger n'a pas de handlers!")
    
    return logger

# Configurer le logger principal - avec gestion d'erreurs pour débogage
try:
    print("Initialisation du système de logs...")
    logger = setup_logger("utils")
    logger.info("Système de logs initialisé avec succès")
    print("Système de logs initialisé")
except Exception as e:
    print(f"ERREUR lors de l'initialisation du système de logs: {str(e)}")
    traceback.print_exc()
    # Fallback logger
    logger = logging.getLogger("utils")
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    logger.error(f"Échec de l'initialisation du système de logs complet: {str(e)}")

# Fonction pour obtenir un logger pour d'autres modules
def get_logger(name):
    """Renvoie un logger configuré pour un module spécifique"""
    try:
        return setup_logger(name)
    except Exception as e:
        print(f"Erreur lors de la création du logger pour {name}: {str(e)}")
        fallback = logging.getLogger(name)
        if not fallback.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
            fallback.addHandler(handler)
            fallback.setLevel(logging.DEBUG)
            fallback.propagate = False
        return fallback

# Fonction de décorateur pour logger l'appel et le retour des fonctions
def log_function_call(func):
    """Décorateur pour logger l'appel et le retour des fonctions"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        module_name = func.__module__
        func_logger = get_logger(module_name)
        
        # Filtrer des arguments sensibles si nécessaire (ex: mots de passe)
        safe_args = []
        for arg in args:
            if isinstance(arg, str) and len(arg) > 500:
                safe_args.append(f"{arg[:50]}... [tronqué]")
            elif 'password' in str(arg).lower() or 'token' in str(arg).lower():
                safe_args.append("***SENSIBLE***")
            else:
                safe_args.append(str(arg))
        
        # Filtrer des arguments nommés sensibles
        safe_kwargs = {}
        for k, v in kwargs.items():
            if 'password' in k.lower() or 'token' in k.lower():
                safe_kwargs[k] = "***SENSIBLE***"
            elif isinstance(v, str) and len(v) > 500:
                safe_kwargs[k] = f"{v[:50]}... [tronqué]"
            else:
                safe_kwargs[k] = v
                
        # Log des arguments
        args_str = ", ".join(safe_args)
        kwargs_str = ", ".join(f"{k}={v}" for k, v in safe_kwargs.items())
        all_args = ", ".join(filter(None, [args_str, kwargs_str]))
        
        func_logger.debug(f"APPEL {func_name}({all_args})")
        
        # Mesurer le temps d'exécution
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            # Si le résultat est très volumineux, ne pas le logger complètement
            str_result = str(result)
            if len(str_result) > 500:
                str_result = str_result[:100] + "... [tronqué]"
            
            # Calculer le temps d'exécution
            exec_time = time.time() - start_time
            
            # Log normal du résultat
            func_logger.debug(f"RETOUR {func_name}: {str_result}")
            
            # Log de performance si l'exécution a pris plus de 0.1 seconde
            if exec_time > 0.1:
                # Créer un log spécial avec attribut performance
                record = func_logger.makeRecord(
                    module_name, 
                    logging.INFO, 
                    func.__code__.co_filename, 
                    func.__code__.co_firstlineno,
                    f"Fonction {func_name} exécutée en {exec_time:.2f} secondes",
                    (), None
                )
                setattr(record, 'performance', True)
                for handler in func_logger.handlers:
                    handler.handle(record)
            
            return result
        except Exception as e:
            # Log d'erreur détaillé
            exec_time = time.time() - start_time
            func_logger.error(
                f"EXCEPTION dans {func_name} après {exec_time:.2f}s: "
                f"{type(e).__name__}: {str(e)}"
            )
            func_logger.error(traceback.format_exc())
            raise
    return wrapper

# Fonction pour mesurer la performance d'une section de code
@contextmanager
def log_performance(logger, section_name):
    """Context manager pour mesurer et logger le temps d'exécution d'une section de code"""
    start_time = time.time()
    try:
        yield
    finally:
        execution_time = time.time() - start_time
        # Créer un log spécial avec attribut performance
        record = logger.makeRecord(
            logger.name, 
            logging.INFO, 
            "", 
            0,
            f"Section {section_name} exécutée en {execution_time:.2f} secondes",
            (), None
        )
        setattr(record, 'performance', True)
        for handler in logger.handlers:
            handler.handle(record)

def purge_old_logs(days=30):
    """Supprime les fichiers de logs plus anciens que le nombre de jours spécifié"""
    logger = get_logger("log_management")
    logger.info(f"Purge des logs plus anciens que {days} jours")
    
    try:
        # Déterminer le répertoire de base en fonction du contexte d'exécution
        if getattr(sys, 'frozen', False):
            # Si on est dans un exécutable (PyInstaller)
            base_dir = os.path.dirname(sys.executable)
        else:
            # En développement
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
        log_folder = os.path.join(base_dir, "logs")
        if not os.path.exists(log_folder):
            logger.warning(f"Dossier de logs introuvable: {log_folder}")
            return
            
        now = time.time()
        count = 0
        
        for root, _, files in os.walk(log_folder):
            for file in files:
                if file.endswith(".txt"):
                    file_path = os.path.join(root, file)
                    if os.stat(file_path).st_mtime < now - days * 86400:
                        os.remove(file_path)
                        count += 1
                        logger.debug(f"Suppression de l'ancien log: {file_path}")
        
        logger.info(f"{count} fichiers de logs supprimés")
    except Exception as e:
        logger.error(f"Erreur lors de la purge des logs: {str(e)}")
        logger.error(traceback.format_exc())

def get_icon_path():
    """Obtient le chemin de l'icône de l'application"""
    logger = get_logger("utils.resources")
    possible_names = ['logo.ico', 'logo.png']
    
    try:
        if getattr(sys, 'frozen', False):
            exe_dir = os.path.dirname(sys.executable)
            # Chercher d'abord dans le dossier de l'exe
            for name in possible_names:
                icon_path = os.path.join(exe_dir, name)
                if os.path.exists(icon_path):
                    logger.debug(f"Icône trouvée: {icon_path}")
                    return icon_path
                    
            # Chercher dans le dossier assets du bundle
            for name in possible_names:
                icon_path = os.path.join(sys._MEIPASS, 'assets', name)
                if os.path.exists(icon_path):
                    logger.debug(f"Icône trouvée dans le bundle: {icon_path}")
                    return icon_path
        else:
            # Mode développement
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            for name in possible_names:
                icon_path = os.path.join(base_path, 'assets', name)
                if os.path.exists(icon_path):
                    logger.debug(f"Icône trouvée en développement: {icon_path}")
                    return icon_path
                    
        logger.warning("Aucune icône trouvée!")
        return None
        
    except Exception as e:
        logger.error(f"Erreur lors de la recherche de l'icône: {str(e)}")
        logger.error(traceback.format_exc())
        return None

def get_resource_path(relative_path):
    """Obtient le chemin absolu vers une ressource, fonctionne en développement et dans l'exécutable"""
    logger = get_logger("utils.resources")
    
    try:
        # Si on cherche l'icône, utiliser la fonction dédiée
        if relative_path.endswith(('logo.ico', 'logo.png')):
            icon_path = get_icon_path()
            if icon_path:
                return icon_path
                
        # Pour le reste des ressources
        if getattr(sys, 'frozen', False):
            exe_dir = os.path.dirname(sys.executable)
            
            # Essayer d'abord à côté de l'exe (prioritaire)
            direct_path = os.path.join(exe_dir, relative_path)
            if os.path.exists(direct_path):
                logger.info(f"Ressource trouvée à côté de l'exe: {direct_path}")
                return direct_path
            
            # Pour les templates, vérifier aussi sans le préfixe "templates/"
            if relative_path.startswith('templates/'):
                # Essai 1: dossier templates à côté de l'exe avec le nom du template
                template_name = os.path.basename(relative_path)
                template_path = os.path.join(exe_dir, 'templates', template_name)
                if os.path.exists(template_path):
                    logger.info(f"Template trouvé dans le dossier templates à côté de l'exe: {template_path}")
                    return template_path
                    
                # Essai 2: dossier dist/templates/ avec le nom du template
                dist_template_path = os.path.join(exe_dir, 'templates', template_name)
                if os.path.exists(dist_template_path):
                    logger.info(f"Template trouvé dans dist/templates/: {dist_template_path}")
                    return dist_template_path
            
            # Si toujours pas trouvé, essayer dans le dossier parent
            parent_dir = os.path.dirname(exe_dir)
            parent_path = os.path.join(parent_dir, relative_path)
            if os.path.exists(parent_path):
                logger.info(f"Ressource trouvée dans le dossier parent: {parent_path}")
                return parent_path
                
            # Pour les templates, essayer aussi dans le dossier parent/templates
            if relative_path.startswith('templates/'):
                template_name = os.path.basename(relative_path)
                parent_template_path = os.path.join(parent_dir, 'templates', template_name)
                if os.path.exists(parent_template_path):
                    logger.info(f"Template trouvé dans le dossier parent/templates/: {parent_template_path}")
                    return parent_template_path
            
            # Si toujours pas trouvé, chercher dans le bundle PyInstaller (faible priorité)
            if hasattr(sys, '_MEIPASS'):
                # Interrompre la recherche dans le bundle PyInstaller temporaire
                # pour forcer l'utilisation des templates externes
                logger.warning(f"Ignorons volontairement la recherche dans le bundle PyInstaller temporaire")
                
                # Mais tout de même, enregistrer l'information pour le débogage
                bundle_path = os.path.join(sys._MEIPASS, relative_path)
                if os.path.exists(bundle_path):
                    logger.warning(f"Ressource trouvée dans le bundle mais ignorée: {bundle_path}")
            
            # Imprimer tous les chemins tentés pour faciliter le débogage
            logger.warning(f"Chemins de recherche tentés pour '{relative_path}':")
            logger.warning(f"1. {direct_path}")
            if relative_path.startswith('templates/'):
                logger.warning(f"2. {template_path}")
                logger.warning(f"3. {dist_template_path}")
            logger.warning(f"4. {parent_path}")
            if relative_path.startswith('templates/'):
                logger.warning(f"5. {parent_template_path}")
            
            # Dernier essai, renvoyer le chemin direct même s'il n'existe pas
            logger.warning(f"Ressource non trouvée: {relative_path}, utilisation du chemin par défaut")
            return direct_path
        else:
            # Mode développement
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            dev_path = os.path.join(base_path, relative_path)
            logger.debug(f"Chemin de développement: {dev_path}")
            return dev_path
            
    except Exception as e:
        logger.error(f"Erreur lors de la résolution du chemin: {str(e)}")
        logger.error(traceback.format_exc())
        return relative_path

# Test immédiat pour vérifier que le système de logs fonctionne
logger.debug("Test de debug du système de logs")
logger.info("Test d'info du système de logs")
logger.warning("Test d'avertissement du système de logs")
logger.error("Test d'erreur du système de logs")
