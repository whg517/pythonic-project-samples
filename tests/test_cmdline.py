"""Test cmdline"""
from typing import List

import pytest
from click.testing import CliRunner

from file2mongo import __version__
from file2mongo.cmdline import main
from file2mongo.exceptions import BaseError


@pytest.mark.parametrize(
    ['invoke_args', 'exit_code', 'output_keyword'],
    [
        ([], 0, 'help'),
        (['--help'], 0, 'help'),
        (['--version'], 0, __version__),
        (['-V'], 0, __version__),
    ]
)
def test_main(
        clicker: CliRunner,
        invoke_args: List[str],
        exit_code: int,
        output_keyword: str,
):
    """Test main cmdline"""
    result = clicker.invoke(main, invoke_args)
    assert result.exit_code == exit_code
    assert output_keyword in result.output


def test_run(clicker: CliRunner, mocker):
    """Test cmd run"""
    mock_func = mocker.patch('file2mongo.cmdline.file_to_mongo')
    clicker.invoke(main, 'run')
    assert mock_func.called


def test_run_error(clicker: CliRunner, mocker):
    """Test cmd run error"""
    mock_func = mocker.patch(
        'file2mongo.cmdline.file_to_mongo',
        side_effect=BaseError('foo')
    )
    result = clicker.invoke(main, 'run')
    assert mock_func.called
    assert 'foo' in result.output
