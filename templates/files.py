import os.path
import streamlit as st
from env_settings import BASE_DIR
from utils import session_scope, get_content_md5
from databases import cruds
from datetime import datetime


def show_upload_block_method():
    st.header('檔案上傳')
    tag_string = st.text_input("請輸入標籤：", placeholder='多個標籤請用半形逗號隔開')

    now = datetime.now()
    for uploaded_file in st.file_uploader("Choose a CSV file", accept_multiple_files=True):
        if not os.path.exists(BASE_DIR / 'files' / uploaded_file.name):
            with session_scope() as session:
                tags = tag_string.split(',') if tag_string else [f'{now.year}-{now.month}-{now.day}']
                tag_obj_list = cruds.create_tags(session=session, tags=tags)

                bytes_data = uploaded_file.read()
                file_obj = cruds.create_file(
                    session=session,
                    name=uploaded_file.name,
                    hashcode=get_content_md5(bytes_data),
                    size=uploaded_file.size,
                    tags=tag_obj_list
                )

                if file_obj:
                    with open(BASE_DIR / 'files' / f'{uploaded_file.name}', 'wb') as file:
                        file.write(bytes_data)

    st.divider()


def show_delete_block_method():
    st.header('檔案刪除')
    tag_delete = st.text_input("請輸入標籤：")
    file_name_delete = st.text_input("請輸入檔案名稱：")

    st.divider()