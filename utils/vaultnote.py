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
    # 更灵活的正则表达式，允许更多格式变化
    NOTE_PATTERN = r"""---\s*
id:\s*(?P<note_id>[^\n]*)\s*
title:\s*(?P<title>[^\n]*)\s*
desc:\s*(?P<desc>[^\n]*)\s*
updated:\s*(?P<mtime>\d+).*?\s*
created:\s*(?P<ctime>\d+).*?\s*
---\s*
(?P<content>.*)"""

    result = re.search(NOTE_PATTERN, raw_content, re.DOTALL)
    if not result:
        # 如果主要模式匹配失败，尝试使用更宽松的备用模式
        ALT_PATTERN = r"""---\s*
id:\s*(?P<note_id>[^\n]*)\s*
.*?title:\s*(?P<title>[^\n]*)\s*
.*?desc:\s*(?P<desc>[^\n]*)\s*
.*?updated:\s*(?P<mtime>\d+).*?\s*
.*?created:\s*(?P<ctime>\d+).*?\s*
---\s*
(?P<content>.*)"""
        result = re.search(ALT_PATTERN, raw_content, re.DOTALL)

    if not result:
        logger.error(f"Failed to parse note with content: {raw_content[:200]}...")
        raise ValueError("Invalid note format")

    note_id = result.group("note_id")
    title = result.group("title")
    desc = result.group("desc")
    mtime = result.group("mtime")
    ctime = result.group("ctime")

    # logger.info(f">>> Note ID: {note_id}")
    assert len(note_id) > 0 and len(note_id) < 50
    # logger.info(f">>> Title: {title}")
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
