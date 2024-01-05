import os
import mimetypes
import streamlit as st
from utils import get_authenticator, session_scope
from databases import cruds
from env_settings import BASE_DIR
from templates.files import show_upload_block_method, show_delete_block_method
from templates.users import show_user_manage_block_method

st.set_page_config(
    page_title='檔案好朋友',
    page_icon='📖'
)
authenticator = get_authenticator()
name, authentication_status, username = authenticator.login(
    'Login', 'main')

if authentication_status:
    show_upload_block = False
    show_delete_block = False
    show_user_block = False

    with st.sidebar:
        st.title('📖 檔案好朋友 📖')
        st.write(f'*{name}* 您好！')
        st.write('請選擇您要進行的操作：')

        with session_scope() as session:
            file_list = cruds.get_files(session=session)

        with st.form(key='search_form', clear_on_submit=True):
            tag_name = st.text_input(label='輸入標籤查詢：')
            file_name = st.text_input(label='輸入檔案名稱查詢：')

            col1, col2 = st.columns(2, gap="large")
            if col1.form_submit_button('查詢'):
                if tag_name and file_name:
                    st.error('請選擇一種查詢方式')
                elif tag_name:
                    with session_scope() as session:
                        file_list = cruds.get_files_by_tag(
                            session=session, tag=tag_name)
                elif file_name:
                    with session_scope() as session:
                        file_list = [cruds.get_file_by_filename(
                            session=session, filename=file_name)]
            if col2.form_submit_button('重置'):
                with session_scope() as session:
                    file_list = cruds.get_files(session=session)

        if username == 'root':
            st.divider()
            st.write(f"下方為管理者專區：")
            show_upload_block = st.checkbox('顯示上傳檔案區塊')
            show_delete_block = st.checkbox('顯示刪除檔案區塊')
            show_user_block = st.checkbox('顯示使用者管理區塊')

        authenticator.logout('Logout', 'main')

    if show_upload_block:
        show_upload_block_method()
    if show_delete_block:
        show_delete_block_method()
    if show_user_block:
        show_user_manage_block_method()

    st.header('檔案列表')

    for index, file in enumerate(file_list):
        if os.path.exists(BASE_DIR / 'files' / file.get('name')):
            with st.expander(f"{file.get('name')}"):
                st.write(f"檔案標籤：{', '.join(list(file.get('tags')))}")
                st.write(f'檔案描述：{file.get("description")}')
                st.write(f'上傳時間：{file.get("created_at")}')

                # 檔案下載按鈕
                with open(BASE_DIR / 'files' / file.get('name'), 'rb') as _file:
                    binary_contents = _file.read()
                st.download_button(
                    'Download File',
                    binary_contents,
                    file_name=file.get('name'),
                    mime=mimetypes.guess_type(file.get('name'))[0],
                    key=index
                )

elif authentication_status is False:
    st.error('Username/password is incorrect')
elif authentication_status is None:
    st.warning('Please enter your username and password')
