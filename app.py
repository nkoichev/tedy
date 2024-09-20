import streamlit as st
import random
import time
from streamlit_echarts import st_echarts, st_pyecharts
from pyecharts import options as opts
from pyecharts.charts import Bar


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

# Function to generate new math problems
def new_numbers():
    st.session_state.problems = []
    for _ in range(5):
        num1 = random.randint(0, 10)
        num2 = random.randint(0, 10)
        operator = "+"
        answer = num1 + num2
        st.session_state.problems.append((num1, operator, num2, answer))

if st.session_state.problems == []:
    new_numbers()

# Button for refreshing problems
with column3:
    button_reload = st.button("Обнови")

if button_reload:
    progress_text = ":) :) :)"
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.005)
        my_bar.progress(percent_complete + 1, text=progress_text)
    time.sleep(0.5)
    my_bar.empty()
    st.session_state.user_answers = [None] * 5

    new_numbers()
    st.snow()

if 'problems' not in st.session_state:
    new_numbers()

# Initialize user answers
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = [None] * 5

# Score calculation
score_true = 0
score_false = 0
score = 0
for i, (num1, operator, num2, answer) in enumerate(st.session_state.problems):
    col1, col2, col3, col4, col5, col6 = st.columns([0.5, 0.3, 0.5,0.5, 1,2], gap="small", vertical_alignment="top")
    
    # Display num1 as GIF
    with col1:
        st.image(f"gifs/{num1}.gif")
    
    # Display operator
    with col2:
        st.write("")
        st.image(f"gifs/plus.png")
    
    # Display num2 as GIF
    with col3:
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

# Show score
# st.write(f"Резултат: {score}/5")
# st.write(f"Правилни отговори: {score_true}")
# st.write(f"Грешни отговори: {score_false}")

st.session_state.show_answers = False

if score_true == 5:
    st.balloons()
    time.sleep(0.8)
    st.balloons()
    time.sleep(0.8)
    st.balloons()
    time.sleep(0.8)
    st.balloons()


with col6:

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
        "radius": "70%",
        "data": [
            {"value": round(score_true,0), "name": "Верни", "itemStyle": {"color": "#7efc89"}},
            {"value": round(score_false,0), "name": "Грешни", "itemStyle": {"color": "#de5770"}}  
        ],
        "emphasis": {
            "itemStyle": {
            "shadowBlur": 10,
            "shadowOffsetX": 0,
            "shadowColor": "rgba(0, 0, 0, 0.5)"
            }
        }
        }
    ]
    })