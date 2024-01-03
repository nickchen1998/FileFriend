import os
from env_settings import BASE_DIR
from sqlalchemy.orm import Session
from databases.schemas import File, Tag
from typing import List


def create_tags(session: Session, tags: List[str]) -> List[Tag]:
    tag_list = []
    for tag_name in tags:
        if tmp := session.query(Tag).filter(Tag.name == tag_name).first():
            tag_list.append(tmp)
        else:
            tag = Tag(name=tag_name)
            session.add(tag)
            session.commit()
            session.refresh(tag)
            tag_list.append(tag)

    return tag_list


def create_file(session: Session, name: str, description: str, hashcode: str, size: float, tags: List[Tag]) -> File:
    if file := session.query(File).filter(File.name == name).first():
        return file
    else:
        file = File(name=name, size=size, hashcode=hashcode, tags=tags, description=description)
        session.add(file)
        session.commit()
        session.refresh(file)

        return file


def get_files(session: Session):
    return session.query(File).all()


def delete_files_by_tag(session: Session, tag: str):
    if tag := session.query(Tag).filter(Tag.name == tag).first():
        for file in tag.files:
            if os.path.exists(BASE_DIR / 'files' / file.name):
                os.remove(BASE_DIR / 'files' / file.name)

            session.delete(file)
        session.delete(tag)
        session.commit()

        return True
    else:
        return False


def delete_file_by_filename(session: Session, filename: str):
    if file := session.query(File).filter(File.name == filename).first():
        if os.path.exists(BASE_DIR / 'files' / file.name):
            os.remove(BASE_DIR / 'files' / file.name)

        session.delete(file)
        session.commit()

        return True
    else:
        return False
