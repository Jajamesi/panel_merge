import streamlit as st
import funcs

st.header('Подлитие базы с панели к базе с платформы')




platform_base = st.file_uploader(
    label="Загрузите базу данных с **:red[ПЛАТФОРМЫ]**",
    type=["sav", "zsav"],
    accept_multiple_files=False,
    key="platform_base",
)

panel_base = st.file_uploader(
    label="Загрузите базу данных с **:blue[ПАНЕЛИ]**",
    type=["sav", "zsav"],
    accept_multiple_files=False,
    key="panel_base",
)

if st.button("Запустить"):
    funcs.process(platform_base, panel_base)

    data_path = st.session_state.get("download_base")

    data = open(data_path, "rb")

    dwnld_button_cols = st.columns([0.3, 0.4, 0.3])
    with dwnld_button_cols[1]:
        st.download_button(label='📥 Скачать базу',
                           data=data,
                           file_name="Объединенная база.zsav")

    st.stop()