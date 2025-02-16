import streamlit as st
from app.pages import user_profile, proposal_writer

st.set_page_config(page_title="Grantd", layout="wide")

st.sidebar.title("Grantd - AI Grant Assistant")
page = st.sidebar.radio("Navigate", ["🏠 Home", "🔍 Search Grants", "✍️ Write Proposal", "✅ Check Eligibility"])

if page == "🔍 Search Grants":
    grant_search.show()
elif page == "User Profile":
    user_profile.show()
elif page == "✍️ Write Proposal":
    proposal_writer.show()
else:
    st.markdown("# Welcome to Grantd 🚀")
    st.markdown("AI-powered grant assistant to help you secure funding!")

if __name__ == "__main__":
    main()