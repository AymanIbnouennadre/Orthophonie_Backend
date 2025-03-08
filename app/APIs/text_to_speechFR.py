from gtts import gTTS
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os

router = APIRouter()

# Spécifier le répertoire de sortie
output_directory = "outputs"
os.makedirs(output_directory, exist_ok=True)  # Créer le répertoire s'il n'existe pas


@router.post("/synthesize_fr/")
async def synthesize_text_fr(text: str):
    try:
        # Générer le son à partir du texte en français
        tts = gTTS(text=text, lang='fr')

        # Spécifier le chemin du fichier de sortie
        output_path = os.path.join(output_directory, "output_fr.mp3")

        # Sauvegarder l'audio dans le fichier
        tts.save(output_path)

        # Retourner le fichier audio généré
        return FileResponse(output_path, media_type="audio/mp3")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in TTS processing: {str(e)}")
