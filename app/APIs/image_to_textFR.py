from fastapi import APIRouter, UploadFile, File
from paddleocr import PaddleOCR
import numpy as np
from PIL import Image
import cv2

# ✅ Initialisation PaddleOCR pour le français
ocr_fr = PaddleOCR(use_angle_cls=True, lang='fr')

# ✅ Initialisation du routeur pour l'API française
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

# ✅ Route OCR en français
@router.post("/")
async def convert_image_to_text_fr(file: UploadFile = File(...)):
    try:
        # Lire l'image envoyée par l'utilisateur
        img_bytes = await file.read()
        processed_img = preprocess_image(img_bytes)

        # Convertir en format PIL pour PaddleOCR
        img_pil = Image.fromarray(processed_img)

        # PaddleOCR pour le français
        results = ocr_fr.ocr(np.array(img_pil), cls=True)
        extracted_text = " ".join([line[1][0] for line in results[0]])

        return {
            "extracted_text": extracted_text.strip()
        }

    except Exception as e:
        return {"error": str(e)}
