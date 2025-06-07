from flask import Flask, render_template, request, jsonify, send_from_directory, url_for
import os
import json
import time
import base64
import uuid
import shutil
import wave
import struct
from werkzeug.utils import secure_filename
import pyttsx3
from gtts import gTTS
import io

app = Flask(__name__)

# Configuration
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
app.config['MODELS_FOLDER'] = os.path.join(app.config['UPLOAD_FOLDER'], 'models')
app.config['AUDIO_FOLDER'] = os.path.join(app.config['UPLOAD_FOLDER'], 'audio')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max upload

# Assurer que les dossiers existent
os.makedirs(app.config['MODELS_FOLDER'], exist_ok=True)
os.makedirs(app.config['AUDIO_FOLDER'], exist_ok=True)

# Routes principales
@app.route('/')
def index():
    return render_template('train.html')

@app.route('/train')
def train():
    return render_template('train.html')

@app.route('/download')
def download():
    return render_template('download.html')

@app.route('/tts')
def tts():
    return render_template('tts.html')

# API pour la page d'entraînement
@app.route('/api/train/analyze-folder', methods=['POST'])
def analyze_folder():
    data = request.json
    folder_path = data.get('folder_path')
    
    # Simuler l'analyse d'un dossier
    # Dans une vraie implémentation, on analyserait réellement le dossier
    return jsonify({
        "file_count": 24,
        "extensions": [".wav", ".mp3"],
        "total_size": 15000000,
        "formatted_size": "15.0 Mo"
    })

@app.route('/api/train/gpu-info', methods=['GET'])
def gpu_info():
    # Simuler la détection de GPU
    return jsonify({
        "gpus": [
            {
                "index": 0,
                "name": "NVIDIA GeForce RTX 3080",
                "memory": "10 GB"
            }
        ]
    })

@app.route('/api/train/start-training', methods=['POST'])
def start_training():
    data = request.json
    experiment_name = data.get('experiment_name', 'default_experiment')
    
    # Créer un dossier pour l'expérience
    experiment_dir = os.path.join(app.config['MODELS_FOLDER'], experiment_name)
    os.makedirs(experiment_dir, exist_ok=True)
    
    # Créer des fichiers simulés pour le modèle et l'index
    model_path = os.path.join(experiment_dir, f"{experiment_name}.pth")
    index_path = os.path.join(experiment_dir, f"{experiment_name}.index")
    
    # Écrire des données simulées dans les fichiers
    with open(model_path, 'w') as f:
        f.write(f"Simulated model file for {experiment_name}")
    
    with open(index_path, 'w') as f:
        f.write(f"Simulated index file for {experiment_name}")
    
    # Créer un fichier de configuration JSON
    config_path = os.path.join(experiment_dir, "config.json")
    with open(config_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    return jsonify({
        "status": "success",
        "message": f"Entraînement terminé pour {experiment_name}",
        "model_path": model_path,
        "index_path": index_path,
        "files_created": [model_path, index_path, config_path],
        "training_result": {
            "model_path": model_path,
            "index_path": index_path
        }
    })

@app.route('/api/train/train-index', methods=['POST'])
def train_index():
    data = request.json
    experiment_name = data.get('experiment_name', 'default_experiment')
    
    # Créer un dossier pour l'expérience s'il n'existe pas
    experiment_dir = os.path.join(app.config['MODELS_FOLDER'], experiment_name)
    os.makedirs(experiment_dir, exist_ok=True)
    
    # Créer un fichier d'index simulé
    index_path = os.path.join(experiment_dir, f"{experiment_name}.index")
    
    # Écrire des données simulées dans le fichier
    with open(index_path, 'w') as f:
        f.write(f"Simulated index file for {experiment_name}")
    
    return jsonify({
        "status": "success",
        "message": f"Index créé pour {experiment_name}",
        "index_path": index_path
    })

# API pour la page d'import
@app.route('/api/download/models', methods=['GET'])
def get_models():
    models = []
    
    # Parcourir le dossier des modèles pour trouver les fichiers .pth et .index
    for root, dirs, files in os.walk(app.config['MODELS_FOLDER']):
        for file in files:
            if file.endswith('.pth'):
                model_name = os.path.splitext(file)[0]
                model_dir = os.path.relpath(root, app.config['MODELS_FOLDER'])
                
                # Vérifier si un fichier index correspondant existe
                index_file = os.path.join(root, f"{model_name}.index")
                has_index = os.path.exists(index_file)
                
                models.append({
                    "name": model_name,
                    "path": os.path.join(model_dir, file),
                    "has_index": has_index
                })
    
    return jsonify({"models": models})

@app.route('/api/download/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "Aucun fichier n'a été envoyé"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "Aucun fichier sélectionné"}), 400
    
    if not (file.filename.endswith('.pth') or file.filename.endswith('.index')):
        return jsonify({"error": "Format de fichier non supporté. Seuls .pth et .index sont acceptés"}), 400
    
    # Sécuriser le nom de fichier
    filename = secure_filename(file.filename)
    
    # Déterminer le dossier de destination
    model_name = os.path.splitext(filename)[0]
    upload_dir = os.path.join(app.config['MODELS_FOLDER'], model_name)
    os.makedirs(upload_dir, exist_ok=True)
    
    # Sauvegarder le fichier
    file_path = os.path.join(upload_dir, filename)
    file.save(file_path)
    
    return jsonify({
        "status": "success",
        "message": f"Fichier {filename} importé avec succès",
        "file_path": file_path
    })

@app.route('/api/download/from-url', methods=['POST'])
def download_from_url():
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({"error": "URL non spécifiée"}), 400
    
    if not (url.endswith('.pth') or url.endswith('.index')):
        return jsonify({"error": "L'URL doit pointer vers un fichier .pth ou .index"}), 400
    
    # Extraire le nom de fichier de l'URL
    filename = secure_filename(os.path.basename(url))
    model_name = os.path.splitext(filename)[0]
    
    # Créer le dossier de destination
    download_dir = os.path.join(app.config['MODELS_FOLDER'], model_name)
    os.makedirs(download_dir, exist_ok=True)
    
    # Simuler le téléchargement en créant un fichier
    file_path = os.path.join(download_dir, filename)
    with open(file_path, 'w') as f:
        f.write(f"Simulated download from {url}")
    
    return jsonify({
        "status": "success",
        "message": f"Fichier {filename} téléchargé avec succès",
        "file_path": file_path
    })

@app.route('/api/download/pretrained-model', methods=['POST'])
def download_pretrained_model():
    data = request.json
    model_id = data.get('model_id')
    sample_rate = data.get('sample_rate', '40k')
    
    if not model_id:
        return jsonify({"error": "ID de modèle non spécifié"}), 400
    
    # Créer le dossier de destination
    download_dir = os.path.join(app.config['MODELS_FOLDER'], model_id)
    os.makedirs(download_dir, exist_ok=True)
    
    # Créer les fichiers simulés
    model_path = os.path.join(download_dir, f"{model_id}.pth")
    index_path = os.path.join(download_dir, f"{model_id}.index")
    
    with open(model_path, 'w') as f:
        f.write(f"Simulated pretrained model {model_id} with sample rate {sample_rate}")
    
    with open(index_path, 'w') as f:
        f.write(f"Simulated index for {model_id} with sample rate {sample_rate}")
    
    return jsonify({
        "status": "success",
        "message": f"Modèle {model_id} téléchargé avec succès",
        "model_path": model_path,
        "index_path": index_path
    })

# API pour la page TTS
@app.route('/api/tts/voices', methods=['GET'])
def get_voices():
    voices = [
        {"id": "fr-FR-HenriNeural", "name": "Henri (Français)", "gender": "Male"},
        {"id": "fr-FR-DeniseNeural", "name": "Denise (Français)", "gender": "Female"},
        {"id": "fr-FR-AlainNeural", "name": "Alain (Français)", "gender": "Male"},
        {"id": "fr-FR-BrigitteNeural", "name": "Brigitte (Français)", "gender": "Female"},
        {"id": "fr-FR-CelesteNeural", "name": "Celeste (Français)", "gender": "Female"},
        {"id": "fr-CA-SylvieNeural", "name": "Sylvie (Français Canadien)", "gender": "Female"},
        {"id": "fr-CA-JeanNeural", "name": "Jean (Français Canadien)", "gender": "Male"},
        {"id": "en-US-GuyNeural", "name": "Guy (Anglais US)", "gender": "Male"},
        {"id": "en-US-JennyNeural", "name": "Jenny (Anglais US)", "gender": "Female"}
    ]
    return jsonify({"voices": voices})

@app.route('/api/tts/convert', methods=['POST'])
def convert_text():
    data = request.json
    text = data.get('text', '')
    tts_voice = data.get('tts_voice', '')
    tts_speed = data.get('tts_speed', 0)
    
    if not text:
        return jsonify({"error": "Texte non spécifié"}), 400
    
    # Générer un ID unique pour le fichier audio
    audio_id = str(uuid.uuid4())
    
    # Chemin du fichier audio à générer
    audio_path = os.path.join(app.config['AUDIO_FOLDER'], f"{audio_id}.wav")
    
    # Déterminer la langue en fonction de la voix sélectionnée
    lang = 'fr'
    if tts_voice.startswith('en'):
        lang = 'en'
    
    try:
        # Utiliser gTTS pour générer l'audio
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(audio_path)
        
        # Si la génération a réussi, renvoyer l'URL du fichier audio
        audio_url = url_for('static', filename=f'uploads/audio/{audio_id}.wav')
        
        return jsonify({
            "status": "success",
            "message": "Conversion terminée avec succès",
            "audio_url": audio_url,
            "audio_id": audio_id,
            "text": text
        })
    except Exception as e:
        # En cas d'erreur avec gTTS, essayer avec pyttsx3
        try:
            engine = pyttsx3.init()
            
            # Ajuster la vitesse si nécessaire
            if tts_speed != 0:
                rate = engine.getProperty('rate')
                new_rate = rate * (1 + tts_speed / 100)
                engine.setProperty('rate', new_rate)
            
            # Sélectionner une voix si possible
            voices = engine.getProperty('voices')
            for voice in voices:
                if lang in voice.id.lower():
                    engine.setProperty('voice', voice.id)
                    break
            
            # Sauvegarder l'audio
            engine.save_to_file(text, audio_path)
            engine.runAndWait()
            
            # Si la génération a réussi, renvoyer l'URL du fichier audio
            audio_url = url_for('static', filename=f'uploads/audio/{audio_id}.wav')
            
            return jsonify({
                "status": "success",
                "message": "Conversion terminée avec succès (pyttsx3)",
                "audio_url": audio_url,
                "audio_id": audio_id,
                "text": text
            })
        except Exception as e2:
            # Si les deux méthodes échouent, créer un fichier audio de test
            # Créer un fichier WAV simple avec un son de bip
            try:
                # Paramètres audio
                sample_rate = 44100  # Hz
                duration = 2.0       # secondes
                frequency = 440.0    # Hz (note A4)
                
                # Générer un son simple (onde sinusoïdale)
                samples = []
                for i in range(int(duration * sample_rate)):
                    sample = int(32767.0 * 0.5 * (1 + (i * frequency * 2 * 3.14159) / sample_rate))
                    samples.append(sample)
                
                # Écrire dans un fichier WAV
                with wave.open(audio_path, 'w') as wav_file:
                    wav_file.setparams((1, 2, sample_rate, int(duration * sample_rate), 'NONE', 'not compressed'))
                    wav_file.writeframes(struct.pack('h' * len(samples), *samples))
                
                audio_url = url_for('static', filename=f'uploads/audio/{audio_id}.wav')
                
                return jsonify({
                    "status": "success",
                    "message": "Conversion terminée avec succès (son de test)",
                    "audio_url": audio_url,
                    "audio_id": audio_id,
                    "text": text,
                    "note": "Utilisation d'un son de test car les moteurs TTS ont échoué"
                })
            except Exception as e3:
                return jsonify({
                    "error": f"Erreur lors de la conversion: {str(e)} / {str(e2)} / {str(e3)}"
                }), 500

@app.route('/api/tts/upload-text', methods=['POST'])
def upload_text_file():
    if 'file' not in request.files:
        return jsonify({"error": "Aucun fichier n'a été envoyé"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "Aucun fichier sélectionné"}), 400
    
    # Vérifier l'extension du fichier
    allowed_extensions = ['.txt', '.md', '.html']
    if not any(file.filename.lower().endswith(ext) for ext in allowed_extensions):
        return jsonify({"error": f"Format de fichier non supporté. Extensions acceptées: {', '.join(allowed_extensions)}"}), 400
    
    # Lire le contenu du fichier
    content = file.read().decode('utf-8')
    
    return jsonify({
        "status": "success",
        "filename": file.filename,
        "content": content[:500] + ("..." if len(content) > 500 else ""),  # Aperçu limité à 500 caractères
        "full_content": content
    })

# Lancement de l'application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
