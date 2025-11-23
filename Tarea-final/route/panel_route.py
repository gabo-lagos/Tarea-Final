from flask import Blueprint, render_template
from conection_with_mongo.conection_MongoDB import juguetes_col

panel_bp = Blueprint("panel_bp", __name__)


@panel_bp.route("/")
def dashboard():
    juguetes = list(juguetes_col.find({}, {"_id": 0}))
    return render_template("dashboard.html", juguetes=juguetes)