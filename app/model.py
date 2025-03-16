from faster_whisper import WhisperModel

# Charger le modèle une fois, avec optimisation pour CPU
model = WhisperModel(
    "medium",
    device="cpu",
    compute_type="float32",  # Quantification pour accélérer sur CPU soit int8 (khfifa) soit float32
    cpu_threads=4  # Utilise tous les cœurs de ton i7-11th (4 cœurs)
)