import streamlit as st

st.title("Potential Lens")
st.write("Find hidden potential, not just keywords.")

resume = st.text_area("Paste a resume here")
role = st.text_input("Target role", "Customer Success Manager")

if st.button("Analyze"):
    st.write("Analysis coming soon for:", role)
    st.write(resume[:200])