from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from bs4 import BeautifulSoup
import requests

# ✅ Import the working Tavily function
from tavily_api import tavily_search

app = FastAPI()


def extract_full_content(url: str):
    response = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=10
    )

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove unwanted tags
    for tag in soup(["script", "style"]):
        tag.decompose()

    return soup.get_text(separator="\n")


@app.get("/view-source", response_class=HTMLResponse)
def view_source(query: str):
    try:
        # Use imported working function
        data = tavily_search(query)
        results = data.get("results", [])

        if not results:
            return "<h2>No sources found</h2>"

        first_url = results[0]["url"]
        content = extract_full_content(first_url)

        return f"""
        <html>
            <body style="background:white; color:black; padding:20px;">
                <h2>First Source URL:</h2>
                <p><a href="{first_url}" target="_blank">{first_url}</a></p>
                <hr>
                <pre style="white-space: pre-wrap;">{content}</pre>
            </body>
        </html>
        """

    except Exception as e:
        return f"<h2>Error:</h2><pre>{str(e)}</pre>"
