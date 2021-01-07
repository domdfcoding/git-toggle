# 3rd party
import pytest
from apeye import URL

# this package
from git_toggle import Remote


def test_remote():

	remote = Remote(
			"https",
			domain="github.com",
			repo="git-toggle",
			username="domdfcoding",
			)

	assert remote.style == "https"
	assert remote.domain == "github.com"
	assert remote.repo == "git-toggle"
	assert remote.username == "domdfcoding"


def test_remote_from_url():
	remote = Remote.from_url("git@github.com:domdfcoding/git-toggle.git")
	assert remote.style == "ssh"
	assert remote.domain == "github.com"
	assert remote.repo == "git-toggle"
	assert remote.username == "domdfcoding"

	assert remote == Remote(
			"ssh",
			domain="github.com",
			repo="git-toggle",
			username="domdfcoding",
			)

	remote = Remote.from_url("https://github.com/domdfcoding/git-toggle.git")
	assert remote.style == "https"
	assert remote.domain == "github.com"
	assert remote.repo == "git-toggle"
	assert remote.username == "domdfcoding"

	assert remote == Remote(
			"https",
			domain="github.com",
			repo="git-toggle",
			username="domdfcoding",
			)

	with pytest.raises(ValueError, match=r"Unknown remote type for .*\."):
		Remote.from_url("ftp://github.com/domdfcoding/git-toggle")


def test_remote_as_url():
	remote = Remote.from_url(URL("git@github.com:domdfcoding/git-toggle.git"))
	assert remote.as_url() == URL("git@github.com:domdfcoding/git-toggle.git")


def test_remote_changing_properties():
	remote = Remote.from_url(URL("git@github.com:domdfcoding/git-toggle.git"))

	remote.username = "octocat"
	assert remote.as_url() == URL("git@github.com:octocat/git-toggle.git")

	remote.repo = "git-toggler"
	assert remote.as_url() == URL("git@github.com:octocat/git-toggler.git")

	remote.domain = "gitlab.com"
	assert remote.as_url() == URL("git@gitlab.com:octocat/git-toggler.git")

	remote.style = "https"
	assert remote.as_url() == URL("https://gitlab.com/octocat/git-toggler.git")

	remote.set_username(None)
	assert remote.as_url() == URL("https://gitlab.com/octocat/git-toggler.git")

	remote.set_username("domdfcoding")
	assert remote.as_url() == URL("https://gitlab.com/domdfcoding/git-toggler.git")

	remote.set_repo(None)
	assert remote.as_url() == URL("https://gitlab.com/domdfcoding/git-toggler.git")

	remote.set_repo("git-toggle")
	assert remote.as_url() == URL("https://gitlab.com/domdfcoding/git-toggle.git")
