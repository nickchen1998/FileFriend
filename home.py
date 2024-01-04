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
        st.write(f'*{name}* 您好')
        if label_name := st.text_input(label='輸入標籤查詢：'):
            print(label_name)
        if file_name := st.text_input(label='輸入檔案名稱查詢：'):
            print(file_name)

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
    with session_scope() as session:
        for index, file in enumerate(cruds.get_files(session=session)):
            if os.path.exists(BASE_DIR / 'files' / file.name):
                with st.expander(f"{file.name}"):
                    st.write(f"檔案標籤：{', '.join(list(map(lambda x: x.name, file.tags)))}")
                    st.write(f'檔案描述：{file.description}')
                    st.write(f'上傳時間：{file.created_at}')

                    # 檔案下載按鈕
                    with open(BASE_DIR / 'files' / file.name, 'rb') as _file:
                        binary_contents = _file.read()
                    st.download_button(
                        'Download File',
                        binary_contents,
                        file_name=file.name,
                        mime=mimetypes.guess_type(file.name)[0],
                        key=index
                    )

elif authentication_status is False:
    st.error('Username/password is incorrect')
elif authentication_status is None:
    st.warning('Please enter your username and password')
