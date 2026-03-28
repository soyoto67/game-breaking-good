#!/bin/bash

# 1. Création de la structure des dossiers
echo "Creating folder structure..."
mkdir -p assets/sprites assets/maps/tilesets assets/maps/levels assets/ui
mkdir -p src/core src/entities src/mechanics src/utils
mkdir -p data/save data/dialogues
mkdir -p docs builds

# 2. Création des fichiers Python de base (vides ou avec placeholders)
echo "Creating Python source files..."
touch src/main.py
touch src/settings.py
touch src/core/game.py
touch src/core/camera.py
touch src/entities/player.py
touch src/entities/npc.py
touch src/mechanics/flashback.py
touch src/utils/loader.py

# 3. Création du fichier de dépendances
echo "pygame-ce" > requirements.txt
echo "pytmx" >> requirements.txt

# 4. Git : Ajouter et Envoyer
echo "Pushing to GitHub..."
git add .
git commit -m "Structure complète du projet Chômeur (Python/Pygame-ce/Tiled)"
git push origin main

echo "Done! Ta structure est prête sur GitHub."
