import streamlit as st
from rag import answer_with_sources

st.title("Insolla — Salesforce Intelligence")
st.caption("RAG over live Salesforce data · OpenAI + LangChain + Pinecone")

if "history" not in st.session_state:
    st.session_state.history = []

for role, msg, sources in st.session_state.history:
    with st.chat_message(role):
        st.write(msg)
        if sources:
            with st.expander(f"Based on these {len(sources)} Salesforce records"):
                for s in sources:
                    st.write("—", s.page_content)

if q := st.chat_input("Ask about accounts, cases, escalations..."):
    st.chat_message("user").write(q)
    st.session_state.history.append(("user", q, None))

    with st.spinner("Searching Salesforce data..."):
        a, docs = answer_with_sources(q)

    with st.chat_message("assistant"):
        st.write(a)
        with st.expander(f"Based on these {len(docs)} Salesforce records"):
            for d in docs:
                st.write("—", d.page_content)
    st.session_state.history.append(("assistant", a, docs))
