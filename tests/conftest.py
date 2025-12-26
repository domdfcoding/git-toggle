# 3rd party
import pytest
from domdf_python_tools.paths import PathPlus
from dulwich.repo import Repo

pytest_plugins = ("coincidence", )


@pytest.fixture()
def temp_repo(tmp_pathplus: PathPlus) -> PathPlus:
	repo: Repo = Repo.init(tmp_pathplus)
	config = repo.get_config()
	config.set(("remote", "origin"), "url", b"https://github.com/domdfcoding/git-toggle.git")
	config.set(("remote", "upstream"), "url", b"git@github.com:repo-helper/git-toggler.git")
	config.write_to_path()

	return tmp_pathplus
