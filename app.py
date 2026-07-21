import streamlit as st
from rag import answer_with_sources

st.set_page_config(page_title="Insolla — Salesforce Intelligence", page_icon="🔎")

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

q = None
q_kwargs = {}

if not st.session_state.history:
    st.write("Not sure where to start? Try one of these:")
    # Each sample carries its own retrieval strategy. The deal-amount
    # question uses a Pinecone metadata filter instead of plain semantic
    # search - "over $100k" is a numeric threshold, and embeddings alone
    # can't reliably match that, only topical similarity.
    sample_prompts = [
        ("What issues has Edge Communications reported?",
         {"filter": {"type": "case"}, "k": 4}),
        ("Tell me about United Oil & Gas Corp.", {}),
        ("Which open deals are worth over $100k?", {
            "filter": {"type": "opportunity", "is_closed": False,
                       "amount": {"$gte": 100000}},
            "k": 10,
        }),
    ]
    for prompt, kwargs in sample_prompts:
        if st.button(prompt, use_container_width=True):
            q = prompt
            q_kwargs = kwargs

if typed := st.chat_input("Ask about accounts, cases, escalations..."):
    q = typed

if q:
    st.chat_message("user").write(q)
    st.session_state.history.append(("user", q, None))

    with st.spinner("Searching Salesforce data..."):
        a, docs = answer_with_sources(q, **q_kwargs)

    with st.chat_message("assistant"):
        st.write(a)
        with st.expander(f"Based on these {len(docs)} Salesforce records"):
            for d in docs:
                st.write("—", d.page_content)
    st.session_state.history.append(("assistant", a, docs))
