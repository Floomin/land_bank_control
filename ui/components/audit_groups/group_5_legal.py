import streamlit as st


def render_group_5():
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
