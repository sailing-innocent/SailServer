# -*- coding: utf-8 -*-
# @file world.py
# @brief The World Model
# @author sailing-innocent
# @date 2025-04-27
# @version 1.0
# ---------------------------------

from pydantic import BaseModel
from internal.data.world import Character, Setting, Story, Description, ContentNote

def clean_all_impl(db):
    db.query(ContentNote).delete()
    db.query(Description).delete()
    db.query(Story).delete()
    db.query(Setting).delete()
    db.query(Character).delete()
    db.commit()

# Character

class CharacterCreate(BaseModel):
    name: str
    data: bytes  # json binary

class CharacterRead(BaseModel):
    id: int
    name: str
    data: bytes  # json binary

def chracter_from_create(character_create: CharacterCreate) -> Character:
    return Character(
        name=character_create.name,
        data=character_create.data
    )

def read_from_character(character: Character) -> CharacterRead:
    return CharacterRead(
        id=character.id,
        name=character.name,
        data=character.data
    )

def create_character_impl(db, character_create: CharacterCreate) -> CharacterRead:
    character = chracter_from_create(character_create)
    db.add(character)
    db.commit()
    db.refresh(character)
    return read_from_character(character)

def get_character_impl(db, character_id: int) -> CharacterRead:
    character = db.query(Character).filter(Character.id == character_id).first()
    if character is None:
        return None
    return read_from_character(character)

# -- Setting

class SettingCreate(BaseModel):
    name: str
    data: bytes  # json binary

class SettingRead(BaseModel):
    id: int
    name: str
    data: bytes  # json binary

def setting_from_create(setting_create: SettingCreate) -> Setting:
    return Setting(
        name=setting_create.name,
        data=setting_create.data
    )

def read_from_setting(setting: Setting) -> SettingRead:
    return SettingRead(
        id=setting.id,
        name=setting.name,
        data=setting.data
    )

def create_setting_impl(db, setting_create: SettingCreate) -> SettingRead:
    setting = setting_from_create(setting_create)
    db.add(setting)
    db.commit()
    db.refresh(setting)
    return read_from_setting(setting)

def get_setting_impl(db, setting_id: int) -> SettingRead:
    setting = db.query(Setting).filter(Setting.id == setting_id).first()
    if setting is None:
        return None
    return read_from_setting(setting)

def update_setting_impl(db, setting_id: int, setting_update: SettingCreate) -> SettingRead:
    setting = db.query(Setting).filter(Setting.id == setting_id).first()
    if setting is None:
        return None
    if setting_update.name is not None:
        setting.name = setting_update.name
    if setting_update.data is not None:
        setting.data = setting_update.data
    db.commit()
    db.refresh(setting)
    return read_from_setting(setting)

# -- Story
class StoryCreate(BaseModel):
    name: str
    content_node_id: int
    data: bytes  # json binary

class StoryRead(BaseModel):
    id: int
    name: str
    content_node_id: int
    data: bytes  # json binary

def story_from_create(story_create: StoryCreate) -> Story:
    return Story(
        name=story_create.name,
        content_node_id=story_create.content_node_id,
        data=story_create.data
    )

def read_from_story(story: Story) -> StoryRead:
    return StoryRead(
        id=story.id,
        name=story.name,
        content_node_id=story.content_node_id,
        data=story.data
    )

def create_story_impl(db, story_create: StoryCreate) -> StoryRead:
    story = story_from_create(story_create)
    db.add(story)
    db.commit()
    db.refresh(story)
    return read_from_story(story)

def get_story_impl(db, story_id: int) -> StoryRead:
    story = db.query(Story).filter(Story.id == story_id).first()
    if story is None:
        return None
    return read_from_story(story)

def get_storys_by_content_node_impl(db, content_node_id: int) -> list[StoryRead]:
    stories = db.query(Story).filter(Story.content_node_id == content_node_id).all()
    if stories is None:
        return None
    return [read_from_story(story) for story in stories]

# -- Description
class DescriptionCreate(BaseModel):
    content_node_id: int
    data: bytes  # json binary

class DescriptionRead(BaseModel):
    id: int
    content_node_id: int
    data: bytes  # json binary

def description_from_create(description_create: DescriptionCreate) -> Description:
    return Description(
        content_node_id=description_create.content_node_id,
        data=description_create.data
    )

def read_from_description(description: Description) -> DescriptionRead:
    return DescriptionRead(
        id=description.id,
        content_node_id=description.content_node_id,
        data=description.data
    )

def create_description_impl(db, description_create: DescriptionCreate) -> DescriptionRead:
    description = description_from_create(description_create)
    db.add(description)
    db.commit()
    db.refresh(description)
    return read_from_description(description)

def get_description_impl(db, description_id: int) -> DescriptionRead:
    description = db.query(Description).filter(Description.id == description_id).first()
    if description is None:
        return None
    return read_from_description(description)

