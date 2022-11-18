# Source: https://github.com/thoth-station/mi/blob/master/srcopsmetrics/github_handling.py
#!/usr/bin/env python3
# Meta-information Indicators
# Copyright(C) 2021 Dominik Tuchyna
#
# This program is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Module that contains handling decorator for GitHub API Rate limit."""

import logging
import os
import time
from datetime import datetime, timezone
from typing import Optional
from dotenv import find_dotenv, load_dotenv

from github import Github
from github.Repository import Repository

load_dotenv(find_dotenv(), override=True)

_LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

_GITHUB_ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")

API_RATE_MINIMAL_REMAINING = 20
GITHUB_TIMEOUT_SECONDS = 60


class GitHubSingleton(object):
    """Singleton class for GitHub object."""

    _instance = None

    def __new__(cls):
        """One-time initialize GH object if there is none."""
        if not cls._instance:
            _LOGGER.debug("Initializing singleton GitHub wrapper object")
            cls._instance = super(GitHubSingleton, cls).__new__(cls)
            cls.github = Github(login_or_token=_GITHUB_ACCESS_TOKEN, timeout=GITHUB_TIMEOUT_SECONDS)

        return cls._instance

class GithubHandler:
    """Handler class that contains GH API rate handling logic."""

    def __init__(self, github: Optional[Github] = None):
        """Initialize with github object."""
        if not github:
            github = Github(login_or_token=_GITHUB_ACCESS_TOKEN, timeout=GITHUB_TIMEOUT_SECONDS)

        self.github = github
        self.remaining = github.get_rate_limit().core.remaining
        _LOGGER.info(" Github Handler __init__: %d remaining api calls" % (self.remaining))

    def _is_api_exhausted(self):
        """Check if GH API rate limit is exhausted."""
        self.remaining = self.github.get_rate_limit().core.remaining
        _LOGGER.info(" _is_api_exhausted: %d remaining api calls" % (self.remaining))
        return self.remaining <= API_RATE_MINIMAL_REMAINING

    def _wait_until_api_reset(self):
        """Wait until the GitHub API rate limit is reset."""
        gh_time = self.github.get_rate_limit().core.reset
        local_time = datetime.now(tz=timezone.utc)

        wait_time = (gh_time - local_time.replace(tzinfo=None)).seconds
        wait_time += 60

        _LOGGER.info("API rate limit REACHED, will now wait for %d minutes" % (wait_time // 60))
        time.sleep(wait_time)

    def check_and_wait_for_api(self):
        """Check if GH is exhausted, if so then wait until it is regained."""
        if self._is_api_exhausted():
            self._wait_until_api_reset()

def github_handler(original_function):
    """Check the GitHub API rate limit and call the original function."""
    # Use it as a @github_handler decorator

    def _wrapper(*args, **kwargs):
        # Check if github_handler is passed
        handler = None
        if args[-1]:
            handler = args[-1]
        else:
            handler = GithubHandler()
        handler.check_and_wait_for_api()
        return original_function(*args, **kwargs)

    return _wrapper

@github_handler
def get_github_object(github_handler=None) -> Github:
    """Connect to GH and return its wrapper object."""
    if github_handler:
        return github_handler.github
    return GitHubSingleton().github

@github_handler
def connect_to_source(repository_name: str, github_handler=None) -> Repository:
    """Connect to GitHub and return repository object.

    :param project: Tuple source repo and repo name.
    """
    if github_handler:
        return get_github_object(github_handler).get_repo(repository_name)
    return get_github_object().get_repo(repository_name)


