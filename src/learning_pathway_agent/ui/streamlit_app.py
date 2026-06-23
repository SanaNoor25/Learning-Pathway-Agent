import requests
import streamlit as st

st.title("Learning Pathway Agent")
user_input = st.text_area("Student Context (paste plain text or JSON)")

target_role = st.text_input("Target Role (e.g. data_scientist)")

if st.button("Run Crew"):
    try:
        response = requests.post(
            "http://localhost:8000/run",
            json={
                "context": user_input,
                "target_role": target_role,
            },
            timeout=300,
        )
        response.raise_for_status()
        data = response.json()
        final_output = data.get("output", "")

        if final_output:
            st.markdown(final_output)
        else:
            st.error("No output was returned from the API.")
    except Exception as e:
        st.error(str(e))
