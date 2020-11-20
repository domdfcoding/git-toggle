#!/usr/bin/env python3
#
#  __main__.py
"""
Toggle Git remotes between https and ssh.
"""
#
#  Copyright © 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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
import argparse
import re
import sys
from typing import List, Optional

# 3rd party
from apeye.url import URL
from domdf_python_tools.utils import stderr_writer
from dulwich.errors import NotGitRepository  # type: ignore
from dulwich.repo import Repo  # type: ignore

__all__ = ["main"]


def main(argv: Optional[List[str]] = None) -> int:

	parser = argparse.ArgumentParser(description="Toggle Git remotes between https and ssh.")
	parser.add_argument("--list", help="List the current remotes and exit..", action="store_true")

	parser.add_argument(
			"what",
			help="Switch the remote type to what? 'http' is an alias of 'https'.",
			type=str,
			choices=["http", "https", "ssh", ''],
			metavar="{http,https,ssh}",
			nargs='?',
			default='',
			)
	parser.add_argument("--username", help="Set the remote username.")
	parser.add_argument("--repo", help="Set the remote repository name.")
	parser.add_argument(
			"--name",
			help="Apply the settings to the remote with the given name. Default '%(default)s'.",
			default="origin",
			)

	args = parser.parse_args(argv)

	try:
		config = Repo('.').get_config()
	except NotGitRepository:
		parser.error("The current directory is not a git repository.")

	if args.list:
		remotes = []
		for key in list(config.keys()):
			if key[0] == b"remote":
				remotes.append((key[1].decode("UTF-8"), config.get(key, "url").decode("UTF-8")))

		if not remotes:
			stderr_writer("No remotes set!")
			return 1

		longest_name = max(len(x[0]) for x in remotes)

		for entry in remotes:
			print(f"{entry[0]}{' ' * (longest_name - len(entry[0]))}  {entry[1]}")

		return 0

	try:
		current_remote = config.get(("remote", args.name), "url").decode("UTF-8")
	except KeyError:
		try:
			current_remote = config.get(("remote", "origin"), "url").decode("UTF-8")
		except KeyError:
			current_remote = ''

	if re.match(r"^\s*http(s)?://", current_remote):
		current_type = "https"
		url = URL(current_remote)
		domain = url.fqdn
		repo = url.path.stem
		username = str(url.path.parent)[1:]

	elif re.match(r"^\s*git@", current_remote):
		current_type = "git"
		url = URL(current_remote)
		domain = url.fqdn
		repo = url.path.stem
		username = str(url.netloc)[(len(domain) + 5):]

	else:
		stderr_writer(f"Unknown remote type {current_remote}.")
		return 1

	if args.username:
		username = args.username
	if args.repo:
		repo = args.repo

	def set_http():
		config.set(("remote", args.name), "url", f"https://{domain}/{username}/{repo}.git".encode("UTF-8"))

	def set_ssh():
		config.set(("remote", args.name), "url", f"git@{domain}:{username}/{repo}.git".encode("UTF-8"))

	if args.what.startswith("http"):
		set_http()
	elif args.what.startswith("ssh"):
		set_ssh()
	else:
		if current_type == "https":
			set_http()
		elif current_type == "git":
			set_ssh()

	config.write_to_path()

	return 0


if __name__ == "__main__":
	sys.exit(main(sys.argv[1:]))
