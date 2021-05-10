"""Test transform"""
from pathlib import Path

import pytest
from pymongo.collection import Collection

from file2mongo.config import settings
from file2mongo.exceptions import NotConfigured
from file2mongo.transform import file_to_mongo, read_file, write_mongo


def test_read_file(data_file):
    """Test read file"""
    res = list(read_file(Path(data_file)))
    assert len(res) == 2
    assert isinstance(res[0], dict)


def test_write_mongo(mocker):
    """Test write data to mongo"""
    mock_col = mocker.MagicMock(spce=Collection)
    write_mongo(mock_col, data={})
    assert mock_col.insert_many.called_once_with({})


@pytest.mark.parametrize(
    ['update_settings', 'error', 'msg'],
    [
        (
                {},
                NotConfigured,
                'MongoDB URI',
        ),
        (
                {
                    'mongodb_uri': 'mongodb://localhost:27017',
                },
                NotConfigured,
                'MongoDB database',

        ),
        (
                {
                    'mongodb_uri': 'mongodb://localhost:27017',
                    'mongodb_database_name': 'foo',
                },
                NotConfigured,
                'MongoDB collection',
        ),
        (
                {
                    'mongodb_uri': 'mongodb://localhost:27017',
                    'mongodb_database_name': 'foo',
                    'mongodb_collection_name': 'foo',
                },
                NotConfigured,
                'File path',
        ),
        (
                {
                    'mongodb_uri': 'mongodb://localhost:27017',
                    'mongodb_database_name': 'foo',
                    'mongodb_collection_name': 'foo',
                    'file_path': 'foo',
                },
                None,
                None,
        ),
    ]
)
def test_file_to_mongo(update_settings, error, msg, data_file, mocker):
    """Test write csv data to mongo"""
    mocker.patch.object(Collection, 'insert_many')
    if update_settings.get('file_path'):
        update_settings.update({'file_path': data_file})

    settings.update(update_settings)

    if error:
        with pytest.raises(error, match=msg):
            file_to_mongo()
    else:
        file_to_mongo()
