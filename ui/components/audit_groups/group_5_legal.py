import streamlit as st


def render_group_5(prefix=""):
    # ГРУПА 5: Юридичний блок
    with st.expander("Група 5: Юридичний блок", expanded=True):
        st.write("**Наявність підписів**")

        is_multi = st.session_state.get(f"{prefix}is_multilateral", "Ні")
        count = (
            st.session_state.get(f"{prefix}party_count", 1) if is_multi == "Так" else 1
        )

        if count == 1:
            # СТАНДАРТНИЙ ВИГЛЯД (1 СТОРОНА)
            c4, c5 = st.columns(2)
            with c4:
                st.checkbox(
                    "Наявність підпису Орендаря",
                    value=True,
                    key=f"{prefix}has_lessee_sign",
                )
                st.checkbox("Наявність печаток", value=True, key=f"{prefix}has_seals")
            with c5:
                st.checkbox(
                    "Наявність підпису Орендодавця",
                    value=True,
                    key=f"{prefix}has_lessor_sign",
                )
        else:
            # БАГАТОСТОРОННІЙ ВИГЛЯД
            c4, c5 = st.columns(2)
            with c4:
                st.checkbox(
                    "Наявність підпису Орендаря",
                    value=True,
                    key=f"{prefix}has_lessee_sign",
                )
                st.checkbox("Наявність печаток", value=True, key=f"{prefix}has_seals")
            with c5:
                st.write("**Підписи Орендодавців:**")
                for i in range(1, count + 1):
                    st.checkbox(
                        f"Підпис Орендодавця (Сторона {i})",
                        value=True,
                        key=f"{prefix}has_lessor_sign_{i}",
                    )
