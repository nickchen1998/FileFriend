from sqlalchemy.orm import Session
from databases.schemas import File, Tag
from typing import List
from utils import get_content_md5


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


def create_file(session: Session, name: str, hashcode: str, size: float, tags: List[Tag]) -> File:
    if file := session.query(File).filter(File.name == name).first():
        return file
    else:
        file = File(name=name, size=size, hashcode=hashcode, tags=tags)
        session.add(file)
        session.commit()
        session.refresh(file)

        return file


def get_files(session: Session):
    return session.query(File).all()