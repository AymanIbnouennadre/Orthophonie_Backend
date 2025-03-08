from fastapi import APIRouter, UploadFile, File
import pytesseract
from PIL import Image
import numpy as np
import cv2

# ✅ Définition de Tesseract pour l'arabe
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# ✅ Initialisation du routeur pour l'API arabe
router = APIRouter()

# ✅ Fonction de prétraitement des images
def preprocess_image(img_bytes):
    nparr = np.frombuffer(img_bytes, np.uint8)
    img_cv = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # 1. Convertir en niveaux de gris
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

    # 2. Augmenter le contraste
    contrasted = cv2.convertScaleAbs(gray, alpha=1.5, beta=0)

    # 3. Appliquer un seuil adaptatif (binarisation)
    adaptive_threshold = cv2.adaptiveThreshold(
        contrasted, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2
    )

    return adaptive_threshold

# ✅ Route OCR en arabe
@router.post("/")
async def convert_image_to_text_ar(file: UploadFile = File(...)):
    try:
        # Lire l'image envoyée par l'utilisateur
        img_bytes = await file.read()
        processed_img = preprocess_image(img_bytes)

        # Convertir en format PIL pour Tesseract
        img_pil = Image.fromarray(processed_img)

        # Tesseract pour l'arabe
        extracted_text = pytesseract.image_to_string(img_pil, lang='ara', config='--psm 6 --oem 3 --dpi 300')

        return {
            "extracted_text": extracted_text.strip()
        }

    except Exception as e:
        return {"error": str(e)}
