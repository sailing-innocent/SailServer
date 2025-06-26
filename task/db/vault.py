# -*- coding: utf-8 -*-
# @file vault.py
# @brief The Vault Control Tasks
# @author sailing-innocent
# @date 2025-05-21
# @version 1.0
# ---------------------------------
import logging

logger = logging.getLogger(__name__)
import os
from utils.vaultnote import parse_vault_note
from internal.model.content.vault import update_vault_note_by_note_id


def update_notes(db_func):
    logger.info("Updating notes...")
    db = next(db_func())
    vault_path = os.environ.get("VAULT_PATH", "/path/to/vault")
    if not os.path.exists(vault_path):
        logger.error(f"Vault path {vault_path} does not exist.")
        return

    to_update_file = os.path.join(vault_path, "to_update")
    with open(to_update_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    all_files = []
    failed_files = []
    # line_limit = 2
    for line in lines:
        # line_limit -= 1
        # if line_limit < 0:
        #     return
        line = line.strip()
        if not line:
            continue
        note_f = os.path.join(vault_path, line)
        if os.path.exists(note_f):
            with open(note_f, "r", encoding="utf-8") as f:
                content = f.read()
            # logger.info(f"Updating {line} with content: {content}")
            try:
                note = parse_vault_note(content, "vault", note_f)
            except ValueError as e:
                logger.error(f"Failed to parse note {line}: {e}")
                continue
            logger.info(
                f"Parsed note: {note.note_id}, {note.title}, {note.desc}, {note.note_path}"
            )
            # Update or Create if not exists
            try:
                update_vault_note_by_note_id(db, note.note_id, note, or_create=True)
                logger.info(f"Updated note {note.note_path} successfully.")
            except Exception as e:
                logger.error(f"Failed to update note {note.note_id}: {e}")
                failed_files.append(note.note_path)
                continue

            all_files.append(note.note_path)
        else:
            logger.warning(f"File {line} does not exist.")

    # overwrite the to_update file with failed files
    with open(to_update_file, "w", encoding="utf-8") as f:
        for failed_file in failed_files:
            f.write(f"{failed_file}\n")
        f.write("\n")

    return f"Done {len(all_files) - len(failed_files)}/{len(all_files)}"
