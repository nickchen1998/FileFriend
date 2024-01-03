import os.path
import streamlit as st
from env_settings import BASE_DIR
from utils import session_scope, get_content_md5
from databases import cruds
from datetime import datetime


def show_upload_block_method():
    now = datetime.now()

    st.header('檔案上傳')
    tag_string = st.text_input("請輸入標籤：", placeholder='多個標籤請用半形逗號隔開')
    description = st.text_input("請輸入檔案描述：")
    upload_file = st.file_uploader("請選擇要上傳的檔案", accept_multiple_files=False)

    if st.button('上傳') and upload_file and description:
        if not os.path.exists(BASE_DIR / 'files' / upload_file.name):
            with session_scope() as session:
                tags = tag_string.split(',') if tag_string else [f'{now.year}-{now.month}-{now.day}']
                tag_obj_list = cruds.create_tags(session=session, tags=tags)

                bytes_data = upload_file.read()
                file_obj = cruds.create_file(
                    session=session,
                    name=upload_file.name,
                    description=description,
                    hashcode=get_content_md5(bytes_data),
                    size=upload_file.size,
                    tags=tag_obj_list
                )

                if file_obj:
                    with open(BASE_DIR / 'files' / f'{upload_file.name}', 'wb') as file:
                        file.write(bytes_data)
    st.divider()


def show_delete_block_method():
    st.header('檔案刪除')
    tag_delete = st.text_input("請輸入標籤：")
    file_name_delete = st.text_input("請輸入檔案名稱：")

    st.divider()
