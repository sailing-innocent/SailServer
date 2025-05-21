# -*- coding: utf-8 -*-
# @file vault.py
# @brief The Vault Model
# @author sailing-innocent
# @date 2025-05-21
# @version 1.0
# ---------------------------------

from internal.data.content import VaultNote, VaultNoteData
import logging

logger = logging.getLogger(__name__)


def create_vault_note_impl(db, note: VaultNoteData):
    # no id required
    note_orm = VaultNote(
        vault_name=note.vault_name,
        note_path=note.note_path,
        note_id=note.note_id,
        title=note.title,
        desc=note.desc,
        ctime=note.ctime,
        mtime=note.mtime,
        tags=note.tags,
        content=note.content,
    )
    db.add(note_orm)
    db.commit()
    return note_orm.id


def get_vault_note_impl(db, id: int):
    note = db.query(VaultNote).filter(VaultNote.id == id).first()
    if not note:
        logger.warning(f"Vault note with id {id} not found.")
        return None
    return note


def update_vault_note_impl(db, id: int, note: VaultNoteData):
    note_orm = db.query(VaultNote).filter(VaultNote.id == id).first()
    if not note_orm:
        logger.warning(f"Vault note with id {id} not found.")
        return None
    for key, value in note.dict().items():
        setattr(note_orm, key, value)
    db.commit()
    return note_orm


def update_vault_note_by_note_id(
    db, note_id: str, note: VaultNoteData, or_create: bool = False
):
    note_orm: VaultNote = (
        db.query(VaultNote).filter(VaultNote.note_id == note_id).first()
    )
    if not note_orm:
        if or_create:
            return create_vault_note_impl(db, note)
        logger.warning(f"Vault note with note_id {note_id} not found.")
        return None

    note_orm.vault_name = note.vault_name
    note_orm.note_path = note.note_path
    note_orm.title = note.title
    note_orm.desc = note.desc
    note_orm.ctime = note.ctime
    note_orm.mtime = note.mtime
    note_orm.tags = note.tags
    note_orm.content = note.content
    db.commit()
    return note_orm


def delete_vault_note_impl(db, id: int):
    note = db.query(VaultNote).filter(VaultNote.id == id).first()
    if not note:
        logger.warning(f"Vault note with id {id} not found.")
        return None
    db.delete(note)
    db.commit()
    return note


def delete_vault_note_by_note_id_impl(db, note_id: str):
    note = db.query(VaultNote).filter(VaultNote.note_id == note_id).first()
    if not note:
        logger.warning(f"Vault note with note_id {note_id} not found.")
        return None
    db.delete(note)
    db.commit()
    return note
