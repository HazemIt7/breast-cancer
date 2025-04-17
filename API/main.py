import os
import numpy as np
import tensorflow as tf
from flask import Flask, request, jsonify
from PIL import Image
import io

# Charger le modèle Keras (utilise .keras ou .h5 selon ton fichier)
MODEL_PATH = 'transfer_learning_model.keras' 
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    print(f"Modèle chargé depuis {MODEL_PATH}")
except Exception as e:
    print(f"Erreur lors du chargement du modèle: {e}")
    model = None # Important pour la suite

# Initialiser l'application Flask
app = Flask(__name__)

IMG_SIZE = (128, 128) 

def preprocess_image(image_bytes):
    """Prétraite les bytes d'une image pour le modèle."""
    try:
        img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        img = img.resize(IMG_SIZE)
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0) # Créer un batch
        img_array = img_array / 255.0 
        return img_array
    except Exception as e:
        print(f"Erreur de pré-traitement: {e}")
        return None

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "model_loaded": model is not None})

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
         return jsonify({"error": "Modèle non chargé"}), 500

    if 'file' not in request.files:
        return jsonify({"error": "Aucun fichier image fourni"}), 400

    file = request.files['file']
    if file.filename == '':
         return jsonify({"error": "Nom de fichier vide"}), 400

    try:
        img_bytes = file.read()
        processed_image = preprocess_image(img_bytes)

        if processed_image is None:
             return jsonify({"error": "Échec du pré-traitement de l'image"}), 400

        # Faire la prédiction
        prediction = model.predict(processed_image)

        predicted_class_index = np.argmax(prediction[0])
        confidence = float(prediction[0][predicted_class_index]) 
        labels = ['Bénin', 'Malin'] 
        predicted_label = labels[predicted_class_index]

        return jsonify({
            "predicted_label": predicted_label,
            "confidence": confidence,
            "raw_prediction": prediction[0].tolist() 
        })

    except Exception as e:
        print(f"Erreur de prédiction: {e}")
        return jsonify({"error": f"Erreur serveur lors de la prédiction: {e}"}), 500

if __name__ == '__main__':
    # Utiliser Gunicorn pour lancer en production, ceci est pour le test local
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))