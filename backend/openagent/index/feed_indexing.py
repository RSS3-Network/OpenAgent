import datetime

from dotenv import load_dotenv
from langchain.indexes import SQLRecordManager
from langchain_core.documents import Document
from langchain_core.indexing import index
from langchain_text_splitters import CharacterTextSplitter
from loguru import logger

from openagent.conf.env import settings
from openagent.index.feed_scrape import fetch_iqwiki_feeds
from openagent.index.pgvector_store import store

load_dotenv()

record_manager = SQLRecordManager("backend", db_url=settings.VEC_DB_CONNECTION)
record_manager.create_schema()


def _clear():
    index([], record_manager, store, cleanup="incremental", source_id_key="id")


def build_index():
    since_ts = 0
    curr_ts = int(datetime.datetime.now().timestamp())
    cursor = None
    logger.info(f"start indexing from {since_ts} to {curr_ts}")
    while True:
        resp = fetch_iqwiki_feeds(since_ts, curr_ts, cursor=cursor)
        if resp["meta"] is None:
            logger.info("no meta in response, done!")
            break
        cursor = resp["meta"]["cursor"]
        logger.info(f"fetched {len(resp['data'])} records, next cursor: {cursor}")

        # get all the records
        records = resp.get("data", [])
        if len(records) == 0:
            break

        docs = [build_docs(record) for record in records]
        final_docs = [doc for sublist in docs for doc in sublist]

        # index the documents
        indexing_result = index(
            final_docs,
            record_manager,
            store,
            cleanup="incremental",
            source_id_key="id",
        )
        logger.info(f"Indexing result: {indexing_result}")


text_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
    is_separator_regex=False,
)


def build_docs(record):
    title = record["actions"][0]["metadata"]["title"]
    body = record["actions"][0]["metadata"]["body"]
    txt = f"<h1>{title}</h1>{body}"
    chunks = text_splitter.split_text(txt)
    return [
        Document(page_content=chunk, metadata={"id": record["id"], "full": record})
        for chunk in chunks
    ]


if __name__ == "__main__":
    _clear()
    build_index()
