#!/usr/bin/env python3
"""
Script pour incrémenter automatiquement la version du projet.
Incrémente le numéro de version dans le fichier version.txt.
"""

import os
import sys
import re

VERSION_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "version.txt")

def read_version():
    """Lit la version actuelle depuis le fichier"""
    if not os.path.exists(VERSION_FILE):
        print(f"Le fichier {VERSION_FILE} n'existe pas. Création avec version 1.0.0")
        write_version([1, 0, 0])
        return [1, 0, 0]
    
    with open(VERSION_FILE, 'r') as f:
        version_str = f.read().strip()
    
    pattern = r'(\d+)\.(\d+)\.(\d+)'
    match = re.match(pattern, version_str)
    
    if not match:
        print(f"Format de version invalide dans {VERSION_FILE}. Réinitialisation à 1.0.0")
        version = [1, 0, 0]
        write_version(version)
        return version
    
    return [int(match.group(1)), int(match.group(2)), int(match.group(3))]

def write_version(version):
    """Écrit la nouvelle version dans le fichier"""
    version_str = ".".join(map(str, version))
    with open(VERSION_FILE, 'w') as f:
        f.write(version_str)
    print(f"Version mise à jour : {version_str}")

def increment_version(version, level='patch'):
    """
    Incrémente la version selon le niveau spécifié
    - patch: 1.0.0 -> 1.0.1
    - minor: 1.0.0 -> 1.1.0 (et reset patch)
    - major: 1.0.0 -> 2.0.0 (et reset minor et patch)
    """
    major, minor, patch = version
    
    if level == 'patch':
        patch += 1
    elif level == 'minor':
        minor += 1
        patch = 0
    elif level == 'major':
        major += 1
        minor = 0
        patch = 0
    else:
        print(f"Niveau d'incrémentation inconnu: {level}. Utilisation de 'patch'")
        patch += 1
    
    return [major, minor, patch]

def main():
    """Fonction principale"""
    # Déterminer le niveau d'incrémentation depuis les arguments
    level = 'patch'  # Par défaut
    if len(sys.argv) > 1:
        level = sys.argv[1].lower()
        if level not in ['major', 'minor', 'patch']:
            print(f"Niveau invalide: {level}. Utilisation de 'patch'")
            level = 'patch'
    
    # Lire la version actuelle
    current_version = read_version()
    print(f"Version actuelle: {'.'.join(map(str, current_version))}")
    
    # Incrémenter la version
    new_version = increment_version(current_version, level)
    
    # Écrire la nouvelle version
    write_version(new_version)

if __name__ == "__main__":
    main()
