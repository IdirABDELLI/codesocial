"""import os
from dotenv import load_dotenv
from groq import Groq
import PyPDF2

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Obtenir la clé API depuis le fichier .env
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("Clé API non trouvée dans .env. Assurez-vous que GROQ_API_KEY est configuré.")

# Initialiser le client Groq
client = Groq(api_key=api_key)

# Fonction pour lire un fichier PDF et extraire son contenu
def lire_pdf(chemin_pdf):
    contenu = ""
    try:
        with open(chemin_pdf, "rb") as fichier:
            lecteur = PyPDF2.PdfReader(fichier)
            for page in lecteur.pages:
                texte = page.extract_text()
                if texte:
                    contenu += texte
    except Exception as e:
        print("Erreur lors de la lecture du PDF:", str(e))
    return contenu

# Fonction pour segmenter le texte en morceaux de taille spécifiée
def segmenter_texte(texte, taille_segment=10000):
    segments = []
    for i in range(0, len(texte), taille_segment):
        segments.append(texte[i:i + taille_segment])
    return segments

# Spécifiez le chemin vers votre fichier PDF ici
chemin_pdf = "Loris Rousseau - Retranscription.pdf"  # Remplacez par le chemin correct
texte_pdf = lire_pdf(chemin_pdf)

if not texte_pdf:
    raise ValueError("Le fichier PDF est vide ou n'a pas pu être lu.")

# Segmenter le texte en morceaux de 10 000 caractères
segments = segmenter_texte(texte_pdf, taille_segment=10000)

# Traiter chaque segment individuellement
for idx, segment in enumerate(segments):
    prompt = (
        "Tu es un sociologue. Analyse le texte suivant et génère une grille thématique "
        "avec trois colonnes : thème, code, verbatim. Chaque thème doit comporter environ "
        "10 codes, chacun illustré par un extrait pertinent du texte. Voici le texte :\n\n"
        f"{segment}"
    )
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.3-70b-versatile",
        )
        reponse = chat_completion.choices[0].message.content
        # Enregistrer la réponse dans un fichier texte
        nom_fichier = f"grille_thematique_segment_{idx + 1}.txt"
        with open(nom_fichier, "w", encoding="utf-8") as f:
            f.write(reponse)
        print(f"Segment {idx + 1} traité et enregistré dans {nom_fichier}")
    except Exception as e:
        print(f"Une erreur s'est produite lors du traitement du segment {idx + 1} :", str(e))



import os
import re
import pandas as pd
from dotenv import load_dotenv
from groq import Groq
import PyPDF2

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Obtenir la clé API depuis le fichier .env
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("Clé API non trouvée dans .env. Assurez-vous que GROQ_API_KEY est configuré.")

# Initialiser le client Groq
client = Groq(api_key=api_key)

# Fonction pour lire un fichier PDF et extraire son contenu
def lire_pdf(chemin_pdf):
    contenu = ""
    try:
        with open(chemin_pdf, "rb") as fichier:
            lecteur = PyPDF2.PdfReader(fichier)
            for page in lecteur.pages:
                texte = page.extract_text()
                if texte:
                    contenu += texte
    except Exception as e:
        print("Erreur lors de la lecture du PDF:", str(e))
    return contenu

# Fonction pour segmenter le texte en morceaux de taille spécifiée
def segmenter_texte(texte, taille_segment=10000):
    segments = []
    for i in range(0, len(texte), taille_segment):
        segments.append(texte[i:i + taille_segment])
    return segments

# Fonction pour analyser un segment et extraire les données
def analyser_segment(segment):
    prompt = (
        "Tu es un sociologue. Analyse le texte suivant et génère une grille thématique "
        "avec trois colonnes : thème, code, verbatim. Chaque thème doit comporter environ "
        "10 codes, chacun illustré par un extrait pertinent du texte. Voici le texte :\n\n"
        f"{segment}"
    )
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.3-70b-versatile",
        )
        reponse = chat_completion.choices[0].message.content
        return reponse
    except Exception as e:
        print("Une erreur s'est produite lors du traitement d'un segment :", str(e))
        return None

# Fonction pour extraire les données de la réponse du modèle
def extraire_donnees(reponse):
    lignes = reponse.strip().split("\n")
    donnees = []
    for ligne in lignes:
        # Supposer que les colonnes sont séparées par des tabulations ou des barres verticales
        if "\t" in ligne:
            parties = ligne.split("\t")
        elif "|" in ligne:
            parties = ligne.split("|")
        else:
            continue
        if len(parties) >= 3:
            theme = parties[0].strip()
            code = parties[1].strip()
            verbatim = "|".join(parties[2:]).strip()
            donnees.append({"Thème": theme, "Code": code, "Verbatim": verbatim})
    return donnees

# Spécifiez le chemin vers votre fichier PDF ici
chemin_pdf = "Loris Rousseau - Retranscription.pdf"  # Remplacez par le chemin correct
texte_pdf = lire_pdf(chemin_pdf)

if not texte_pdf:
    raise ValueError("Le fichier PDF est vide ou n'a pas pu être lu.")

# Segmenter le texte en morceaux de 10 000 caractères
segments = segmenter_texte(texte_pdf, taille_segment=10000)

# Traiter chaque segment et collecter les données
toutes_donnees = []
for idx, segment in enumerate(segments):
    print(f"Traitement du segment {idx + 1}/{len(segments)}...")
    reponse = analyser_segment(segment)
    if reponse:
        donnees = extraire_donnees(reponse)
        toutes_donnees.extend(donnees)

# Créer un DataFrame à partir des données collectées
df = pd.DataFrame(toutes_donnees)

# Générer le nom du fichier de sortie
nom_fichier_entree = os.path.splitext(os.path.basename(chemin_pdf))[0]
nom_fichier_sortie = f"codage_{nom_fichier_entree}.csv"

# Enregistrer le DataFrame dans un fichier CSV
df.to_csv(nom_fichier_sortie, index=False, encoding="utf-8")
print(f"Fichier CSV généré : {nom_fichier_sortie}")
"""
import os
from dotenv import load_dotenv
from groq import Groq
import PyPDF2

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Obtenir la clé API depuis le fichier .env
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("Clé API non trouvée dans .env. Assurez-vous que GROQ_API_KEY est configuré.")

# Initialiser le client Groq
client = Groq(api_key=api_key)

# Fonction pour lire un fichier PDF et extraire son contenu
def lire_pdf(chemin_pdf):
    contenu = ""
    try:
        with open(chemin_pdf, "rb") as fichier:
            lecteur = PyPDF2.PdfReader(fichier)
            for page in lecteur.pages:
                texte = page.extract_text()
                if texte:
                    contenu += texte
    except Exception as e:
        print("Erreur lors de la lecture du PDF:", str(e))
    return contenu

# Fonction pour segmenter le texte en morceaux de taille spécifiée
def segmenter_texte(texte, taille_segment=10000):
    segments = []
    for i in range(0, len(texte), taille_segment):
        segments.append(texte[i:i + taille_segment])
    return segments

# Spécifiez le chemin vers votre fichier PDF ici
chemin_pdf = "Loris Rousseau - Retranscription.pdf"  # Remplacez par le chemin correct
texte_pdf = lire_pdf(chemin_pdf)

if not texte_pdf:
    raise ValueError("Le fichier PDF est vide ou n'a pas pu être lu.")

# Segmenter le texte en morceaux de 10 000 caractères
segments = segmenter_texte(texte_pdf, taille_segment=10000)

# Traiter chaque segment individuellement
for idx, segment in enumerate(segments):
    prompt = (
        "Tu es un sociologue. Analyse le texte suivant et génère une grille thématique "
        "avec trois colonnes : thème, code, verbatim. Chaque thème doit comporter environ "
        "10 codes, chacun illustré par un extrait pertinent du texte. Voici le texte :\n\n"
        f"{segment}"
    )
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.3-70b-versatile",
        )
        reponse = chat_completion.choices[0].message.content
        # Enregistrer la réponse dans un fichier texte
        nom_fichier = f"grille_thematique_segment_{idx + 1}.txt"
        with open(nom_fichier, "w", encoding="utf-8") as f:
            f.write(reponse)
        print(f"Segment {idx + 1} traité et enregistré dans {nom_fichier}")
    except Exception as e:
        print(f"Une erreur s'est produite lors du traitement du segment {idx + 1} :", str(e))
