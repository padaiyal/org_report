import datetime
import json
import os

import requests
from mdutils import MdUtils
from typing import List

ORGANIZATION = 'padaiyal'
GITHUB_INSTANCE = 'https://api.github.com'
GITHUB_ACCESS_TOKEN = os.environ.get("GITHUB_TOKEN")


def get_repositories() -> list:
    request = requests.get(
        f'{GITHUB_INSTANCE}/orgs/{ORGANIZATION}/repos',
        headers={'Authorization': f'token {GITHUB_ACCESS_TOKEN}'}
    )
    repositories: list = json.loads(request.content)
    return repositories


def get_organization_report_name() -> str:
    return "README"


def get_repository_community_profile(repository_name: str) -> dict:
    request = requests.get(
        f'{GITHUB_INSTANCE}/repos/{ORGANIZATION}/{repository_name}/community/profile',
        headers={'Authorization': f'token {GITHUB_ACCESS_TOKEN}'}
    )
    community_profile: dict = json.loads(request.content)
    return community_profile


def get_repository_latest_version(repository_name: str) -> dict:
    request = requests.get(
        f'{GITHUB_INSTANCE}/repos/{ORGANIZATION}/{repository_name}/releases/latest',
        headers={'Authorization': f'token {GITHUB_ACCESS_TOKEN}'}
    )
    latest_version: dict = json.loads(request.content)
    return latest_version


def get_boolean_representation(value) -> str:
    if value == '🤷‍':
        return value
    if value == 'None' or not bool(value):
        return '❌'
    return '✅'


def generate_organization_report() -> None:
    repositories: list = get_repositories()
    organization_report_name: str = get_organization_report_name()
    table_headers: List[str] = ["Name", "Latest version", "Language", "Exposure", "Supported?", "Last Updated",
                                "Open Issues", "License",
                                "Health %", "Description", "Content reports enabled?", "Code of Conduct?",
                                "Contributing Guide?", "Issue template?", "Pull request template?", "README?", "Stars"]
    table: List[str] = list(table_headers)
    for repository in repositories:
        print(repository['name'])
        repository
        community_profile: dict = get_repository_community_profile(repository['name'])
        community_profile['health_percentage'] = str(community_profile.get('health_percentage', '‍🤷'))
        community_profile['health_percentage'] += '%' if community_profile['health_percentage'] != '‍🤷' else ''
        community_profile['description'] = str(community_profile.get('description', '‍🤷'))
        community_profile_files: dict = community_profile.get(
            'files',
            {
                'code_of_conduct': '‍🤷',
                'contributing': '🤷‍',
                'issue_template': '🤷‍',
                'pull_request_template': '🤷‍',
                'readme': '🤷‍'
            }
        )
        latest_release_info: dict = get_repository_latest_version(repository['name'])
        latest_release: str = f"[{latest_release_info.get('name', '🤷‍')}]({latest_release_info.get('html_url')})"
        table.extend(
            [
                f"[{repository['full_name']}]({repository['html_url']})",
                latest_release,
                repository['language'],
                '🔒' if bool(repository['private']) else '🌏',
                get_boolean_representation(not bool(repository['archived'])),
                repository['updated_at'],
                f"[{repository['open_issues_count']}]({repository['html_url']}/issues)",
                repository['license']['name'] if repository['license'] else '🤷‍',
                community_profile['health_percentage'],
                community_profile['description'],
                get_boolean_representation(community_profile.get('content_reports_enabled', '🤷‍')),
                get_boolean_representation(community_profile_files['code_of_conduct']),
                get_boolean_representation(community_profile_files['contributing']),
                get_boolean_representation(community_profile_files['issue_template']),
                get_boolean_representation(community_profile_files['pull_request_template']),
                get_boolean_representation(community_profile_files['readme']),
                repository['stargazers_count']
            ]
        )

    now: str = datetime.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
    md_file: MdUtils = MdUtils(file_name=organization_report_name,
                               title=f'{ORGANIZATION} report - {now}')
    md_file.new_line()
    md_file.new_table(columns=len(table_headers), rows=len(repositories) + 1, text=table, text_align='center')
    md_file.create_md_file()


def generate_repository_documentation_report() -> None:
    pass


def generate_repository_health_report() -> None:
    pass


if __name__ == '__main__':
    if not GITHUB_ACCESS_TOKEN:
        raise PermissionError("GITHUB_TOKEN environment variable isn't set.")
    generate_organization_report()
