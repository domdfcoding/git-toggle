# 3rd party
from apeye_core import URL

# this package
from git_toggle import Remote, Toggler


def test_creation(temp_repo, data_regression):
	toggler = Toggler(temp_repo)
	data_regression.check(toggler.list_remotes())


def test_get_current_remote(temp_repo):
	toggler = Toggler(temp_repo)

	assert toggler.get_current_remote() == "https://github.com/domdfcoding/git-toggle.git"
	assert toggler.get_current_remote("origin") == "https://github.com/domdfcoding/git-toggle.git"
	assert toggler.get_current_remote("repo-helper") == "https://github.com/domdfcoding/git-toggle.git"
	assert toggler.get_current_remote("upstream") == "git@github.com:repo-helper/git-toggler.git"

	# TODO: test get_current_remote with no remotes set


def test_get_current_remote_no_remotes(tmp_pathplus):
	toggler = Toggler.init(tmp_pathplus)
	assert toggler.get_current_remote() == ''


def test_set_current_remote(temp_repo):
	toggler = Toggler(temp_repo)

	toggler.set_current_remote("git@github.com:domdfcoding/git-toggle.git")
	assert toggler.get_current_remote() == "git@github.com:domdfcoding/git-toggle.git"

	toggler.set_current_remote("git@github.com:octocat/git-toggle.git", "origin")
	assert toggler.get_current_remote("origin") == "git@github.com:octocat/git-toggle.git"

	toggler.set_current_remote(URL("https://github.com/repo-helper/git-toggle.git"), "http")
	assert toggler.get_current_remote("http") == "https://github.com/repo-helper/git-toggle.git"

	toggler.set_current_remote(Remote.from_url("git@github.com:domdfcoding/git-toggle.git"))
	assert toggler.get_current_remote() == "git@github.com:domdfcoding/git-toggle.git"
