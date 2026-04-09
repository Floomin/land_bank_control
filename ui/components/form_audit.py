import streamlit as st
from core.utils.data_cleaners import load_options


def render_audit_form():
    """Відображає форму аудиту, розділену на групи."""

    st.subheader("Форма аудиту")

    # ГРУПА 0: Загальна інформація
    with st.expander("Група 0: Загальна інформація", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("Тип договору", options=load_options("contract_types.txt"))
            st.selectbox("Організація", options=load_options("org_list.txt"))
            st.selectbox("Населений пункт", options=load_options("vilage.txt"))

        with col2:
            st.selectbox(
                "Тип Контрагенту", options=load_options("counterparty_types.txt")
            )
            st.selectbox("Багатосторонній", options=["Так", "Ні"])
            st.text_input("№ папки в Архіві")

    # ГРУПА 1: Наявність документів
    with st.expander("Група 1: Наявність документів", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.checkbox("Оригінал договору", value=True)
        with c2:
            st.checkbox("Копія паспорта", value=True)
        with c3:
            st.checkbox("Копія ІПН", value=True, help="text")

        st.multiselect(
            "Копія правоустановчих документів",
            options=load_options("legal_docs.txt"),
            help="Можна обрати декілька варіантів",
        )

        st.multiselect(
            "Наявність обов'язкових додатків",
            options=load_options("annexes.txt"),
            placeholder="Оберіть за наявності",
        )

    # ГРУПА 2: Реквізити договору
    with st.expander("Група 2: Реквізити договору", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Номер договору")
            st.text_input("Номер реєстрації оренди")
            st.text_input("ПІБ Орендодавця")
            st.text_input("Частка права володіння (напр. 1/3)")
            st.date_input("Дата закінчення (#ff0000 зігдно ДОГОВОРУ!!!)", value=None)
        with col2:
            st.date_input("Дата підписання", value=None)
            st.date_input("Дата реєстрації договору", value=None)
            st.text_input("ІПН (пайовика)")
            # st.text_input("Паспортні дані")
            st.text_input("Частка паю (картка земельної ділянки)")
            st.text_input("Частка орендної плати")
            st.date_input("Дата закінчення (Аудит)", value=None)

        st.write("**Строк дії**")
        sc1, sc2, sc3 = st.columns(3)
        sc1.number_input("Роки", min_value=0, step=1)
        sc2.number_input("Місяці", min_value=0, max_value=11)
        sc3.number_input("Дні", min_value=0, max_value=30)

    # ГРУПА 3: Відомості про земельну ділянку
    with st.expander("Група 3: Відомості про земельну ділянку", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.number_input(
                "Площа по паперовому примірнику", format="%.4f", min_value=0.0
            )
            st.text_input("Місце розташування")
            st.selectbox(
                "Цільове призначення", options=load_options("land_purposes.txt")
            )
            st.selectbox("Вид угідь", options=load_options("land_types.txt"))
        with col2:
            st.number_input(
                "Площа згідно правоустановчих документів", format="%.4f", min_value=0.0
            )
            st.text_input("Місце розташування (ПД)")
            st.selectbox(
                "Цільове призначення (ПД)",
                options=load_options("land_purposes.txt"),
                key="purpose_pd",
            )
            st.selectbox(
                "Вид угідь (ПД)", options=load_options("land_types.txt"), key="type_pd"
            )

    # ГРУПА 5: Юридичний блок
    with st.expander("Група 5: Юридичний блок", expanded=True):
        # st.text_input("Тип обмеження")
        # c1, c2, c3 = st.columns(3)
        # with c1:
        #    st.checkbox("Передача в Суборенду", value=True)
        # with c2:
        #    st.checkbox("Реорганізація не припиняє договір", value=True)
        # with c3:
        #    st.checkbox("Розірвання в односторонньому порядку")

        st.write("**Наявність підписів**")
        c4, c5 = st.columns(2)
        with c4:
            st.checkbox("Наявність підпису Орендаря", value=True)
            st.checkbox("Наявність печаток", value=True)
        with c5:
            st.checkbox("Наявність підпису Орендодавця", value=True)

    st.text_area(
        "Примітка Аудитора",
        placeholder="Заповніть усні не зазначені у формі помилки в договорі. \nКожну помилку починайте з цифри по порядку.\nНаприклад:\n1. У паперовому примірнику помилка у ПІБ орендодавця ",
        height=200,
    )
    # ГРУПА 6: Додаткові угоди
    with st.expander("Група 6: Додаткові угоди"):
        st.info("Цей блок наразі порожній")

    # КНОПКИ
    st.divider()
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])

    with col_btn1:
        if st.button("Зберегти", width="stretch", type="primary"):
            st.session_state.show_confirm = True

    with col_btn2:
        st.button("Розблокувати", width="stretch", help="Тільки для адміністратора")

    # Модальне вікно підтвердження (через session_state)
    if st.session_state.get("show_confirm"):
        st.warning("Ви впевнені, що хочете зберегти дані?")
        cb1, cb2 = st.columns(2)
        if cb1.button("Так, зберегти", width="stretch"):
            st.success("Дані збережено!")
            st.session_state.show_confirm = False
        if cb2.button("Скасувати", width="stretch"):
            st.session_state.show_confirm = False
