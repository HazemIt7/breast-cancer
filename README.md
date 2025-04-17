# Mini-Projet Deep Learning : Classification du Cancer du Sein (BreaKHis)

**Auteur :** Hazem Ayachi
**Cours :** Deep Learning
**Date :** 17 Avril 2025

## Description

Ce projet met en œuvre et évalue différentes approches de Convolutional Neural Networks (CNN) pour la classification d'images histologiques de cancer du sein (bénin vs malin) à partir du dataset BreaKHis. Le projet couvre :
1.  La création et l'évaluation d'une CNN de base.
2.  L'amélioration des performances via l'augmentation de données.
3.  L'implémentation et l'évaluation du Transfer Learning (avec DenseNet121 et fine-tuning).
4.  Le déploiement du meilleur modèle en tant qu'API web sur Google Cloud Run à l'aide de Flask et Docker.


## Installation et Prérequis (Pour exécution locale)

* Python 3.8+
* Pip (gestionnaire de paquets Python)
* Docker Desktop (ou Docker Engine)
* Git

1.  **Cloner le dépôt :**
    ```bash
    git clone https://github.com/HazemIt7/breast-cancer.git
    cd breast-cancer
    ```

2.  **(Optionnel) Créer un environnement virtuel :**
    ```bash
    python -m venv venv
    # Sur Linux/macOS:
    source venv/bin/activate
    # Sur Windows:
    # venv\Scripts\activate
    ```

3.  **Installer les dépendances (pour l'API) :**
    ```bash
    pip install -r API/requirements.txt
    ```

## Exécution Locale

1.  **Notebook Jupyter :**
    * Lance Jupyter Lab ou Jupyter Notebook : `jupyter lab` ou `jupyter notebook`.
    * Ouvre le fichier `Project_Notebook.ipynb`.
    * **Important :** Le notebook nécessite l'accès au dataset BreaKHis. Assure-toi que le chemin vers le dataset dans le notebook est correct pour ton environnement local.
    * Lien pour télécharger la dataset: https://www.kaggle.com/datasets/ambarish/breakhis?select=BreaKHis_v1
    * L'exécution du notebook entraînera les modèles et affichera les résultats d'évaluation.

2.  **API Flask (Optionnel, pour test local) :**
    * Télécharge le fichier modèle `.keras` (voir section suivante) et place-le dans le dossier `API/`.
    * Navigue vers le dossier API : `cd API`
    * Lance le serveur Flask : `python main.py`
    * L'API sera accessible sur `http://localhost:8080` (ou un port similaire).

## Fichiers des Modèles Entraînés

Les modèles Keras entraînés (`.keras`) ne sont pas inclus directement dans ce dépôt Git en raison de leur taille.

Vous pouvez les télécharger depuis le dossier Google Drive suivant :
**[Lien vers les Modèles Entraînés](https://drive.google.com/drive/folders/1ZgiviKsET_5y17htsysXmxX8mDpUyJyJ?usp=sharing)**

Le modèle utilisé par l'API déployée est `transfer_learning_model.keras` (le modèle DenseNet121 fine-tuné).

## Déploiement Cloud et Instructions de Test

L'API de prédiction a été conteneurisée avec Docker et déployée sur **Google Cloud Run**.

* **URL de Base du Service :**
    [`https://breast-cancer-54106035782.europe-west1.run.app/`](https://breast-cancer-54106035782.europe-west1.run.app/)
    *(Vous pouvez tester cet URL de base dans un navigateur pour voir le "health check")*

* **Endpoint de Prédiction :**
    [`https://breast-cancer-54106035782.europe-west1.run.app/predict`](https://breast-cancer-54106035782.europe-west1.run.app/predict)

* **Comment Tester :**
    Pour obtenir une prédiction, envoyez une requête `POST` à l'endpoint `/predict`. La requête doit être de type `multipart/form-data` et contenir le fichier image sous la clé `file`.

    **Exemple avec `curl` :**
    ```bash
    # Remplacez /chemin/vers/votre/image.png par le chemin d'une image locale
    curl -X POST -F "file=@/chemin/vers/votre/image.png" https://breast-cancer-54106035782.europe-west1.run.app/predict
    ```
    *(Vous pouvez utiliser les images dans le dossier `sample_images/` de ce dépôt pour tester).*

    **Exemple avec Postman / Insomnia :**
    1.  Créez une nouvelle requête.
    2.  Méthode : `POST`.
    3.  URL : `https://breast-cancer-54106035782.europe-west1.run.app/predict`.
    4.  Allez dans l'onglet "Body", sélectionnez "form-data".
    5.  Entrez `file` comme "KEY".
    6.  Changez le type de la clé de "Text" à "File".
    7.  Cliquez sur "Select Files" et choisissez votre image.
    8.  Envoyez la requête ("Send").

* **Réponse Attendue :**
    L'API retournera une réponse JSON contenant la prédiction, similaire à ceci :
    ```json
    {
      "predicted_label": "Malignant",
      "confidence": 0.987654321,
      "raw_prediction": [0.01234567, 0.987654321]
    }
    ```
    *(Le label sera "Benign" ou "Malignant")*

## Rapport Détaillé

Le rapport complet du projet, détaillant la méthodologie, les résultats et la discussion, peut être trouvé dans ce répo
