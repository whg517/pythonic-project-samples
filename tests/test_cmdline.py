import uvicorn
from alembic import config

import example_blog
from example_blog import cmdline


def test_main(cli):
    result = cli.invoke(cmdline.main)
    assert result.exit_code == 0
    result = cli.invoke(cmdline.main, '-V')
    assert result.exit_code == 0
    assert str(result.output).strip() == example_blog.__version__


def test_run(cli, mocker):
    mock_run = mocker.patch.object(uvicorn, 'run')
    result = cli.invoke(cmdline.main, ['server', '-h', '127.0.0.1', '-p', '8080'])
    assert result.exit_code == 0
    mock_run.assert_called_once_with(app=mocker.ANY, host='127.0.0.1', port=8080)


def test_migrate(cli, mocker):
    mock_main = mocker.patch.object(config, 'main')
    cli.invoke(cmdline.main, ['migrate', '--help'])
    mock_main.assert_called_once()
