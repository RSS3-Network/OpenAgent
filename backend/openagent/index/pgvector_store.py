from dotenv import load_dotenv
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_postgres.vectorstores import PGVector

from openagent.conf.env import settings

load_dotenv()


def build_vector_store() -> PGVector:
    collection_name = "backend"
    underlying_embeddings = VertexAIEmbeddings(
        model_name="textembedding-gecko@003", project=settings.PROJECT_ID
    )
    return PGVector(
        embeddings=underlying_embeddings,
        collection_name=collection_name,
        connection=settings.VEC_DB_CONNECTION,
        use_jsonb=True,
    )


store = build_vector_store()
