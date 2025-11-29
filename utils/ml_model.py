
import os
import joblib
import numpy as np

MODEL_PATH = "models/priority_model.pkl"   # same file your training script dumps
_model = None                              # cached after first call

def _load_model():
    """Lazy-load (so unit-tests don't choke on missing file)."""
    global _model
    if _model is None and os.path.isfile(MODEL_PATH):
        _model = joblib.load(MODEL_PATH)
    return _model

def predict_priority(difficulty: int, urgency: int, importance: int, duration: int) -> int:
    """
    Returns integer priority score 0-100.
    Order of magnitude should stay similar to your old heuristic so UI labels
    don't jump around between releases.
    """
    model = _load_model()
    if model is None:                       # fallback until model exists
        # transparent heuristic: 1-5 sliders → 4-100 range
        return int((difficulty + urgency + importance) * 8 + duration * 2)

    X = np.array([[difficulty, urgency, importance, duration]], dtype=np.float32)
    raw = model.predict(X)[0]               # regressor → float
    return max(0, int(round(raw)))          # guard against negative preds