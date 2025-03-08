from gtts import gTTS
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os

router = APIRouter()

# Spécifier le répertoire de sortie
output_directory = "outputs"
os.makedirs(output_directory, exist_ok=True)  # Créer le répertoire s'il n'existe pas


@router.post("/synthesize_ar/")
async def synthesize_text_ar(text: str):
    try:
        # Générer l'audio à partir du texte en arabe
        tts = gTTS(text=text, lang='ar')

        # Spécifier le chemin du fichier de sortie
        output_path = os.path.join(output_directory, "output_ar.mp3")

        # Sauvegarder l'audio dans le fichier
        tts.save(output_path)

        # Retourner le fichier audio généré
        return FileResponse(output_path, media_type="audio/mp3")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in TTS processing: {str(e)}")
