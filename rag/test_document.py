from rag.retriever_pipeline import retrieve_from_document

file_path = "test.pdf"

# Interactive query input
query = input("Enter a keyword/topic to search in the document: ").strip()
top_k = 3  # number of top chunks to display

# Retrieve relevant chunks
top_chunks = retrieve_from_document(file_path, query, top_k=top_k)

print("\nTop relevant chunks from document:\n")

if not top_chunks or top_chunks == ["Not found"]:
    print("No relevant content found for your query.")
else:
    for i, chunk in enumerate(top_chunks, 1):
        print(f"{i}. {chunk}\n")


