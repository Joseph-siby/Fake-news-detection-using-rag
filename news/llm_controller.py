import json
import re

from news.tavily_api import tavily_search
from llm.llm_service import ask_llm


def estimate_source_credibility(source):

    prompt = f"""
You are a news credibility evaluator.

Analyze the following news source and estimate
its credibility score from 0-100.

Evaluate based on:
- writing professionalism
- evidence quality
- factual tone
- reliability of reporting
- neutrality

Title:
{source.get("title", "")}

Content:
{source.get("content", "")[:1200]}

URL:
{source.get("url", "")}

Respond ONLY in JSON format:

{{
    "trust_score": 78,
    "reason": "short explanation"
}}
"""

    response = ask_llm(prompt)

    try:
        json_match = re.search(r"\{.*?\}", response, re.DOTALL)

        if json_match:
            parsed = json.loads(json_match.group())

            return {
                "trust_score": parsed.get("trust_score", 50),
                "reason": parsed.get(
                    "reason",
                    "No explanation provided."
                )
            }

    except Exception as e:
        print("SOURCE CREDIBILITY ERROR:", e)

    return {
        "trust_score": 50,
        "reason": "Unable to estimate credibility"
    }


def rag_with_credibility_gate(query: str):

    tavily_response = tavily_search(query)
    results = tavily_response.get("results", [])

    if not results:
        return {
            "answer": tavily_response.get("answer"),
            "overall_analysis": {
                "credible": False,
                "reason": "No sources found."
            },
            "sources": []
        }

    combined_snippets = "\n\n".join(
        [r["content"] for r in results]
    )

    print("QUERY LENGTH:", len(query))
    print("NUM RESULTS:", len(results))
    print("TOTAL SNIPPET LENGTH:", len(combined_snippets))

    # -------- OVERALL RAG ANALYSIS --------

    evaluation_prompt = f"""
You are a credibility evaluation system.

Claim:
{query}

Retrieved Evidence Snippets:
{combined_snippets}

Respond strictly in JSON format:

{{
  "credible": true or false,
  "reason": "short explanation"
}}
"""

    decision = ask_llm(evaluation_prompt)

    try:
        json_match = re.search(r"\{.*?\}", decision, re.DOTALL)

        if json_match:
            parsed = json.loads(json_match.group())

            credible = parsed.get("credible", False)

            reason = parsed.get(
                "reason",
                "No explanation provided."
            )

        else:
            credible = False
            reason = "No JSON found in LLM response."

    except Exception as e:
        credible = False
        reason = f"LLM parsing error: {str(e)}"

    # -------- SOURCE-WISE TRUST ANALYSIS --------

    source_analysis = []

    for source in results:

        credibility_data = estimate_source_credibility(source)

        source_analysis.append({
            "title": source.get("title"),
            "url": source.get("url"),
            "content": source.get("content"),
            "trust_score": credibility_data["trust_score"],
            "credibility_reason": credibility_data["reason"]
        })

    # -------- FINAL RESPONSE --------

    return {
        "answer": tavily_response.get("answer"),

        "overall_analysis": {
            "credible": credible,
            "reason": reason
        },

        "sources": source_analysis if credible else []
    }