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

st.set_page_config("Cognitive Biases Experiment", None, "wide", "expanded")

sidebar = st.sidebar

if "admin" not in st.session_state:

    st.session_state.admin = False
    st.session_state.qnum = 0

import src
data = src.data
df = pd.DataFrame().from_dict(data)

def savedata():
    open("src.py", "w").write(f"data = {data}")
    df = pd.DataFrame.from_dict(data)

def updateuser(userid, col, value):

    print(data["ID"])
    print(userid)

    for i in range(len(data["ID"])):
        if data["ID"][i] == userid:
            print("ID FOUND")
            data[col][i] = value

pages = {
    "Admin": ["Controls", "Data", "Tested Biases"],
    "User": ["Home", "Survey"]
}

questions = {

    "Q1": {
        "question": "Death By Train",
        "desc": "A train is heading towards an old couple, who are trying to slowly cross the tracks. On another set of tracks is a litter of 10 kittens. You are a good distance away, close enough to see them, but too far to be heard. Right next to you, there is a lever to switch the tracks.",
        "options": ["No", "Yes"]
    },

    "Q2": {
        "question": "Killed By A Train",
        "desc": "A train is heading towards an old couple, who are trying to slowly cross the tracks. On another set of tracks is a litter of 10 kittens. You are a good distance away, close enough to see them, but too far to be heard. Right next to you, there is a lever to switch the tracks.",
        "options": ["Let the couple die", "Kill the kittens"]
    },

    "Q3": {
        "question": "Killed By Bystander",
        "desc": "You are standing on a bridge, which extends over a road. Below, there is a car - with a family of 4 - on a direct collision course with a drunk driver's car going the opposite direction. On the bridge, there is a child sitting on the railing, their parents nowhere in sight. You know that if you push the child down, the family will swerve out of the way in time to avoid the drunk driver, but the child will surely die.",
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
            
            uid = "".join([str(random.randint(1, 9)) for i in range(3)])
            
            newdata = ["Logged In", uid, lastname, firstname, gender, age, 0, 0, 0, 0, 0]

            for i in range(len(data)):
                data[list(data.keys())[i]].append(newdata[i])

            try:
                st.write(f"**User ID: {uid}**")
                time.sleep(10)
                savedata()
            except:
                savedata()

if page == "Survey":

    with st.empty():

        if st.session_state.qnum == 0:

            with st.container():

                st.title("Bias Experiment Survey")

                st.write("**This will be a short survey, consisting of 3 questions, with no breaks in between.**")
                st.write("**You will have 15 seconds to answer the first two, and 20 seconds for the last one. Put in your answer and hit \"Submit\"**")
                st.write("**Don't think too hard; just do what you feel is best in that scenario.**")
                st.write("When you are ready, hit Ready. I will tell you when to start. When I do, hit Start - you may have to hit some buttons twice for them to work.")


                if st.button("Ready"):
                    updateuser(loginid, "Status", "Ready")
                    print(data)

                if st.button("Start"):
                    st.session_state.qnum = 1

        elif st.session_state.qnum == 1:

            with st.container():

                st.title(questions["Q1"]["question"])
                st.write(questions["Q1"]["desc"])

                choice = st.radio("Do you switch them?", questions["Q1"]["options"])
                
                if st.button("Next"):
                    updateuser(loginid, "Q1", choice)
                    st.session_state.qnum += 1

                try:
                    time.sleep(15)
                    updateuser(loginid, "Q1", choice)
                    savedata()
                    st.session_state.qnum += 1

                except:
                    updateuser(loginid, "Q1", choice)
                    savedata()
                    st.session_state.qnum += 1

        elif st.session_state.qnum == 2:

            with st.container():

                st.title(questions["Q2"]["question"])
                st.write(questions["Q2"]["desc"])
                
                choice = st.radio("Do you kill the kittens, or let the couple die?", questions["Q2"]["options"])
                
                if st.button("Next"):
                    updateuser(loginid, "Q2", choice)
                    st.session_state.qnum += 1

                try:
                    time.sleep(15)
                    updateuser(loginid, "Q2", choice)
                    savedata()
                    st.session_state.qnum += 1

                except:
                    updateuser(loginid, "Q2", choice)
                    savedata()
                    st.session_state.qnum += 1

        elif st.session_state.qnum == 3:

            with st.container():

                st.title(questions["Q3"]["question"])
                st.write(questions["Q3"]["desc"])
                
                choice = st.radio("Do you push the child?", questions["Q3"]["options"])
                
                if st.button("Next"):
                    updateuser(loginid, "Q3", choice)
                    st.session_state.qnum += 1

                try:
                    time.sleep(20)
                    updateuser(loginid, "Q3", choice)
                    savedata()
                    st.session_state.qnum += 1

                except:
                    updateuser(loginid, "Q3", choice)
                    savedata()
                    st.session_state.qnum += 1

        else:

            st.title("Survey Complete.")

if page == "Data":
    
    st.subheader("Test Data")
    st.write(f"**Total Participants: {len(data['ID'])}**")
    st.dataframe(data, hide_index=True, use_container_width=True)

if page == "Controls":

    st.title("Survey Controls")

    c1, c2 = st.columns(2)

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
            "Age": [],
            "Q1": [],
            "Q2": [],
            "Q3": []
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

    st.write("---")
    st.header("Experiment QR Code")
    st.write("---")
    st.image("qrcode.jpeg", width=600)

if page == "Tested Biases":
    st.title("Tested Biases")
    st.write("---")
    st.header("Egocentric Bias")
    st.write("The human tendency to be biased in favour of one’s own perspective; stubbornness. The extent of this varies from person to person, but in general, it’s usually best to keep an open mind whenever possible, as this is the only way to learn from other people.")
    st.header("Affect Heuristic Bias")
    st.write("The way humans rely on emotion to some extent in making quick decisions. This is evident when there is a short time limit on decisions, and therefore can lead to unfavourable outcomes.")
