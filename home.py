import os.path
import streamlit as st
from env_settings import BASE_DIR
from utils import get_authenticator, session_scope, get_content_md5
from databases import cruds
from datetime import datetime

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

    with st.sidebar:
        st.title('📖 檔案好朋友 📖')
        st.write(f'*{name}* 您好')
        if label_name := st.text_input(label='輸入標籤查詢：'):
            print(label_name)
        if file_name := st.text_input(label='輸入檔案名稱查詢：'):
            print(file_name)

        superuser_list = ['root', 'nick', 'sam']
        if username in superuser_list:
            st.divider()
            st.write(f"下方為管理者專區：")
            show_upload_block = st.checkbox('顯示上傳檔案區塊')
            show_delete_block = st.checkbox('顯示刪除檔案區塊')

        authenticator.logout('Logout', 'main')

    if show_upload_block:
        st.header('檔案上傳')
        tag_string = st.text_input("請輸入標籤：", placeholder='多個標籤請用半形逗號隔開')

        uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
        if not os.path.exists(BASE_DIR / 'files'):
            os.mkdir(BASE_DIR / 'files')

        now = datetime.now()
        for uploaded_file in uploaded_files:
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

    if show_delete_block:
        st.header('檔案刪除')
        tag_delete = st.text_input("請輸入標籤：")
        file_name_delete = st.text_input("請輸入檔案名稱：")

        st.divider()

    st.header('熱門搜尋')
    for i in range(10):
        with st.expander("See explanation"):
            st.write(
                """
            The chart above shows some numbers I picked for you.
                I rolled actual dice for these, so they're *guaranteed* to
                be random."""
            )
            binary_contents = b'example content'
            st.download_button('Download File', binary_contents, key=i)

elif authentication_status is False:
    st.error('Username/password is incorrect')
elif authentication_status is None:
    st.warning('Please enter your username and password')
