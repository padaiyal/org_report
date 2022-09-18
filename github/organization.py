import json
import os
import requests

from github.repository import GitHubRepository


class GitHubOrganization:
    def __init__(self, server: str, name: str) -> None:
        self.organization = name
        self.server = server

    def get_repositories(self) -> tuple:
        request = requests.get(
            f'{self.server}/orgs/{self.organization}/repos',
            headers={'Authorization': f'token {os.environ.get("GITHUB_TOKEN")}'}
        )
        repositories_json: list = json.loads(request.content)

        return tuple(
            GitHubRepository(
                server=self.server,
                organization_name=self.organization,
                name=repository_json['name'],
                additional_info=repository_json
            ) for repository_json in repositories_json
        )
