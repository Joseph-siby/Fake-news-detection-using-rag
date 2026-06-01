from fastapi import FastAPI, UploadFile, File, Form, Body
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from news.llm_controller import rag_with_credibility_gate
from news.explain_controller import explain_from_sources
from gemini.image_service import describe_image_file

# ✅ NEW: context builder
from news.utils import build_news_query


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5175",
        "http://127.0.0.1:5175"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----------- Models -----------

class QueryInput(BaseModel):
    query: str

class ExplainInput(BaseModel):
    query: str
    sources: list


# ----------- Routes -----------

@app.post("/search")
async def search_from_frontend(
    data: QueryInput = Body(None),
    query: str = Form(None),
    image: UploadFile = File(None)
):
    print("\n========== NEW REQUEST ==========")

    print("JSON BODY:", data)
    print("FORM QUERY:", query)
    print("IMAGE:", image.filename if image else None)

    final_query = None

    # ----------- IMAGE FLOW -----------
    if image is not None and image.filename:
        print("➡️ IMAGE DETECTED → RUNNING IMAGE MODEL")

        try:
            image_desc = describe_image_file(image)
            print("IMAGE DESCRIPTION:", image_desc)

            if not image_desc or image_desc.startswith("Error"):
                print("❌ IMAGE PROCESSING FAILED")
                return {"error": "Image processing failed"}

            # ✅ Extract only description
            description_only = (
                image_desc.split("Usefulness:")[0]
                .replace("Description:", "")
                .strip()
            )

            print("EXTRACTED DESCRIPTION:", description_only)

            # ✅ NEW: convert to smart news query
            final_query = build_news_query(description_only)

            print("TRANSFORMED QUERY:", final_query)

        except Exception as e:
            print("❌ IMAGE PIPELINE ERROR:", str(e))
            return {"error": "Image processing error"}

    # ----------- TEXT FLOW -----------
    else:
        print("➡️ TEXT FLOW")

        if data is not None and hasattr(data, "query"):
            final_query = data.query
            print("USING JSON QUERY")

        if (not final_query or final_query.strip() == "") and query:
            final_query = query
            print("USING FORM QUERY")

    # ----------- FINAL VALIDATION -----------
    print("FINAL QUERY BEFORE CLEAN:", final_query)

    if not final_query or final_query.strip() == "":
        print("❌ ERROR: EMPTY QUERY")
        return {"error": "Empty query received"}

    final_query = final_query.strip()
    print("FINAL QUERY SENT TO RAG:", final_query)

    # ----------- RAG CALL -----------
    try:
        result = rag_with_credibility_gate(final_query)
        print("RAG RESULT:", result)

        if not result:
            print("❌ EMPTY RESPONSE FROM MODEL")
            return {"error": "Model returned empty response"}

        return result

    except Exception as e:
        print("❌ RAG ERROR:", str(e))
        return {"error": "Internal model error"}


@app.post("/explain")
def explain(data: ExplainInput):
    explanation = explain_from_sources(data.query, data.sources)
    return {"explanation": explanation}