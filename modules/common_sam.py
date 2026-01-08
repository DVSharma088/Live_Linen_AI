# ====================================================
# Common SAM + GroundingDINO loader (CPU-safe, portable)
# ====================================================
import os
import torch
from groundingdino.util.inference import load_model
from segment_anything import sam_model_registry, SamPredictor

# ====================================================
# FORCE CPU
# ====================================================
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
DEVICE = torch.device("cpu")

# ====================================================
# BASE DIRECTORY
# ====================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# BASE_DIR -> SAM_Model/

# ====================================================
# PATHS (RELATIVE, PORTABLE)
# ====================================================
DINO_CONFIG = os.path.join(
    BASE_DIR,
    "GroundingDINO",
    "groundingdino",
    "config",
    "GroundingDINO_SwinT_OGC.py"
)

DINO_CHECKPOINT = os.path.join(
    BASE_DIR,
    "Grounded-Segment-Anything",
    "weights",
    "groundingdino_swint_ogc.pth"
)

SAM_CHECKPOINT = os.path.join(
    BASE_DIR,
    "sam_vit_b_01ec64.pth"
)

# ====================================================
# SANITY CHECKS (FAIL FAST)
# ====================================================
for path in [DINO_CONFIG, DINO_CHECKPOINT, SAM_CHECKPOINT]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"❌ Required file not found: {path}")

# ====================================================
# LOAD MODELS (ONCE)
# ====================================================
print("🔹 Loading DINO + SAM (CPU)")

dino_model = load_model(
    DINO_CONFIG,
    DINO_CHECKPOINT,
    device="cpu"
)

sam = sam_model_registry["vit_b"](checkpoint=SAM_CHECKPOINT)
sam.to(device=DEVICE)

sam_predictor = SamPredictor(sam)
