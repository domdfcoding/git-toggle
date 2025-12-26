# 3rd party
from apeye_core import URL
from coincidence.regressions import AdvancedDataRegressionFixture
from domdf_python_tools.paths import PathPlus

# this package
from git_toggle import Remote, Toggler


def test_creation(temp_repo: PathPlus, advanced_data_regression: AdvancedDataRegressionFixture):
	toggler = Toggler(temp_repo)
	advanced_data_regression.check(toggler.list_remotes())


def test_get_current_remote(temp_repo: PathPlus):
	toggler = Toggler(temp_repo)

	assert toggler.get_current_remote() == "https://github.com/domdfcoding/git-toggle.git"
	assert toggler.get_current_remote("origin") == "https://github.com/domdfcoding/git-toggle.git"
	assert toggler.get_current_remote("repo-helper") == "https://github.com/domdfcoding/git-toggle.git"
	assert toggler.get_current_remote("upstream") == "git@github.com:repo-helper/git-toggler.git"

	# TODO: test get_current_remote with no remotes set


def test_get_current_remote_no_remotes(tmp_pathplus: PathPlus):
	toggler = Toggler.init(tmp_pathplus)
	assert toggler.get_current_remote() == ''


def test_set_current_remote(temp_repo: PathPlus):
	toggler = Toggler(temp_repo)

	toggler.set_current_remote("git@github.com:domdfcoding/git-toggle.git")
	assert toggler.get_current_remote() == "git@github.com:domdfcoding/git-toggle.git"

	toggler.set_current_remote("git@github.com:octocat/git-toggle.git", "origin")
	assert toggler.get_current_remote("origin") == "git@github.com:octocat/git-toggle.git"

	toggler.set_current_remote(URL("https://github.com/repo-helper/git-toggle.git"), "http")
	assert toggler.get_current_remote("http") == "https://github.com/repo-helper/git-toggle.git"

	toggler.set_current_remote(Remote.from_url("git@github.com:domdfcoding/git-toggle.git"))
	assert toggler.get_current_remote() == "git@github.com:domdfcoding/git-toggle.git"
