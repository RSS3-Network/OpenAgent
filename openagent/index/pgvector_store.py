from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_postgres.vectorstores import PGVector
from toolz import memoize

from openagent.conf.env import settings

load_dotenv()


@memoize
def build_vector_store() -> PGVector:
    collection_name = "backend"
    if settings.VERTEX_PROJECT_ID:
        underlying_embeddings = VertexAIEmbeddings(model_name="textembedding-gecko@003", project=settings.VERTEX_PROJECT_ID)

    elif settings.GOOGLE_GEMINI_API_KEY:
        underlying_embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=settings.GOOGLE_GEMINI_API_KEY)
    else:
        underlying_embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    return PGVector(
        embeddings=underlying_embeddings,
        collection_name=collection_name,
        connection=settings.DB_CONNECTION,
        use_jsonb=True,
    )
