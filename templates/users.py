import yaml
import streamlit as st
from env_settings import BASE_DIR
from streamlit_authenticator import Hasher


def show_user_manage_block_method():
    st.header('使用者管理')

    add_user_tab, delete_user_tab = st.tabs(["新增", "刪除"])

    with add_user_tab:
        with st.form(key='add_user_form', clear_on_submit=True):
            username = st.text_input("請輸入 username：")
            email = st.text_input("請輸入 email：")
            password = st.text_input("請輸入 password：", type='password')
            password_confirm = st.text_input("請再次輸入 password：", type='password')

            if st.form_submit_button('新增'):
                if password == password_confirm:
                    with open(BASE_DIR / 'volumes' / 'credentials.yaml', 'r') as file:
                        data = yaml.safe_load(file)

                    if data['credentials']['usernames'].get(username):
                        st.error("username 已存在")
                    else:
                        data['credentials']['usernames'][username] = {
                            "email": email,
                            "name": username,
                            "password": Hasher([password]).generate()[0]
                        }
                        with open(BASE_DIR / 'volumes' / 'credentials.yaml', 'w') as file:
                            yaml.safe_dump(data, file)
                        st.success("新增成功")
                else:
                    st.error("兩次 password 不一致")

    with delete_user_tab:
        with st.form(key='delete_user_form', clear_on_submit=True):
            username = st.text_input("請輸入 username：")
            email = st.text_input("請輸入 email：")

            if st.form_submit_button('刪除'):
                if username and email:
                    st.error("請選擇一種刪除方式")
                elif username:
                    with open(BASE_DIR / 'volumes' / 'credentials.yaml', 'r') as file:
                        data = yaml.safe_load(file)

                    if data['credentials']['usernames'].get(username):
                        if data['credentials']['usernames'][username]['name'] == 'root':
                            st.error("root 無法刪除")
                        else:
                            del data['credentials']['usernames'][username]
                            with open(BASE_DIR / 'volumes' / 'credentials.yaml', 'w') as file:
                                yaml.safe_dump(data, file)
                            st.success("刪除成功")
                    else:
                        st.error(f"{username} 不存在")
                elif email:
                    with open(BASE_DIR / 'volumes' / 'credentials.yaml', 'r') as file:
                        data = yaml.safe_load(file)

                    for username, info in data['credentials']['usernames'].items():
                        if info['email'] == email:
                            if data['credentials']['usernames'][username]['name'] == 'root':
                                st.error("root 無法刪除")
                                break
                            else:
                                del data['credentials']['usernames'][username]
                                with open(BASE_DIR / 'volumes' / 'credentials.yaml', 'w') as file:
                                    yaml.safe_dump(data, file)
                                st.success("刪除成功")
                                break
                    else:
                        st.error(f"{email} 不存在")
