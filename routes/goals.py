import calendar
from datetime import date, timedelta
from flask import Blueprint, render_template,session,request,flash,redirect,url_for
from utils.helpers import load_reader
from utils.decorators import login_required


goals_bp = Blueprint('goals', __name__)

@goals_bp.route("/goals", methods=["GET", "POST"])
@login_required
def goals():

    reader = load_reader()
    if not reader:
        flash("You must be logged in.")
        return redirect(url_for("auth.sign_in"))

    if request.method == "POST":
        title = request.form["title"]
        goal_type = request.form["goal_type"]
        deadline = request.form.get("deadline") or None
        target_value_raw = request.form.get("target_value", "").strip()

        errors = {}

        if not target_value_raw:
            errors["target_value"] = "Target value cannot be empty."
        else:
            try:
                target_value = int(target_value_raw)
                if target_value <= 0:
                    errors["target_value"] = "Target value must be greater than 0."
            except ValueError:
                errors["target_value"] = "Target value must be a valid number."

        if goal_type == "Custom" and not deadline:
            errors["deadline"] = "Deadline is required for custom goals."

        if errors:
            return render_template("goals.html", goals=reader.goals, add_errors=errors, add_data=request.form)

        today = date.today()
        if not deadline:
            if goal_type == "Daily":
                deadline = today.isoformat()
            elif goal_type == "Weekly":
                deadline = (today + timedelta(days=7)).isoformat()
            elif goal_type == "Monthly":
                month = today.month + 1
                year = today.year
                if month > 12:
                    month = 1
                    year += 1
                day = min(today.day, calendar.monthrange(year, month)[1])
                deadline = date(year, month, day).isoformat()
            elif goal_type == "Annual":
                deadline = date(today.year + 1, today.month, today.day).isoformat()

        reader.add_goal(title, goal_type, target_value, deadline)
        flash("Goal created successfully!")
        return redirect(url_for("goals.goals"))

    return render_template("goals.html", goals=reader.goals)


@goals_bp.route("/goals/edit", methods=["POST"])
def edit_goal():
    reader = load_reader()
    if not reader:
        flash("User not found!")
        return redirect(url_for("goals.goals"))

    goal_id = request.form.get("goal_id", "").strip()
    if not goal_id:
        flash("Missing goal identifier.")
        return redirect(url_for("goals.goals"))

    goal = reader.find_goal_by_id(goal_id)
    if not goal:
        flash("Goal not found.")
        return redirect(url_for("goals.goals"))


    title = request.form.get("title", "").strip()
    goal_type = request.form.get("goal_type", "Custom")
    deadline = request.form.get("deadline") or None
    target_raw = request.form.get("target", "").strip()
    progress_raw = request.form.get("current", "0").strip()

    errors = {}
    if not target_raw:
        errors["target"] = "Target is required."
    else:
        try:
            target_value = int(target_raw)
            if target_value <= 0:
                errors["target"] = "Target must be greater than 0."
        except ValueError:
            errors["target"] = "Target must be a number."

    try:
        progress = int(progress_raw) if progress_raw != "" else 0
        if progress < 0:
            errors["current"] = "Current progress cannot be negative."
        elif progress > target_value:
            errors["current"] = "Current progress cannot exceed target."
    except ValueError:
        errors["current"] = "Current must be a number."

    if goal_type == "Custom" and not deadline:
        errors["deadline"] = "Deadline is required for custom goals."

    if errors:
        edit_data = request.form.to_dict()
        edit_data['goal_id'] = goal_id
        return render_template("goals.html", goals=reader.goals, edit_errors=errors, edit_data=edit_data)

    if not deadline:
        today = date.today()
        if goal_type == "Daily":
            deadline = today.isoformat()
        elif goal_type == "Weekly":
            deadline = (today + timedelta(days=7)).isoformat()
        elif goal_type == "Monthly":
            month = today.month + 1
            year = today.year
            if month > 12:
                month = 1
                year += 1
            day = min(today.day, calendar.monthrange(year, month)[1])
            deadline = date(year, month, day).isoformat()
        elif goal_type == "Annual":
            deadline = date(today.year + 1, today.month, today.day).isoformat()
        else:
            deadline = None

    reader.edit_goal_by_id(goal_id,
                           title=title or goal.title,
                           goal_type=goal_type,
                           target_value=target_value,
                           deadline=deadline,
                           progress=progress)
    flash("Goal updated successfully!")
    return redirect(url_for("goals.goals"))


@goals_bp.route("/goals/delete", methods=["POST"])
def delete_goal():
    reader = load_reader()
    if not reader:
        flash("User not found!")
        return redirect(url_for("goals.goals"))

    goal_id = request.form.get("goal_id", "").strip()
    if not goal_id:
        flash("Missing goal identifier.")
        return redirect(url_for("goals.goals"))

    if reader.delete_goal_by_id(goal_id):
        flash("Goal deleted successfully!")
    else:
        flash("Goal not found.")
    return redirect(url_for("goals.goals"))
