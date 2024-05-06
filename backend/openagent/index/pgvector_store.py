from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_postgres.vectorstores import PGVector

from openagent.conf.env import settings

load_dotenv()


def build_vector_store() -> PGVector:
    collection_name = "backend"
    underlying_embeddings = OpenAIEmbeddings()
    return PGVector(
        embeddings=underlying_embeddings,
        collection_name=collection_name,
        connection=settings.VEC_DB_CONNECTION,
        use_jsonb=True,
    )


if __name__ == "__main__":
    store = build_vector_store()

    docs = [
        Document(
            page_content="there are cats in the pond",
            metadata={"id": 1, "location": "pond", "topic": "animals"},
        ),
        Document(
            page_content="ducks are also found in the pond",
            metadata={"id": 2, "location": "pond", "topic": "animals"},
        ),
    ]
    store.add_documents(docs, ids=[doc.metadata["id"] for doc in docs])
