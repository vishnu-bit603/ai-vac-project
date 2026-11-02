import json
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Review
from app.ai_service import analyze_content

analysis_bp = Blueprint("analysis", __name__)

@analysis_bp.route("/new", methods=["GET", "POST"])
@login_required
def new():
    if request.method == "POST":
        title = request.form.get("title", "").strip()[:160]
        content = request.form.get("content", "").strip()
        provider = request.form.get("provider", "groq").lower()
        if len(content) < 40:
            flash("Please provide at least 40 characters for a useful review.", "error")
            return render_template("analysis.html")
        if len(content) > 30000:
            flash("Please keep the content under 30,000 characters.", "error")
            return render_template("analysis.html")
        try:
            result, model = analyze_content(content, provider)
            review = Review(
                user_id=current_user.id,
                title=title or result.get("title") or "Untitled review",
                content=content,
                provider=provider,
                model=model,
                quality_score=result["quality_score"],
                readability_score=result["readability_score"],
                originality_risk=result["originality_risk"],
                ai_style_estimate=result["ai_style_estimate"],
                result_json=json.dumps(result, ensure_ascii=False)
            )
            db.session.add(review)
            db.session.commit()
            return redirect(url_for("reports.detail", review_id=review.id))
        except Exception as exc:
            db.session.rollback()
            flash(f"Analysis failed: {exc}", "error")
    return render_template("analysis.html")
