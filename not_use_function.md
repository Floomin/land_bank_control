
   st.selectbox("Форма договору", options=load_options("form_types.txt"))
   
   # st.selectbox(
            #     "Тип набуття чинності", options=load_options("entry_force.txt")
            # )
   
   
   
    # ГРУПА 4: Орендна плата
    with st.expander("Група 4: Орендна плата", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("Форма оплати", options=["Грошова", "Натуральна", "Змішана"])
            st.number_input("Розмір (грн)", step=0.01, min_value=0.0)
            st.number_input("% від НГО", step=0.01, min_value=0.0)
        with col2:
            st.number_input("Кількість зерна (тонн)", step=0.001, min_value=0.0)
            st.checkbox("Індексація НГО", value=True)
            st.checkbox("Застосування індексів інфляції", value=False)
        st.text_input("Наявність додаткових виплат")



        # st.write("**Відповідність підписів**")
        # c6, c7 = st.columns(2)
        # with c6:
        #   st.checkbox("Відповідність підпису Орендаря", value=True)
        # with c7:
        #   st.checkbox("Відповідність підпису Орендодавця", value=True)


                st.multiselect(
            "Наявність обов'язкових додатків",
            options=load_options("annexes.txt"),
            placeholder="Оберіть за наявності",
        )