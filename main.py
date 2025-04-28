import os
from dotenv import load_dotenv
from groq import Groq

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Obtenir la clé API depuis le fichier .env
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("Clé API non trouvée dans .env. Assurez-vous que GROQ_API_KEY est configuré.")

# Initialiser le client Groq
client = Groq(api_key=api_key)








# Faire une requête de complétion de chat
try:
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Explain the importance of fast language models",
            }
        ],
        model="llama-3.3-70b-versatile",
    )
    # Afficher le contenu de la réponse
    print("Réponse du modèle :", chat_completion.choices[0].message.content)
except Exception as e:
    print("Une erreur s'est produite :", str(e))
