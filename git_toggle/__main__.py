#!/usr/bin/env python3
#
#  __main__.py
"""
Toggle Git remotes between https and ssh.
"""
#
#  Copyright © 2020-2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
import sys
from typing import Optional

# 3rd party
import click
from consolekit import click_command
from consolekit.options import auto_default_option, flag_option
from consolekit.utils import abort
from dulwich.errors import NotGitRepository

# this package
from git_toggle import Remote, Toggler

__all__ = ["main", "get_repo_or_raise"]

# Fix intersphinx links
click.UsageError.__module__ = "click"


def get_repo_or_raise() -> Toggler:
	"""
	Return a :class:`~.Toggler` instance for the repository in the current working directory,
	or raise :exc:`click.UsageError` if the current directory is not a git repository.
	"""  # noqa: D400

	try:
		toggler = Toggler('.')
	except NotGitRepository:
		raise click.UsageError("The current directory is not a git repository.")

	return toggler


def list_remotes_callback(ctx: click.Context, param: click.Option, value: int):
	"""
	Callback fore the ``--list`` option.

	:param ctx:
	:param param:
	:param value:
	"""

	if not value or ctx.resilient_parsing:
		return

	toggler = get_repo_or_raise()
	remotes = toggler.list_remotes()

	if not remotes:
		raise abort("No remotes set!")

	longest_name = max(len(x) for x in remotes)

	for entry in remotes.items():
		click.echo(f"{entry[0]}{' ' * (longest_name - len(entry[0]))}  {entry[1]}")

	ctx.exit()


@flag_option(
		"--list",
		"list_remotes",
		help="List the current remotes and exit.",
		callback=list_remotes_callback,
		expose_value=False,
		is_eager=True,
		)
@auto_default_option("--repo", help="Set the remote repository name.")
@auto_default_option("--username", help="Set the remote username.")
@auto_default_option(
		"--name",
		help="Apply the settings to the remote with the given name.",
		show_default=True,
		)
@click.argument(
		"what",
		# help="Switch the remote type to what? 'http' is an alias of 'https'.",
		type=click.Choice(["http", "https", "ssh", ''], case_sensitive=False),
		metavar="[[http|https|ssh]]",
		default='',
		)
@click_command()
def main(
		what: str,
		name: str = "origin",
		username: Optional[str] = None,
		repo: Optional[str] = None,
		):
	"""
	Toggle Git remotes between https and ssh.
	"""

	toggler = get_repo_or_raise()

	try:
		current_remote = Remote.from_url(toggler.get_current_remote(name))
	except ValueError as e:
		raise abort(str(e))

	current_remote.set_username(username)
	current_remote.set_repo(repo)

	if what.startswith("http"):
		current_remote.style = "https"
	elif what.startswith("ssh"):
		current_remote.style = "ssh"

	toggler.set_current_remote(current_remote, name)

	return 0


if __name__ == "__main__":
	sys.exit(main())
