from http import HTTPStatus

from flask.views import MethodView
from flask_smorest import Blueprint, abort

from ..models import db, Note
from ..schemas import NoteCreateSchema, NoteSchema, NoteUpdateSchema

blp = Blueprint(
    "Notes",
    "notes",
    url_prefix="/notes",
    description="CRUD endpoints for managing notes"
)


@blp.route("/")
class NotesList(MethodView):
    """
    PUBLIC_INTERFACE
    get:
      summary: List notes
      description: Retrieve all notes ordered by most recently updated first.
    post:
      summary: Create note
      description: Create a new note with a title and content.
    """

    @blp.response(HTTPStatus.OK, NoteSchema(many=True))
    def get(self):
        """Return a list of all notes."""
        notes = Note.query.order_by(Note.updated_at.desc()).all()
        return [n.to_dict() for n in notes]

    @blp.arguments(NoteCreateSchema)
    @blp.response(HTTPStatus.CREATED, NoteSchema)
    def post(self, data):
        """Create a new note."""
        try:
            note = Note(title=data["title"].strip(), content=data["content"].strip())
            db.session.add(note)
            db.session.commit()
            return note.to_dict()
        except Exception:
            db.session.rollback()
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message="Failed to create note")


@blp.route("/<int:note_id>")
class NoteDetail(MethodView):
    """
    PUBLIC_INTERFACE
    get:
      summary: Get note by ID
      description: Retrieve a single note by its ID.
    put:
      summary: Update note by ID
      description: Update title and/or content of a note by its ID.
    delete:
      summary: Delete note by ID
      description: Delete a note permanently by its ID.
    """

    @blp.response(HTTPStatus.OK, NoteSchema)
    def get(self, note_id: int):
        """Retrieve a note."""
        note = Note.query.get(note_id)
        if not note:
            abort(HTTPStatus.NOT_FOUND, message="Note not found")
        return note.to_dict()

    @blp.arguments(NoteUpdateSchema)
    @blp.response(HTTPStatus.OK, NoteSchema)
    def put(self, data, note_id: int):
        """Update a note."""
        note = Note.query.get(note_id)
        if not note:
            abort(HTTPStatus.NOT_FOUND, message="Note not found")
        try:
            if "title" in data:
                note.title = data["title"].strip()
            if "content" in data:
                note.content = data["content"].strip()
            db.session.commit()
            return note.to_dict()
        except Exception:
            db.session.rollback()
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message="Failed to update note")

    @blp.response(HTTPStatus.NO_CONTENT)
    def delete(self, note_id: int):
        """Delete a note."""
        note = Note.query.get(note_id)
        if not note:
            abort(HTTPStatus.NOT_FOUND, message="Note not found")
        try:
            db.session.delete(note)
            db.session.commit()
            return ""
        except Exception:
            db.session.rollback()
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message="Failed to delete note")
