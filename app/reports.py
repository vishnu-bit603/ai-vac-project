import csv, io, json
from flask import Blueprint, render_template, abort, Response
from flask_login import login_required, current_user
from app.models import Review

reports_bp = Blueprint("reports", __name__)

@reports_bp.get("/history")
@login_required
def history():
    reviews = Review.query.filter_by(user_id=current_user.id).order_by(Review.created_at.desc()).all()
    return render_template("history.html", reviews=reviews)

@reports_bp.get("/<int:review_id>")
@login_required
def detail(review_id):
    review = Review.query.filter_by(id=review_id, user_id=current_user.id).first_or_404()
    return render_template("detail.html", review=review, result=json.loads(review.result_json))

@reports_bp.get("/<int:review_id>/csv")
@login_required
def csv_report(review_id):
    review = Review.query.filter_by(id=review_id, user_id=current_user.id).first_or_404()
    result = json.loads(review.result_json)
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Field", "Value"])
    for key, value in result.items():
        writer.writerow([key, "; ".join(map(str, value)) if isinstance(value, list) else value])
    writer.writerow(["Provider", review.provider])
    writer.writerow(["Model", review.model])
    response = Response(output.getvalue(), mimetype="text/csv")
    response.headers["Content-Disposition"] = f'attachment; filename="review-{review.id}.csv"'
    return response
