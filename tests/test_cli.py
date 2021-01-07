# stdlib
import tempfile

# 3rd party
import click
import pytest
from click.testing import CliRunner, Result
from domdf_python_tools.paths import in_directory
from domdf_python_tools.testing import check_file_regression
from dulwich.repo import Repo
from pytest_regressions.file_regression import FileRegressionFixture

# this package
from git_toggle import Toggler
from git_toggle.__main__ import get_repo_or_raise, main


def test_get_repo_or_raise(temp_repo):

	with tempfile.TemporaryDirectory() as tmpdir:
		with in_directory(tmpdir):
			with pytest.raises(click.UsageError, match=r"The current directory is not a git repository\."):
				get_repo_or_raise()

	with in_directory(temp_repo):
		assert isinstance(get_repo_or_raise(), Repo)


def test_list_remotes(temp_repo, file_regression: FileRegressionFixture):
	with in_directory(temp_repo):
		runner = CliRunner()

		result: Result = runner.invoke(main, catch_exceptions=False, args="--list")
		assert result.exit_code == 0
		check_file_regression(result.stdout, file_regression)


def test_list_remotes_no_remotes(tmp_pathplus):
	Repo.init(tmp_pathplus)

	with in_directory(tmp_pathplus):
		runner = CliRunner()

		result: Result = runner.invoke(main, catch_exceptions=False, args="--list")
		assert result.exit_code == 1
		assert result.stdout == "No remotes set!\nAborted!\n"


def test_toggle(temp_repo):
	toggler = Toggler(temp_repo)

	with in_directory(temp_repo):
		runner = CliRunner()

		result: Result = runner.invoke(main, catch_exceptions=False)
		assert result.exit_code == 0
		assert toggler.get_current_remote() == "https://github.com/domdfcoding/git-toggle.git"
		assert toggler.get_current_remote("upstream") == "git@github.com:repo-helper/git-toggler.git"

		result = runner.invoke(main, catch_exceptions=False, args="ssh")
		assert result.exit_code == 0
		assert toggler.get_current_remote() == "git@github.com:domdfcoding/git-toggle.git"
		assert toggler.get_current_remote("upstream") == "git@github.com:repo-helper/git-toggler.git"

		result = runner.invoke(main, catch_exceptions=False, args="http")
		assert result.exit_code == 0
		assert toggler.get_current_remote() == "https://github.com/domdfcoding/git-toggle.git"
		assert toggler.get_current_remote("upstream") == "git@github.com:repo-helper/git-toggler.git"

		result = runner.invoke(main, catch_exceptions=False, args=["https", "--name", "upstream"])
		assert result.exit_code == 0
		assert toggler.get_current_remote() == "https://github.com/domdfcoding/git-toggle.git"
		assert toggler.get_current_remote("upstream") == "https://github.com/repo-helper/git-toggler.git"


def test_toggle_errors(temp_repo):
	with in_directory(temp_repo):
		runner = CliRunner()

		result: Result = runner.invoke(main, catch_exceptions=False, args="ftp")
		assert result.exit_code == 2
		error = "Error: Invalid value for '[[http|https|ssh]]': invalid choice: ftp. (choose from http, https, ssh, )"
		assert result.stdout.splitlines()[-1] == error


def test_help(file_regression: FileRegressionFixture):
	runner = CliRunner()

	result: Result = runner.invoke(main, catch_exceptions=False, args="-h")
	assert result.exit_code == 0
	check_file_regression(result.stdout.rstrip(), file_regression)

	result = runner.invoke(main, catch_exceptions=False, args="--help")
	assert result.exit_code == 0
	check_file_regression(result.stdout.rstrip(), file_regression)
