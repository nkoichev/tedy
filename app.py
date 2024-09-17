import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import random
import time

st.write("Здравей, Теди!")

if "show_answers" not in st.session_state:
    st.session_state.show_answers = False

column1, column2, column3 = st.columns(3, gap="small")

with column1:
    button_show = st.button("Покажи отговорите")
    if button_show:
        st.session_state.show_answers = True
with column2:
    button_hide = st.button("Скрий отговорите")
    if button_hide:
        st.session_state.show_answers = False






with column3:
    button_reload = st.button("Обнови")


if button_reload:
    progress_text = ":) :) :)"
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)
    time.sleep(1)
    my_bar.empty()
    st.session_state.user_answers = [None] * 10
    st.balloons()
# Initialize session state for problems and answers
if 'problems' not in st.session_state:
    st.session_state.problems = []
    for i in range(10):
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        operator = random.choice(["+"])
        if operator == "+":
            answer = num1 + num2
        else:
            answer = num1 - num2
        st.session_state.problems.append((num1, operator, num2, answer))

# Initialize session state for user answers
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = [None] * 10

# Score calculation
score_true = 0
score_false = 0
score = 0
for i, (num1, operator, num2, answer) in enumerate(st.session_state.problems):
    col1, col2, col3, col4 = st.columns([0.8, 0.8, 4, 1], gap="small", vertical_alignment = "bottom")
    with col1:
        #st.write("")
        st.write("")
        st.write(f"{num1} {operator} {num2} =")
    with col2:
        user_input = st.number_input(label="", format="%0.0f", value=st.session_state.user_answers[int(i)] or None, key=f"input_{i}")
    st.session_state.user_answers[i] = user_input

    # Check if the answer is correct
    if user_input == answer:
        with col3:
            st.success(f":green[Вярно!]", icon="✅")
        score += 1
        score_true += 1
    else:
        # time.sleep(2)
        if st.session_state.user_answers[i] != None:
            with col3:
                st.error(f":red[Грешно!]", icon="⚠️")
            
                

        if st.session_state.show_answers:
            with col3:
                st.success(f':green[{answer}]')
        score_false += 1

# Show score
st.write(f"Your score: {score}/10")
st.write(f"True answers: {score_true}")
st.write(f"False answers: {score_false}")

st.session_state.show_answers = False