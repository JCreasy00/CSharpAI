import chromadb

# create a persistent client
client = chromadb.HttpClient(host='localhost', port=8000)

# create and get the function
# note that once the collection is created it does not need to be created again or -> "error":"ValueError('Collection my_collection already exists.')"
# collection = client.create_collection(name="my_collection")
collection = client.get_collection(name="my_collection")

# print(collection.peek())
# print(collection.count())

# lets try and add some stuff to our collection my_collection
# the same goes for adding to the collection, once it is added it does not need to be added again
# collection.add(
#     documents=["This is document1", "This is document2"], # we handle tokenization, embedding, and indexing automatically. You can skip that and add your own embeddings as well
#     metadatas=[{"source": "notion"}, {"source": "google-docs"}], # filter on these!
#     ids=["doc1", "doc2"],
# )

# now when we peek or count we see that we have some files.
# print(collection.peek())
# print(collection.count())

collection.add(
    documents=["This is a que document1", "This query"],
    metadatas=[{"source": "notion"}, {"source": "google-docs"}], # filter on these!
    ids=["doc3","doc4"]
)

# Query/search 2 most similar results. You can also .get by id
results = collection.query(
    query_texts=["This is a query document"],
    n_results=2,
    # where={"metadata_field": "is_equal_to_this"}, # optional filter
    # where_document={"$contains":"search_string"}  # optional filter
)

print(results)