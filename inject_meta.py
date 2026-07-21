"""Patches Streamlit's own static/index.html to add Open Graph / Twitter
Card meta tags, since Streamlit only updates document.title client-side
via JavaScript after load - link-preview crawlers (iMessage, Slack,
LinkedIn) fetch the raw HTML and never run JS, so they never see that.

Runs as a build step (see Render's Build Command) since it patches an
installed package file that gets reinstalled fresh on every deploy.
"""
import os
import streamlit

INDEX_PATH = os.path.join(os.path.dirname(streamlit.__file__), "static", "index.html")

TITLE = "Insolla — Salesforce Intelligence"
DESCRIPTION = ("RAG app answering natural-language questions over live "
               "Salesforce data. OpenAI + LangChain + Pinecone.")
IMAGE = ("https://raw.githubusercontent.com/brianshimkus/"
         "Insolla-Salesforce-RAG/main/screenshot.png")
URL = "https://rag.insolla.ai/"

META_TAGS = f"""    <meta property="og:title" content="{TITLE}" />
    <meta property="og:description" content="{DESCRIPTION}" />
    <meta property="og:image" content="{IMAGE}" />
    <meta property="og:url" content="{URL}" />
    <meta property="og:type" content="website" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{TITLE}" />
    <meta name="twitter:description" content="{DESCRIPTION}" />
    <meta name="twitter:image" content="{IMAGE}" />
"""

with open(INDEX_PATH) as f:
    html = f.read()

if 'property="og:title"' in html:
    print("Meta tags already present, skipping")
else:
    html = html.replace(
        "<title>Streamlit</title>",
        f"<title>{TITLE}</title>\n{META_TAGS}",
    )
    with open(INDEX_PATH, "w") as f:
        f.write(html)
    print(f"Injected Open Graph meta tags into {INDEX_PATH}")
