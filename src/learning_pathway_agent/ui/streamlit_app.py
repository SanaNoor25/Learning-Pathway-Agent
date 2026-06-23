import streamlit as st
import requests

import json
st.title("Learning Pathway Agent")
user_input = st.text_area("Student Context (paste plain text or JSON)")

target_role = st.text_input("Target Role (e.g. data_scientist)")
if st.button("Run Crew"):

    response = requests.post(
        "http://localhost:8000/run",
        json={
            "context": user_input,
            "target_role": target_role
        },
        stream=True
    )

    logs = ""

    for line in response.iter_lines():
        if line:
            decoded = line.decode()

            if decoded.startswith("data: "):
                msg = decoded[6:]

                if "[FINAL]" in msg:
                    st.success(msg.replace("[FINAL]", ""))
                elif "[ERROR]" in msg:
                    st.error(msg)
                else:
                    logs += msg + "\n"
                    st.text_area("Live Logs", logs, height=300)