# ====================================================
# 🔧 PATH SETUP (MUST BE AT VERY TOP)
# ====================================================
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Add local ML repos to Python path
sys.path.insert(0, os.path.join(BASE_DIR, "GroundingDINO"))
sys.path.insert(0, os.path.join(BASE_DIR, "Grounded-Segment-Anything"))

# ====================================================
# 📦 STANDARD IMPORTS
# ====================================================
import time
from flask import Flask, render_template, request

# ====================================================
# 🚀 APP INITIALIZATION
# ====================================================
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB uploads

# ====================================================
# 🧠 MODULE IMPORTS (AFTER sys.path FIX)
# ====================================================
from modules.background import replace_wall
from modules.flooring import replace_floor
from modules.product_color import product_color
from modules.multicolor import detect_multicolors, modify_detected_color
from modules.object_change import replace_accessory
from modules.product_replace import analyze_image, replace_product


# ====================================================
# 🏠 DASHBOARD
# ====================================================
@app.route("/")
def index():
    return render_template("index.html")


# ====================================================
# 🟦 BACKGROUND
# ====================================================
@app.route("/background", methods=["GET", "POST"])
def background():
    output = None
    if request.method == "POST":
        output = replace_wall(request)
    return render_template("background.html", output=output)


# ====================================================
# 🟫 FLOORING
# ====================================================
@app.route("/flooring", methods=["GET", "POST"])
def flooring():
    output = None
    if request.method == "POST":
        output = replace_floor(request)
    return render_template("flooring.html", output=output)


# ====================================================
# 🎨 PRODUCT COLOR
# ====================================================
@app.route("/product-color", methods=["GET", "POST"])
def product_color_view():
    results = None
    ts = None
    if request.method == "POST":
        results, ts = product_color(request)
    return render_template("product_color.html", results=results, ts=ts)


# ====================================================
# 🌈 MULTI COLOR
# ====================================================
@app.route("/multi-color", methods=["GET", "POST"])
def multi_color():
    detected_color_list = None
    multicolor_filename = None
    ts = None

    if request.method == "POST":
        detected_color_list, multicolor_filename, ts = detect_multicolors(request)

    return render_template(
        "multicolor.html",
        detected_color_list=detected_color_list,
        multicolor_filename=multicolor_filename,
        ts=ts
    )


# ====================================================
# 🌈 MODIFY MULTI COLOR
# ====================================================
@app.route("/modify-detected-color", methods=["POST"])
def apply_detected_color():
    detected_result, ts = modify_detected_color(request)
    return render_template(
        "multicolor.html",
        detected_result=detected_result,
        ts=ts
    )


# ====================================================
# 🧱 OBJECT CHANGE
# ====================================================
@app.route("/object-change", methods=["GET", "POST"])
def object_change():
    replaced_accessory_image = None
    ts = None

    if request.method == "POST":
        replaced_accessory_image, ts = replace_accessory(request)

    return render_template(
        "object_change.html",
        replaced_accessory_image=replaced_accessory_image,
        ts=ts
    )


# ====================================================
# 🛏️ PRODUCT REPLACE – STEP 1 (ANALYZE)
# ====================================================
@app.route("/product-replace", methods=["GET", "POST"])
def product_replace_view():
    items = None
    setup_path = None

    if request.method == "POST":
        items, setup_path = analyze_image(request)

        if not isinstance(items, list):
            raise RuntimeError("items must be a list")

    return render_template(
        "product_replace.html",
        items=items,
        setup_path=setup_path
    )


# ====================================================
# 🛏️ PRODUCT REPLACE – STEP 2 (REPLACE)
# ====================================================
@app.route("/product-replace/replace", methods=["POST"])
def product_replace_action():
    output = replace_product(request)

    return render_template(
        "product_replace.html",
        output=output
    )


# ====================================================
# 🚀 RUN SERVER (DOCKER / AWS SAFE)
# ====================================================
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",   # REQUIRED for Docker & AWS
        port=5000,
        debug=False       # Disable debug in containers
    )
