from pathlib import Path
from flask import Blueprint, send_from_directory

bp = Blueprint("aurealis_network", __name__)

ROOT = Path(__file__).resolve().parent / "network"

@bp.get("/network/")
def network_home():
    return send_from_directory(ROOT, "index.html")

@bp.get("/network/<path:filename>")
def network_assets(filename):
    return send_from_directory(ROOT, filename)
