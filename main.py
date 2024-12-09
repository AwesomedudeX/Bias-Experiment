import streamlit as st

requirements = """
numpy
pandas
matplotlib
seaborn
"""

reqs = open("requirements.txt", "w")
reqs.write(requirements)


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn
import numpy as np
import os
import time

from numpy import random

st.set_page_config("Cognitive Biases Experiment", None, "wide", "auto")

sidebar = st.sidebar

if "admin" not in st.session_state:

    st.session_state.admin = False
    st.session_state.qnum = 0

try:
    import src
    data = src.data
    df = pd.DataFrame().from_dict(data)

except:
    data = {
        "Status": [],
        "ID": [],
        "Surname": [],
        "Name": [],
        "Gender": [],
        "Age": [],
        "Q1": [],
        "Q2": [],
        "Q3": []
    }
    open("src.py", "w").write(f"data = {data}")

def savedata():
    open("src.py", "w").write(f"data = {data}")
    df = pd.DataFrame.from_dict(data)

pages = {
    "Admin": ["Controls", "Statistics", "Data", "Tested Biases"],
    "User": ["Home", "Survey"]
}

st.session_state.questions = {

    "Q1": {
        "question": "Death By Train",
        "desc": "A train is heading towards an old couple, who are trying to slowly cross the tracks. On another set of tracks is a litter of 10 kittens. You are a good distance away, close enough to see them, but too far to be heard. Right next to you, there is a lever to switch the tracks. Do you switch them?",
        "options": ["No", "Yes"]
    },

    "Q2": {
        "question": "Killed By A Train",
        "desc": "A train is heading towards an old couple, who are trying to slowly cross the tracks. On another set of tracks is a litter of 10 kittens. You are a good distance away, close enough to see them, but too far to be heard. Right next to you, there is a lever to switch the tracks. Do you kill the kittens, or let the couple die?",
        "options": ["Let the couple die", "Kill the kittens"]
    },

    "Q3": {
        "question": "Killed By Bystander",
        "desc": "You are standing on a bridge, which extends over a road. Below, there is a car - with a family of 4 - on a direct collision course with a drunk driver's car going the opposite direction. On the bridge, there is a child sitting on the railing, their parents nowhere in sight. You know that if you push the child down, the family will swerve out of the way in time to avoid the drunk driver, but the child will surely die. Do you push the child?",
        "options": ["Let the family die", "Push the child", "Sacrifice yourself (jump)"]
    },

}

sidebar.button("Refresh Page")

login = sidebar.expander(":red[**Login**]")
usermode = login.radio("User Type:", ["Test Subject", "Admin"])

loginsuccess = False

if usermode == "Admin":

    pwd = login.text_input(":red[**Enter Admin Password:**]")

    if pwd == str(st.secrets.password):
        st.session_state.admin = True

else:

    loginid = login.text_input("Enter your 3-digit user ID:", max_chars=3)

    if loginid != "":

        for i in range(len(data["ID"])):
            
            if data["ID"][i] == loginid:
                loginsuccess = True
                login.write(f"**Logged in as Test Subject.**\n\n**Welcome, :green[{data['Name'][i]} {data['Surname'][i]}].**")


        if not loginsuccess:
            login.write("**:red[INVALID ID.]**")



if st.session_state.admin:
    nav = sidebar.radio("**:blue[Navigation:]**", [f"**{p}**" for p in pages["Admin"]])
else:
    nav = sidebar.radio("**:blue[Navigation:]**", [f"**{p}**" for p in pages["User"]])    
    
page = nav.strip("**")

if page == "Home":

    st.title("Cognitive Biases")
    st.write(":grey[**Your information will be anonymously presented to other participants. If you do not consent to this, do not participate in this experiment.**]")
    st.write("---")
    st.write(f"Fill out ALL information on this page, and hit Submit. Once done, you will recieve a user ID number.")
    st.write("Afterward, log in with the ID number **IMMEDIATELY** using the sidebar on the left - don't click on anything else.")
    st.write("Then, proceed to the survey. If you forget your ID number, ask me, and I'll give it to you.")

    c1, c2 = st.columns(2)

    firstname = c1.text_input("**First Name:**")
    lastname = c2.text_input("**Last Name:**")
    age = c1.number_input("**Age (years):**", max_value=20)
    gender = c2.selectbox("**Gender:**", ["Male", "Female", "Non-Binary"])

    if firstname != "" and lastname != "" and age != 0:
        
        submit = st.button("Submit")

        if submit:
            
            id = "".join([str(random.randint(1, 9)) for i in range(3)])
            
            newdata = ["Logged In", id, lastname, firstname, gender, age, 0, 0, 0, 0, 0]

            for i in range(len(data)):
                data[list(data.keys())[i]].append(newdata[i])
            
            st.write(f"**User ID: {id}**")

        if loginsuccess:
            savedata()

if page == "Statistics":
    
    for q in st.session_state.questions:

        st.header(st.session_state.questions[q]['question'])

        st.write(st.session_state.questions[q]["desc"])
        
        for o in st.session_state.questions[q]['options']:
            st.write(f"**{o}: {'NaN'}%**")

if page == "Data":
    
    st.subheader("Test Data")
    st.write(f"**Total Participants: {len(data['ID'])}**")
    st.dataframe(data, hide_index=True, use_container_width=True)

if page == "Controls":

    st.title("Survey Controls")

    st.write(f"**Current Question: {st.session_state.qnum}**")

    c1, c2 = st.columns(2)

    prev = c1.button("Previous Question", use_container_width=True)
    next = c2.button("Next Question", use_container_width=True)

    c1a, c1b = c1.columns(2)

    if c1a.button("Clear System Log", use_container_width=True):
        os.system("cls")
    
    if c1b.button("Clear Data", use_container_width=True):
        data = {
            "Status": [],
            "ID": [],
            "Surname": [],
            "Name": [],
            "Gender": [],
            "Age": []
        }
        savedata()

    c2a, c2b = c2.columns(2)


    if c2a.button("Save Data", use_container_width=True):
        savedata()

    remove = c2b.expander("**:red[Remove a Participant]**")
    removeid = remove.text_input("Participant ID:", max_chars=3)
    removeuser = remove.button("Remove Participant", use_container_width=True)
    removesuccess = False

    if removeuser:
        
        if len(df) == 1:

            for col in data:
                data[col] = []
        
        else:

            for i in range(len(data["ID"])-1):
                
                if removeid == data["ID"][i]:

                    for col in data:
                        data[col].pop(i)

    if next:
        st.session_state.qnum += 1

    if prev and st.session_state.qnum > 0:
        st.session_state.qnum -= 1

if page == "Tested Biases":
    st.title("Tested Biases")
    st.write("---")
    st.header("Egocentric Bias")
    st.write("The human tendency to be biased in favour of one’s own perspective; stubbornness. The extent of this varies from person to person, but in general, it’s usually best to keep an open mind whenever possible, as this is the only way to learn from other people.")
    st.header("Affect Heuristic Bias")
    st.write("The way humans rely on emotion to some extent in making quick decisions. This is evident when there is a short time limit on decisions, and therefore can lead to unfavourable outcomes.")