from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user

from app import db
from app.models import Note

notes_bp = Blueprint("notes", __name__)


def _get_owned_note_or_404(note_id):
    """Fetch a note by id, but block access if it doesn't belong to the current user."""
    note = Note.query.get_or_404(note_id)
    if note.user_id != current_user.id:
        abort(403)
    return note


@notes_bp.route("/")
@login_required
def list_notes():
    q = request.args.get("q", "").strip()
    query = Note.query.filter_by(user_id=current_user.id)

    if q:
        like = f"%{q}%"
        query = query.filter((Note.title.ilike(like)) | (Note.content.ilike(like)))

    notes = query.order_by(Note.updated_at.desc()).all()
    return render_template("notes/list.html", notes=notes, q=q)


@notes_bp.route("/new", methods=["GET", "POST"])
@login_required
def create_note():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()

        if not title or not content:
            flash("Title and content are both required.", "error")
            return render_template("notes/create.html", title=title, content=content)

        note = Note(title=title, content=content, user_id=current_user.id)
        db.session.add(note)
        db.session.commit()

        flash("Note saved.", "success")
        return redirect(url_for("notes.view_note", note_id=note.id))

    return render_template("notes/create.html")


@notes_bp.route("/<int:note_id>")
@login_required
def view_note(note_id):
    note = _get_owned_note_or_404(note_id)
    return render_template("notes/view.html", note=note)


@notes_bp.route("/<int:note_id>/edit", methods=["GET", "POST"])
@login_required
def edit_note(note_id):
    note = _get_owned_note_or_404(note_id)

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()

        if not title or not content:
            flash("Title and content cannot be empty.", "error")
            return render_template("notes/edit.html", note=note)

        note.title = title
        note.content = content
        db.session.commit()

        flash("Changes saved.", "success")
        return redirect(url_for("notes.view_note", note_id=note.id))

    return render_template("notes/edit.html", note=note)


@notes_bp.route("/<int:note_id>/delete", methods=["POST"])
@login_required
def delete_note(note_id):
    note = _get_owned_note_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    flash("Note deleted.", "success")
    return redirect(url_for("notes.list_notes"))
