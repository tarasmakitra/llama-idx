import streamlit as st

from database import get_candidates, get_candidate_details

st.title("Candidates List")


candidates = get_candidates()
candidate_names = [f"{name} ({file_name})" for file_name, name, _, _ in candidates]

selected = st.selectbox("Select a candidate:", candidate_names)

if selected:
    file_name = selected.split("(")[-1].replace(")", "")
    details = get_candidate_details(file_name)
    if details:
        st.subheader("Candidate Details")
        st.write(f"**Name:** {details.get('name')}")
        st.write(f"**Profession:** {details.get('profession')}")
        st.write(f"**Years of Experience:** {details.get('years_of_experience')}")
        st.write(f"**Summary:** {details.get('summary')}")
    else:
        st.warning("Details not found for this candidate.")
