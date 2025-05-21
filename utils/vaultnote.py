# -*- coding: utf-8 -*-
# @file vaultnote.py
# @brief The VaultNote Utility
# @author sailing-innocent
# @date 2025-05-21
# @version 1.0
# ---------------------------------

import re
from internal.data.content import VaultNoteData
import logging

logger = logging.getLogger(__name__)


def parse_vault_note(
    raw_content: str, vault_name: str, note_path: str
) -> VaultNoteData:
    NOTE_PATTERN = r"""---
id: (?P<note_id>.*)
title: (?P<title>.*)
desc: (?P<desc>.*)
updated: (?P<mtime>\d+)
created: (?P<ctime>\d+).*?
---
(?P<content>.*)"""

    result = re.search(NOTE_PATTERN, raw_content, re.DOTALL)
    if not result:
        raise ValueError("Invalid note format")
    note_id = result.group("note_id")
    title = result.group("title")
    desc = result.group("desc")
    mtime = result.group("mtime")
    ctime = result.group("ctime")
    # logger.info(f"Parsed note: {note_id}, {title}, {desc}, {mtime}, {ctime}")

    return VaultNoteData(
        vault_name=vault_name,
        note_path=note_path,
        note_id=note_id,
        title=title,
        desc=desc,
        ctime=int(ctime) // 1000,
        mtime=int(mtime) // 1000,
        tags="",
        content=raw_content,
    )
