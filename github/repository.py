import json
import os
import requests


class GitHubRepository:

    def __init__(self, server: str, organization_name: str, name: str, additional_info=None) -> None:
        if additional_info is None:
            additional_info = dict()
        self.server = server
        self.organization = organization_name
        self.name = name
        self.additional_info = additional_info
        self.community_profile = None

    def get_repository_community_profile(self) -> dict:
        if not self.community_profile:
            request = requests.get(
                f'{self.server}/repos/{self.organization}/{self.name}/community/profile',
                headers={'Authorization': f'token {os.environ.get("GITHUB_TOKEN")}'}
            )
            self.community_profile: dict = json.loads(request.content)
            self.community_profile['health_percentage'] = str(self.community_profile.get('health_percentage', '‍🤷'))
            self.community_profile['health_percentage'] += ('%' if self.community_profile['health_percentage'] != '‍🤷'
                                                            else '')
            self.community_profile['description'] = str(self.community_profile.get('description', '‍🤷'))
            self.community_profile['files'] = self.community_profile.get(
                'files',
                {
                    'code_of_conduct': '‍🤷',
                    'contributing': '🤷‍',
                    'issue_template': '🤷‍',
                    'pull_request_template': '🤷‍',
                    'readme': '🤷‍'
                }
            )
        return self.community_profile

    def get_repository_latest_version(self) -> dict:
        request = requests.get(
            f'{self.server}/repos/{self.organization}/{self.name}/releases/latest',
            headers={'Authorization': f'token {os.environ.get("GITHUB_TOKEN")}'}
        )
        latest_version: dict = json.loads(request.content)
        return latest_version
