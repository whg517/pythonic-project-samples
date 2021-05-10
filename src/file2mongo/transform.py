"""Transform"""
import csv
from pathlib import Path
from typing import Any, Dict, Iterator

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from file2mongo.config import settings
from file2mongo.exceptions import NotConfigured


def read_file(path: Path) -> Iterator[Dict[str, Any]]:
    """
    Read file.
    :param path:
    :return:
    """
    with open(path, mode='r', encoding=settings.CHARACTERSET) as f_obj:
        reader = csv.DictReader(f_obj)
        for line in reader:
            yield line


def write_mongo(
        collection: Collection,
        data: Dict[str, Any], *args
) -> None:
    """
    :param collection:
    :param data:
    :param args: data-s
    :return:
    """
    docs = list(args)
    docs.append(data)
    collection.insert_many(docs)


def file_to_mongo():
    """Write csv file data to mongo"""
    uri = settings.MONGODB_URI
    if not uri:
        raise NotConfigured('MongoDB URI not configured.')
    client = MongoClient(uri)
    db_name = settings.MONGODB_DATABASE_NAME
    if not db_name:
        raise NotConfigured('MongoDB database name not configured.')
    database = Database(client, db_name)
    col_name = settings.MONGODB_COLLECTION_NAME
    if not col_name:
        raise NotConfigured('MongoDB collection name not configured.')
    collection = Collection(database, col_name)

    file_path = settings.FILE_PATH
    if not file_path:
        raise NotConfigured('File path not configured.')

    for line in read_file(Path(file_path)):
        write_mongo(collection, line)
