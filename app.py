# python3 -m venv venv
# source venv/bin/activate
# pip install -r requirements.txt

import streamlit as st
import random
import time
from streamlit_echarts import st_echarts, st_pyecharts
from pyecharts import options as opts
from pyecharts.charts import Bar
import numpy as np
import pandas as pd

st.set_page_config(
    page_icon="🧊",
    # layout="wide",

)

tab1, tab2, tab3 = st.tabs(["Задачи 1", "Задачи 2", "Задачи 3"])

with tab1:

    col1, col2, col3 = st.columns([4,0.9,2.1])
    # Create random dataframe with 5 rows and two columns with random numbers from 0 to 10
    @st.cache_data
    def load_numbers():
        data = pd.DataFrame({
            'А': np.random.randint(0, 11, 10),
            '+': "+",
            'Б': np.random.randint(0, 11, 10),
            '=': '=',
            'Сума': [None]*10,  # Empty column to manually input sum
            #'Check Sum': [False]*5  # Empty column to check sum (True/False)
            
        })
        
        return data
    
    data = load_numbers()
    
    

    for i in range(len(data)):
        
        correct_sum = data['А'][i] + data['Б'][i]
        # Update 'Check Sum' column with True or False based on user input in 'Sum'
        #data.at[i, 'Check Sum'] = (data['Sum'][i] == correct_sum)



    with col1:
        # Use st.data_editor to display the dataframe and allow manual editing for 'Sum' column
        edited_data = st.data_editor(
            data,
            column_config={
                'Сума': st.column_config.NumberColumn("Пресметни"),
                #'Check Sum': st.column_config.CheckboxColumn("Check Sum")
            },
            #disabled=["Check Sum"],  # Disable editing on Check Sum column
            #use_container_width=True,
            hide_index=True
        )
        
        # Automatically update the 'Check Sum' column based on user input
        for i in range(len(edited_data)):
            correct_sum = edited_data['А'][i] + edited_data['Б'][i]
            # Update 'Check Sum' column with True or False based on user input in 'Sum'
            edited_data.at[i, 'Проверка'] = (edited_data['Сума'][i] == correct_sum)
        
    # Display the updated dataframe with True/False in 'Check Sum' column
    with col2:
        filtered_data = edited_data['Проверка']
        st.dataframe(filtered_data, hide_index=True)

    with col3:
        image_tedy = st.image("tedy_5_hd.png", width=500)


    if "reload" not in st.session_state:
        st.session_state["reload"] = False

    reload = st.button("Reload")
    if reload:
        st.session_state.reload = True

    if st.session_state.reload:

        progress_text = "✅ ⚠️ ✅ ⚠️ ✅ ⚠️ ✅ ⚠️"
        my_bar = st.progress(0, text=progress_text)

        for percent_complete in range(100):
            time.sleep(0.005)
            my_bar.progress(percent_complete + 1, text=progress_text)
        time.sleep(0.5)
        my_bar.empty()

        load_numbers.clear()
        st.session_state["reload"] = False

with tab2:

    image_tedy = st.image("little_tedy.jpg", width=300)

    st.write(f"Здравей, :blue[Теди]! Можеш ли да решиш тези задачи?")

    # Initialize session state for showing/hiding answers
    if "show_answers" not in st.session_state:
        st.session_state.show_answers = False

    # Columns for buttons
    column1, column2, column3, column4 = st.columns([0.5, 0.5, 0.5, 1], gap="small", vertical_alignment="bottom")

    with column1:
        button_show = st.button("Покажи отговорите")
        if button_show:
            st.session_state.show_answers = True
    with column2:
        button_hide = st.button("Скрий отговорите")
        if button_hide:
            st.session_state.show_answers = False

    # Initialize problem set
    if 'problems' not in st.session_state:
        st.session_state.problems = []

    if 'problems2' not in st.session_state:
        st.session_state.problems2 = []

    # Function to generate new math problems
    def new_numbers():
        st.session_state.problems = []
        for _ in range(5):
            num1 = random.randint(0, 10)
            num2 = random.randint(0, 10)
            operator = "+"
            answer = num1 + num2
            st.session_state.problems.append((num1, operator, num2, answer))


    # Function to generate new math problems
    def new_numbers_2():
        st.session_state.problems2 = []
        for _ in range(1):
            num01 = random.randint(10, 20)
            num02 = random.randint(10, 20)
            operator2 = "+"
            answer2 = num01 + num02
            st.session_state.problems2.append((num01, operator2, num02, answer2))


    if st.session_state.problems == []:
        new_numbers()

    if st.session_state.problems2 == []:
        new_numbers_2()

    # Button for refreshing problems
    with column3:
        button_reload = st.button("Обнови")

    # with column4:
    #     st.image("Tedy_5.png", width=300)

    if button_reload:
        progress_text = "✅ ⚠️ ✅ ⚠️ ✅ ⚠️ ✅ ⚠️ ✅"
        my_bar = st.progress(0, text=progress_text)

        for percent_complete in range(100):
            time.sleep(0.005)
            my_bar.progress(percent_complete + 1, text=progress_text)
        time.sleep(0.5)
        my_bar.empty()
        st.session_state.user_answers = [None] * 5
        st.session_state.user_answers2 = [None] * 5

        new_numbers()
        new_numbers_2()
        st.snow()

    if 'problems' not in st.session_state:
        new_numbers()

    if 'problems2' not in st.session_state:
        new_numbers_2()

    # Initialize user answers
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = [None] * 5

    if 'user_answers2' not in st.session_state:
        st.session_state.user_answers2 = [None] * 5

    # Score calculation
    score_true = 0
    score_false = 0
    score = 0
    for i, (num1, operator, num2, answer) in enumerate(st.session_state.problems):
        col1, col2, col3, col4, col5, col6 = st.columns([0.5, 0.3, 0.5,0.5, 1,2], gap="small", vertical_alignment="top")
        
        # Display num1 as GIF
        with col1:
            st.write("")
            st.image(f"gifs/{num1}.gif")
        
        # Display operator
        with col2:
            st.write("")
            st.write("")
            st.image(f"gifs/plus.png")
        
        # Display num2 as GIF
        with col3:
            st.write("")
            st.image(f"gifs/{num2}.gif")
        
        # User input for the answer
        with col4:
            user_input = st.number_input(label="", format="%0.0f", value=st.session_state.user_answers[int(i)] or None, key=f"input_{i}")
            
            st.session_state.user_answers[i] = user_input

            with col5:
                # Check if the answer is correct
                if user_input == answer:
                    st.write("")
                    st.success(f":green[Вярно!]", icon="✅")
                    score += 1
                    score_true += 1
                else:
                    if st.session_state.user_answers[i] != None:
                        st.write("")
                        st.error(f":red[Грешно!]", icon="⚠️")
                    if st.session_state.show_answers:
                        st.write("")
                        st.success(f':green[{answer}]')
                    if user_input != None:
                        score_false += 1

    st.write("---")
    # Score calculation2
    for i, (num01, operator2, num02, answer2) in enumerate(st.session_state.problems2):
        col1, col2, col3, col4, col5, col6 = st.columns([0.5, 0.3, 0.5,0.5, 1,2], gap="small", vertical_alignment="top")
        
        # Display num1 as GIF
        with col1:
            st.write("")
            st.image(f"gifs/{num01}.gif")
        
        # Display operator
        with col2:
            st.write("")
            st.write("")
            st.image(f"gifs/plus.png")
        
        # Display num2 as GIF
        with col3:
            st.write("")
            st.image(f"gifs/{num02}.gif")
        
        # User input for the answer
        with col4:
            user_input = st.number_input(label="", format="%0.0f", value=st.session_state.user_answers2[int(i)] or None, key=f"input2_{i}")
            
            st.session_state.user_answers2[i] = user_input

            with col5:
                # Check if the answer is correct
                if user_input == answer2:
                    st.write("")
                    st.success(f":green[Вярно!]", icon="✅")
                    score += 1
                    score_true += 1
                else:
                    if st.session_state.user_answers2[i] != None:
                        st.write("")
                        st.error(f":red[Грешно!]", icon="⚠️")
                    if st.session_state.show_answers:
                        st.write("")
                        st.success(f':green[{answer2}]')
                    if user_input != None:
                        score_false += 1

    # Show score
    # st.write(f"Резултат: {score}/5")
    # st.write(f"Правилни отговори: {score_true}")
    # st.write(f"Грешни отговори: {score_false}")

    st.session_state.show_answers = False



    if score_true == 6:
        st.balloons()
        time.sleep(0.8)
        st.balloons()
        time.sleep(0.8)
        st.balloons()
        time.sleep(0.8)
        st.balloons()


    # with col6:
    if score_true != 0 and score_false != 0:
        c1,c2 = st.columns([5,4], gap="small", vertical_alignment="top")
        with c1:
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            pie = st_echarts(options={
            # "title": {
            #     "text": f"Верни {round(score_true,0):,.0f} vs Грешни {round(score_false,0):,.0f}".replace(',', ' '),
            #     "left": "center"
            # },
            "tooltip": {
                "trigger": "item" 
            },
            "legend": {
                "orient": "horizontal",
                "left": "left"
            },
            "series": [
                {
                #"name": "Брой",
                "type": "pie",
                "radius": "60%",
                "data": [
                    {"value": round(score_true,0), "name": "Верни", "itemStyle": {"color": "#7efc89"}},
                    {"value": round(score_false,0), "name": "Грешни", "itemStyle": {"color": "#de5770"}}  
                ],
                "emphasis": {
                    "itemStyle": {
                    "shadowBlur": 10,
                    "shadowOffsetX": 10,
                    "shadowColor": "rgba(0, 0, 0, 0.5)"
                    }
                }
                }
            ]
            })

with tab3:



    # # Function to mix two hex colors
    # def mix_colors(color1, color2):
    #     mixed_color = "#"
    #     for i in range(1, 7, 2):
    #         component1 = int(color1[i:i+2], 16)
    #         component2 = int(color2[i:i+2], 16)
    #         mixed_component = (component1 + component2) // 2
    #         mixed_color += f"{mixed_component:02x}"
    #     return mixed_color

    # def generate_css_for_options(colors: list) -> str:
    #     css = "<style>"
    #     for i, color in enumerate(colors):
    #         css += (
    #             f"""ul[data-testid="stSelectboxVirtualDropdown"] li[role="option"]:nth-child({i + 1})"""
    #             + "{"
    #             + f"background-color: {color['code']}; color: {color['text_color']};"
    #             + "}"
    #         )
    #     css += "</style>"
    #     return css



    # def generate_css_for_box(color_name: str) -> str:
    #     css = "<style>"
    #     for color in colors:
    #         if color["name"] == color_name:
    #             css += (
    #                 """div[data-baseweb="select"] > div:first-child {"""
    #                 + f"background-color: {color['code']}; color: {color['text_color']};"
    #                 + "}"
    #             )
    #             break
    #     css += "</style>"
    #     return css

    # colors1 = [
    #     {"code": "#101B58", "name": "Penn Blue", "text_color": "#FFFFFF"},
    #     {"code": "#45296C", "name": "Tekhelet", "text_color": "#FFFFFF"},
    #     {"code": "#793780", "name": "Eminence", "text_color": "#FFFFFF"},
    #     {"code": "#AD4594", "name": "Fandango", "text_color": "#FFFFFF"},
    #     {"code": "#E153A8", "name": "Brilliant Rose", "text_color": "#FFFFFF"},
    #     {"code": "#F0A998", "name": "Melon", "text_color": "#FFFFFF"},
    #     {"code": "#F8D490", "name": "Sunset", "text_color": "#000000"},
    #     {"code": "#FFFF88", "name": "Icterine", "text_color": "#000000"},
    # ]


    # color2 = [
    #     {"code": "#FF0000", "name": "Red", "text_color": "#FFFFFF"},
    #     {"code": "#00FF00", "name": "Green", "text_color": "#000000"},
    #     {"code": "#0000FF", "name": "Blue", "text_color": "#FFFFFF"},
    #     {"code": "#FFFF00", "name": "Yellow", "text_color": "#000000"},
    #     {"code": "#FFA500", "name": "Orange", "text_color": "#000000"},
    #     {"code": "#800080", "name": "Purple", "text_color": "#FFFFFF"},
    #     {"code": "#FFC0CB", "name": "Pink", "text_color": "#000000"},
    #     {"code": "#808080", "name": "Gray", "text_color": "#FFFFFF"},
    #     {"code": "#FFFFFF", "name": "White", "text_color": "#000000"},
    #     {"code": "#000000", "name": "Black", "text_color": "#FFFFFF"},
    #     {"code": "#A52A2A", "name": "Brown", "text_color": "#FFFFFF"},
    #     {"code": "#00FFFF", "name": "Cyan", "text_color": "#000000"},
    #     {"code": "#008000", "name": "Dark Green", "text_color": "#FFFFFF"},
    # ]

    # colors = st.segmented_control("Цветове", ["Основни", "Други"])
    # if colors == "Основни":
    #     colors = color2
    # else:
    #     colors = colors1

    # col1, col2 = st.columns([1, 1])

    # with col1:
    #     st.markdown(generate_css_for_options(colors), unsafe_allow_html=True)
    #     options = [color["name"] for color in colors]
    #     selected_color = st.selectbox(label="Избери цвят 1", options=options, key="color_selected")
    #     st.markdown(generate_css_for_box(selected_color), unsafe_allow_html=True)

    # with col2:
    #     st.markdown(generate_css_for_options(colors), unsafe_allow_html=True)
    #     options2 = [color["name"] for color in colors]
    #     selected_color2 = st.selectbox(label="Избери цвят 2", options=options2, key="color_selected2")
    #     st.markdown(generate_css_for_box(selected_color2), unsafe_allow_html=True)

    # st.write("Selected Color:", f'{selected_color}: {next(color["code"] for color in colors if color["name"] == selected_color)}')
    # st.write("Selected Color2:", f'{selected_color2}: {next(color["code"] for color in colors if color["name"] == selected_color2)}')

    # # Find the corresponding color dictionaries
    # color1 = next(color for color in colors if color["name"] == selected_color)
    # color2 = next(color for color in colors if color["name"] == selected_color2)

    # # Mix the selected colors
    # mixed_color = mix_colors(color1["code"], color2["code"])
    # st.write("Mixed Color:", mixed_color)
    # st.markdown(
    #     f'<div style="background-color: {mixed_color}; width: 200px; height: 200px;"></div>',
    #     unsafe_allow_html=True,
    # )




    # Function to mix two hex colors
    def mix_colors(color1, color2):
        mixed_color = "#"
        for i in range(1, 7, 2):
            component1 = int(color1[i:i+2], 16)
            component2 = int(color2[i:i+2], 16)
            mixed_component = (component1 + component2) // 2
            mixed_color += f"{mixed_component:02x}"
        return mixed_color

    def generate_css_for_options(colors: list) -> str:
        css = "<style>"
        for i, color in enumerate(colors):
            css += (
                f"""ul[data-testid="stSelectboxVirtualDropdown"] li[role="option"]:nth-child({i + 1})"""
                + "{"
                + f"background-color: {color['code']}; color: {color['text_color']};"
                + "}"
            )
        css += "</style>"
        return css

    def generate_css_for_box(color_name: str) -> str:
        css = "<style>"
        for color in colors:
            if color["name"] == color_name:
                css += (
                    """div[data-baseweb="select"] > div:first-child {"""
                    + f"background-color: {color['code']}; color: {color['text_color']};"
                    + "}"
                )
                break
        css += "</style>"
        return css

    # Define the colors
    colors1 = [
        {"code": "#101B58", "name": "Penn Blue", "text_color": "#FFFFFF"},
        {"code": "#45296C", "name": "Tekhelet", "text_color": "#FFFFFF"},
        {"code": "#793780", "name": "Eminence", "text_color": "#FFFFFF"},
        {"code": "#AD4594", "name": "Fandango", "text_color": "#FFFFFF"},
        {"code": "#E153A8", "name": "Brilliant Rose", "text_color": "#FFFFFF"},
        {"code": "#F0A998", "name": "Melon", "text_color": "#FFFFFF"},
        {"code": "#F8D490", "name": "Sunset", "text_color": "#000000"},
        {"code": "#FFFF88", "name": "Icterine", "text_color": "#000000"},

    ]

    colors2 = [
        {"code": "#FF0000", "name": "Red", "text_color": "#FFFFFF"},
        {"code": "#00FF00", "name": "Green", "text_color": "#000000"},
        {"code": "#0000FF", "name": "Blue", "text_color": "#FFFFFF"},
        {"code": "#FFFF00", "name": "Yellow", "text_color": "#000000"},
        {"code": "#FFA500", "name": "Orange", "text_color": "#000000"},
        {"code": "#800080", "name": "Purple", "text_color": "#FFFFFF"},
        {"code": "#FFC0CB", "name": "Pink", "text_color": "#000000"},
        {"code": "#808080", "name": "Gray", "text_color": "#FFFFFF"},
        {"code": "#FFFFFF", "name": "White", "text_color": "#000000"},
        {"code": "#000000", "name": "Black", "text_color": "#FFFFFF"},
        {"code": "#A52A2A", "name": "Brown", "text_color": "#FFFFFF"},
        {"code": "#008000", "name": "Dark Green", "text_color": "#FFFFFF"},
    ]

    colors = st.segmented_control("Цветове", ["Основни", "Други"], default="Основни")
    if colors == "Основни":
        colors = colors2
    else:
        colors = colors1

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown(generate_css_for_options(colors), unsafe_allow_html=True)
        options = [color["name"] for color in colors]
        selected_color = st.selectbox(label="Избери цвят 1", options=options, key="color_selected")
        st.markdown(generate_css_for_box(selected_color), unsafe_allow_html=True)

    with col2:
        st.markdown(generate_css_for_options(colors), unsafe_allow_html=True)
        options2 = [color["name"] for color in colors]
        selected_color2 = st.selectbox(label="Избери цвят 2", options=options2, key="color_selected2")
        st.markdown(generate_css_for_box(selected_color2), unsafe_allow_html=True)

    st.write("Selected Color:", f'{selected_color}: {next(color["code"] for color in colors if color["name"] == selected_color)}')
    st.write("Selected Color2:", f'{selected_color2}: {next(color["code"] for color in colors if color["name"] == selected_color2)}')

    # Find the corresponding color dictionaries
    color1 = next(color for color in colors if color["name"] == selected_color)
    color2 = next(color for color in colors if color["name"] == selected_color2)

    # Mix the selected colors
    mixed_color = mix_colors(color1["code"], color2["code"])
    st.write("Mixed Color:", mixed_color)
    st.markdown(
        f'<div style="background-color: {mixed_color}; width: 200px; height: 200px;"></div>',
        unsafe_allow_html=True,
    )