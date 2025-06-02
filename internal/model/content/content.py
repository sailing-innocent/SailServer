# -*- coding: utf-8 -*-
# @file content.py
# @brief The General Content Arena
# @author sailing-innocent
# @date 2025-05-22
# @version 1.0
# ---------------------------------

from internal.data.content import ContentNode, Content, ContentData, ContentNodeData
import logging

logger = logging.getLogger(__name__)


def clean_all_impl(db):
    db.query(Content).delete()
    db.query(ContentNode).delete()
    db.commit()


def content_from_data(create: ContentData):
    return Content(
        data=create.data,
        size=create.size,
    )


def data_from_content(content: Content):
    return ContentData(
        id=content.id,
        data=content.data,
        size=content.size,
    )


def create_content_impl(db, crt: ContentData):
    content = content_from_data(crt)
    db.add(content)
    db.commit()
    return content.id, content.size


def read_content_impl(db, content_id: int):
    content = db.query(Content).filter(Content.id == content_id).first()
    if content is None:
        return None
    return data_from_content(content)


def content_node_from_data(create: ContentNodeData):
    return ContentNode(
        raw_tags=create.raw_tags,
        tags=create.tags,
        content_id=create.content_id,
        start=create.start,
        offset=create.offset,
    )


def create_content_node_impl(db, crt: ContentNodeData):
    content_node = content_node_from_data(crt)
    db.add(content_node)
    db.commit()
    return content_node.id


def create_content_with_node_impl(db, crt: ContentData):
    cid, sz = create_content_impl(db, crt)
    # the auto binding full node
    node_crt = ContentNodeData(
        raw_tags="",
        tags="",
        content_id=cid,
        start=0,
        offset=sz,
    )
    return create_content_node_impl(db, node_crt)


def read_content_data_by_node_impl(db, node_id: int):
    node = db.query(ContentNode).filter(ContentNode.id == node_id).first()
    if node is None:
        return None
    content = db.query(Content).filter(Content.id == node.content_id).first()
    if content is None:
        return None
    if node.start + node.offset > content.size:
        logger.error("ContentNode out of range")
        return None

    return content.data[node.start : node.start + node.offset]
