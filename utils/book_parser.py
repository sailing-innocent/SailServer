# -*- coding: utf-8 -*-
# @file book_parser.py
# @brief A simple book parser
# @author sailing-innocent
# @date 2025-01-31
# @version 1.0
# ---------------------------------

class BPBook:
    def __init__(self, title, author, preface, chapters):
        self.title = title
        self.author = author
        self.preface = preface
        self.chapters = chapters

    def __str__(self):
        return f"Book: {self.title}, {self.author}, {len(self.chapters)} chapters"

    def __repr__(self):
        return f"Book: {self.title}, {self.author}, {len(self.chapters)} chapters"

    def __len__(self):
        return len(self.chapters)

    def __getitem__(self, key):
        return self.chapters[key]


class BPChapter:
    def __init__(self, title, content):
        self.title = title
        self.content = content

    def __str__(self):
        return f"Chapter: {self.title}, {len(self.content)} characters"

    def __repr__(self):
        return f"Chapter: {self.title}, {len(self.content)} characters"

    def __len__(self):
        return len(self.content)

    def __getitem__(self, key):
        return self.content[key]


def is_chapter_title(line):
    first_part = line.split(" ")[0]
    special_tags = [
        "尾声",
        "后记",
        "附录",
        "序言",
        "序",
        "楔子",
        "前言",
        "引子",
        "序幕",
        "序章",
    ]
    if first_part.startswith("第") and first_part.endswith("回"):
        return True
    if first_part.startswith("第") and first_part.endswith("章"):
        return True
    if first_part in special_tags:
        return True
    return False


class BookParser:
    # A StateMachine that parses novel text
    def __init__(self, title, author):
        self.state = "start"
        self.book = None
        self.title = title
        self.author = author
        self.preface = ""
        self.chapter_title = ""
        self.chapter_content = ""
        self.chapters = []

    def parse(self, lines):
        for line in lines:
            line = line.strip()
            if self.state == "start":
                self.state = "preface"
            elif self.state == "preface":
                if line == "正文":
                    self.state = "chapter"
                else:
                    self.preface += line
            elif self.state == "chapter":
                if line == "":
                    continue
                if is_chapter_title(line):
                    if self.chapter_title:
                        self.chapters.append(
                            BPChapter(self.chapter_title, self.chapter_content)
                        )
                    self.chapter_title = line
                    self.chapter_content = ""
                else:
                    self.chapter_content += line

        # Add the last chapter
        if self.chapter_title:
            self.chapters.append(BPChapter(self.chapter_title, self.chapter_content))
        self.state = "end"
        self.book = BPBook(self.title, self.author, self.preface, self.chapters)
