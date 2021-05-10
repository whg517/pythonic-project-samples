"""Test config"""
from tempfile import NamedTemporaryFile

import pytest
from click.testing import CliRunner


@pytest.fixture()
def clicker():
    """clicker fixture"""
    yield CliRunner()


@pytest.fixture()
def data_file():
    """data_file fixture"""
    data = """name,age,addr
xiaoming,20,beijing
hanmeimei,18,shanghai
"""
    with NamedTemporaryFile(suffix='.csv') as tmp_file:
        with open(tmp_file.name, mode='w', encoding='utf-8') as f_obj:
            f_obj.write(data)
        yield tmp_file.name
