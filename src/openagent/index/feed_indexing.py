import datetime

from dotenv import load_dotenv
from langchain.indexes import SQLRecordManager
from langchain_core.documents import Document
from langchain_core.indexing import index
from langchain_text_splitters import CharacterTextSplitter
from loguru import logger

from openagent.conf.env import settings
from openagent.index.feed_scrape import fetch_iqwiki_feeds, fetch_mirror_feeds
from openagent.index.pgvector_store import build_vector_store

load_dotenv()

record_manager = SQLRecordManager("backend", db_url=settings.DB_CONNECTION)
record_manager.create_schema()


def _clear():
    index([], record_manager, build_vector_store(), cleanup="incremental", source_id_key="id")


def build_index():
    indexing_iqwiki()
    indexing_mirror()


def indexing_iqwiki():
    index_feed(fetch_iqwiki_feeds, "iqwiki")


def indexing_mirror():
    index_feed(fetch_mirror_feeds, "mirror")


def index_feed(fetch_function, feed_name):
    since_date = datetime.datetime.now() - datetime.timedelta(days=180)
    curr_date = datetime.datetime.now()
    since_ts = int(since_date.timestamp())
    curr_ts = int(curr_date.timestamp())

    cursor = None
    logger.info(
        f"Starting to index feed '{feed_name}' from " f"{since_date.strftime('%Y-%m-%d %H:%M:%S')} to" f" {curr_date.strftime('%Y-%m-%d %H:%M:%S')}"
    )
    while True:
        resp = fetch_function(since_ts, curr_ts, cursor=cursor)
        if resp["meta"] is None:
            logger.info(f"no meta in response, done with {feed_name}!")
            break
        cursor = resp["meta"]["cursor"]
        logger.info(f"fetched {len(resp['data'])} records from {feed_name}," f" next cursor: {cursor}")

        records = resp.get("data", [])
        if len(records) == 0:
            break

        save_records(records)


def save_records(records):
    docs = [build_docs(record) for record in records]
    final_docs = [doc for sublist in docs for doc in sublist]
    # index the documents
    indexing_result = index(
        final_docs,
        record_manager,
        build_vector_store(),
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
    return [Document(page_content=chunk, metadata={"id": record["id"], "full": record}) for chunk in chunks]


if __name__ == "__main__":
    _clear()
    build_index()
