import streamlit as st
from core.utils.data_cleaners import load_options


def render_group_1(prefix=""):
    # ГРУПА 1: Наявність документів
    with st.expander("Група 1: Наявність документів", expanded=True):
        st.checkbox("Оригінал договору", value=True, key=f"{prefix}has_original")

        # Отримуємо кількість сторін з Групи 0 (за замовчуванням 1)
        is_multi = st.session_state.get(f"{prefix}is_multilateral", "Ні")
        count = (
            st.session_state.get(f"{prefix}party_count", 1) if is_multi == "Так" else 1
        )

        if count == 1:
            # СТАНДАРТНИЙ ВИГЛЯД (1 СТОРОНА)
            c1, c2 = st.columns(2)
            with c1:
                st.checkbox(
                    "Копія паспорта (Згідно останього діючого документу)", value=True, key=f"{prefix}has_passport_copy"
                )
            with c2:
                st.checkbox(
                    "Копія ІПН (Згідно останього діючого документу)", value=True, help="text", key=f"{prefix}has_ipn_copy"
                )

            st.multiselect(
                "Копія правоустановчих документів (Згідно останього діючого документу)",
                options=load_options("legal_docs.txt"),
                help="Можна обрати декілька варіантів",
                key=f"{prefix}legal_docs_copies",
            )
        else:
            # БАГАТОСТОРОННІЙ ВИГЛЯД
            st.write("**Документи сторін:**")
            for i in range(1, count + 1):
                with st.container(border=True):
                    st.markdown(f"**Сторона {i}**")
                    c1, c2 = st.columns(2)
                    with c1:
                        st.checkbox(
                            "Копія паспорта (Згідно останього діючого документу)",
                            value=True,
                            key=f"{prefix}has_passport_copy_{i}",
                        )
                    with c2:
                        st.checkbox(
                            "Копія ІПН(Згідно останього діючого документу)",
                            value=True,
                            help="text",
                            key=f"{prefix}has_ipn_copy_{i}",
                        )

                    st.multiselect(
                        "Копія правоустановчих документів (Згідно останього діючого документу)",
                        options=load_options("legal_docs.txt"),
                        key=f"{prefix}legal_docs_copies_{i}",
                    )
