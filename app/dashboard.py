from flask import Blueprint, render_template
from flask_login import login_required, current_user
from sqlalchemy import func
from app.models import Review

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.get("/")
@login_required
def index():
    reviews = Review.query.filter_by(user_id=current_user.id).order_by(Review.created_at.desc()).limit(6).all()
    total = Review.query.filter_by(user_id=current_user.id).count()
    avg = Review.query.with_entities(func.avg(Review.quality_score)).filter_by(user_id=current_user.id).scalar()
    return render_template("dashboard.html", reviews=reviews, total=total, average=round(avg or 0))
