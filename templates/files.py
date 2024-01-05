import os.path
import streamlit as st
from env_settings import BASE_DIR
from utils import session_scope, get_content_md5
from databases import cruds
from datetime import datetime


def show_upload_block_method():
    st.header('檔案上傳')
    with st.form(key='upload_file_form', clear_on_submit=True):
        now = datetime.now()
        tag_string = st.text_input("請輸入標籤：", placeholder='多個標籤請用半形逗號隔開')
        description = st.text_area(label="請輸入檔案描述：")
        upload_file = st.file_uploader("請選擇要上傳的檔案", accept_multiple_files=False)

        if st.form_submit_button('上傳'):
            if upload_file and description and tag_string:
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
                            st.success("上傳成功")


def show_delete_block_method():
    st.header('檔案刪除')
    with st.form(key='delete_file_form', clear_on_submit=True):
        tag = st.text_input("請輸入標籤：")
        file_name = st.text_input("請輸入檔案名稱：")

        if st.form_submit_button('刪除'):
            if tag and file_name:
                st.error("標籤及檔案名稱請擇一輸入")

            elif tag:
                with session_scope() as session:
                    result = cruds.delete_files_by_tag(session=session, tag=tag)
                    if result is False:
                        st.error("標籤不存在")
                    else:
                        st.success("刪除成功")

            elif file_name:
                with session_scope() as session:
                    result = cruds.delete_file_by_filename(session=session, filename=file_name)
                    if result is False:
                        st.error("檔案不存在")
                    else:
                        st.success("刪除成功")
