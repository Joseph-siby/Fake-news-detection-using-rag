# test_rag.py

from rag.retriever_pipeline import retrieve

def test_rag():
    claim = "NASA discovers water on the Moon"
    
    print(f"Claim: {claim}\n")
    
    top_evidence = retrieve(claim, top_k=3)
    
    print("Top 3 retrieved evidence snippets:")
    for i, snippet in enumerate(top_evidence, 1):
        print(f"{i}. {snippet}")

if __name__ == "__main__":
    test_rag()
