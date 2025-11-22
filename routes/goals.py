from flask import Blueprint, jsonify, render_template, session, request, flash, redirect, url_for
from models.goal import Goal
from utils.helpers import load_reader
from utils.decorators import login_required
from utils.validators import validate_goal_form

goals_bp = Blueprint('goals', __name__)


@goals_bp.route("/goals", methods=["GET", "POST"])
@login_required
def goals():
    reader = load_reader()
    if not reader:
        flash("You must be logged in.")
        return redirect(url_for("auth.sign_in"))

    goals_data = [goal.to_dict() for goal in reader.goals]

    if request.method == "POST":
        form_data = request.form.to_dict()
        errors, target_value, current = validate_goal_form(form_data)

        if errors:
            return render_template(
                "goals/goals.html",
                goals=reader.goals,
                goals_data=goals_data,
                add_errors=errors,
                add_data=form_data,
                edit_data=None,
                edit_errors={}
            )

        deadline = form_data.get("deadline") or Goal.default_deadline(form_data.get("goal_type"))

        reader.add_goal(
            title=form_data["title"],
            unit=form_data.get("unit"),
            goal_type=form_data["goal_type"],
            target_value=target_value,
            deadline=deadline,
        )

        flash("Goal created successfully!")
        return redirect(url_for("goals.goals"))

    return render_template(
        "goals/goals.html",
        goals=reader.goals,
        goals_data=goals_data,
        add_data=None,
        add_errors={},
        edit_data=None,
        edit_errors={}
    )


@goals_bp.route("/goals/edit", methods=["POST"])
@login_required
def edit_goal():
    reader = load_reader()
    if not reader:
        return jsonify(success=False, errors={"general": "User not found"})

    goal_id = request.form.get("goal_id", "").strip()
    goal = reader.find_goal_by_id(goal_id)

    if not goal:
        return jsonify(success=False, errors={"general": "Goal not found"})

    errors, target_value, progress = validate_goal_form(request.form)

    if errors:
        return jsonify(success=False, errors=errors)

    deadline = request.form.get("deadline") or Goal.default_deadline(request.form.get("goal_type"))

    reader.edit_goal_by_id(
        goal_id,
        title=request.form.get("title") or goal.title,
        unit=request.form.get("unit", goal.unit),
        goal_type=request.form.get("goal_type", goal.goal_type),
        target_value=target_value,
        deadline=deadline,
        progress=progress
    )

    return jsonify(success=True)


@goals_bp.route("/goals/delete", methods=["POST"])
@login_required
def delete_goal():
    reader = load_reader()
    if not reader:
        flash("User not found!")
        return redirect(url_for("goals.goals"))

    goal_id = request.form.get("goal_id", "").strip()

    if not goal_id:
        flash("Missing goal ID")
        return redirect(url_for("goals.goals"))

    reader.delete_goal_by_id(goal_id)
    flash("Goal deleted successfully!")
    return redirect(url_for("goals.goals"))
