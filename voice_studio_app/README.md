# VoiceStudio - Application de Conversion Vocale

![VoiceStudio Logo](https://img.shields.io/badge/VoiceStudio-1.0-6a11cb?style=for-the-badge)
![Licence](https://img.shields.io/badge/Licence-MIT-blue?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.6+-green?style=flat-square)
![Flask](https://img.shields.io/badge/Flask-2.2.3-red?style=flat-square)

VoiceStudio est une application web locale de conversion vocale inspirée de MangioRVC et Applio. Elle permet d'entraîner des modèles vocaux, d'importer des fichiers modèles et d'utiliser la synthèse vocale (TTS) pour générer des fichiers audio à partir de texte.

## Fonctionnalités

### 1. Entraînement de Modèles Vocaux
- Configuration complète des paramètres d'entraînement
- Détection automatique du matériel (GPU)
- Sélection d'algorithmes d'extraction de pitch
- Sauvegarde des modèles et des index

### 2. Import et Gestion de Fichiers
- Upload de fichiers .pth et .index
- Téléchargement depuis URL
- Bibliothèque de modèles pré-entraînés
- Gestion des modèles importés

### 3. Synthèse Vocale (TTS)
- Conversion de texte en parole
- Support de multiples voix TTS
- Import de fichiers texte
- Contrôle de la vitesse de lecture
- Génération et téléchargement de fichiers audio

## Installation

### Prérequis
- Python 3.6 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. **Cloner ou télécharger le projet**
   ```
   git clone <url-du-repo> voice_studio_app
   cd voice_studio_app
   ```
   Ou décompressez l'archive téléchargée.

2. **Créer un environnement virtuel Python**
   ```
   python -m venv venv
   ```

3. **Activer l'environnement virtuel**
   - Windows:
     ```
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```
     source venv/bin/activate
     ```

4. **Installer les dépendances**
   ```
   pip install -r requirements.txt
   ```

## Utilisation

### Démarrer l'application
```
python app.py
```
L'application sera accessible à l'adresse: http://localhost:5000

### Page d'Entraînement

1. Configurez les paramètres d'entraînement:
   - Nom de l'expérience
   - Taux d'échantillonnage
   - Paramètres GPU
   - Algorithme d'extraction de pitch

2. Sélectionnez le dossier d'entraînement contenant vos fichiers audio

3. Lancez l'entraînement en cliquant sur "Entraîner le modèle" ou "Entraîner l'index de caractéristiques"

### Page d'Import

1. Importez des fichiers modèles de trois façons:
   - Glisser-déposer des fichiers .pth ou .index
   - Télécharger depuis une URL
   - Sélectionner un modèle pré-entraîné

2. Consultez la liste des modèles importés en bas de la page

### Page TTS (Text-to-Speech)

1. Sélectionnez:
   - Un modèle vocal (optionnel)
   - Un fichier d'index (optionnel)
   - Une voix TTS
   - La vitesse de lecture

2. Entrez du texte ou importez un fichier texte

3. Cliquez sur "Convertir" pour générer l'audio

4. Écoutez, téléchargez ou effacez l'audio généré

## Architecture du Projet

```
voice_studio_app/
├── app.py                  # Application Flask principale
├── requirements.txt        # Dépendances Python
├── static/                 # Fichiers statiques
│   ├── css/                # Feuilles de style
│   │   └── style.css       # Style principal
│   ├── js/                 # Scripts JavaScript
│   │   └── main.js         # Script principal
│   ├── img/                # Images
│   └── uploads/            # Fichiers uploadés
│       ├── models/         # Modèles vocaux
│       └── audio/          # Fichiers audio générés
└── templates/              # Templates HTML
    ├── base.html           # Template de base
    ├── train.html          # Page d'entraînement
    ├── download.html       # Page d'import
    └── tts.html            # Page TTS
```

## Fonctionnement Hors Ligne

VoiceStudio est conçu pour fonctionner entièrement en local, sans nécessiter de connexion internet. Toutes les fonctionnalités sont disponibles hors ligne:

- Les modèles sont stockés localement
- La synthèse vocale utilise des moteurs locaux (pyttsx3 et gTTS en mode hors ligne)
- Aucune donnée n'est envoyée à des serveurs externes

## Technologies Utilisées

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Synthèse Vocale**: gTTS, pyttsx3
- **Interface**: Bootstrap 5

## Dépannage

### Problèmes courants

1. **Erreur lors du lancement de l'application**
   - Vérifiez que toutes les dépendances sont installées
   - Assurez-vous que le port 5000 n'est pas déjà utilisé

2. **Fichiers audio non générés**
   - Vérifiez que les dossiers `static/uploads/audio` et `static/uploads/models` existent et sont accessibles en écriture
   - Assurez-vous que les bibliothèques TTS sont correctement installées

3. **Interface non responsive**
   - Videz le cache de votre navigateur
   - Essayez un autre navigateur (Chrome, Firefox)

## Contribution

Les contributions sont les bienvenues! Pour contribuer:

1. Forkez le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/amazing-feature`)
3. Committez vos changements (`git commit -m 'Add some amazing feature'`)
4. Poussez vers la branche (`git push origin feature/amazing-feature`)
5. Ouvrez une Pull Request

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## Remerciements

- Inspiré par [MangioRVC](https://github.com/Mangio621/Mangio-RVC-Fork) et [Applio](https://github.com/IAHispano/Applio)
- Développé dans le cadre d'un projet académique
- Merci à tous les contributeurs des bibliothèques open source utilisées

---

Développé avec ❤️ par LAOUAD Ayoub
