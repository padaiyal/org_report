import json
import os
import requests


class GitHubRepository:

    def __init__(self, server: str, organization_name: str, name: str, additional_info: dict = dict()) -> None:
        self.server = server
        self.organization = organization_name
        self.repository = name
        self.additional_info = additional_info

    def get_repository_community_profile(self) -> dict:
        request = requests.get(
            f'{self.server}/repos/{self.organization}/{self.repository}/community/profile',
            headers={'Authorization': f'token {os.environ.get("GITHUB_TOKEN")}'}
        )
        community_profile: dict = json.loads(request.content)
        return community_profile

    def get_repository_latest_version(self) -> dict:
        request = requests.get(
            f'{self.server}/repos/{self.organization}/{self.repository}/releases/latest',
            headers={'Authorization': f'token {os.environ.get("GITHUB_TOKEN")}'}
        )
        latest_version: dict = json.loads(request.content)
        return latest_version
