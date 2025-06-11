import streamlit as st

from database import get_candidates, get_candidate_details
from agent import create_react_agent

st.title("Candidates List")


candidates = get_candidates()
candidate_names = [f"{name} ({file_name})" for file_name, name, _, _ in candidates]

selected = st.selectbox("Select a candidate:", candidate_names)

if selected:
    file_name = selected.split("(")[-1].replace(")", "")
    details = get_candidate_details(file_name)

    tab1, tab2 = st.tabs(["Candidate Agent Chat", "Candidate Details"])

    with tab1:
        if "messages" not in st.session_state:
            st.session_state.messages = []

        if (
            "agent_file" not in st.session_state
            or st.session_state.agent_file != file_name
        ):
            st.session_state.agent = create_react_agent(file_name)
            st.session_state.agent_file = file_name
            st.session_state.messages = []

        st.subheader("Candidate Agent Chat")
        st.markdown(
            "This agent can answer candidate-related questions, stock-market queries, and general-knowledge inquiries."
        )
        st.markdown("**Example questions:**")
        st.markdown(
            "- What is the stock price of the company where the candidate is seeking employment?"
        )
        st.markdown(
            "- What's the highest mountain in the state where the candidate's prospective employer is headquartered?"
        )

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Ask a question or type your prompt here..."):
            with st.chat_message("user"):
                st.markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})

            agent = st.session_state.agent
            with st.spinner("Agent is thinking..."):
                response = agent.chat(prompt)
            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

    with tab2:
        if details:
            st.subheader("Candidate Details")
            st.write(f"**Name:** {details.get('name')}")
            st.write(f"**Profession:** {details.get('profession')}")
            st.write(f"**Years of Experience:** {details.get('years_of_experience')}")
            st.write(f"**Summary:** {details.get('summary')}")
        else:
            st.warning("Details not found for this candidate.")
