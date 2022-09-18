import datetime
import os

from mdutils import MdUtils
from typing import List

from github.organization import GitHubOrganization

ORGANIZATION = 'padaiyal'
GITHUB_INSTANCE = 'https://api.github.com'
GITHUB_ACCESS_TOKEN = os.environ.get("GITHUB_TOKEN")

github_organization = GitHubOrganization(
    server='https://api.github.com',
    name='padaiyal'
)


def get_organization_report_name() -> str:
    return "README"


def get_boolean_representation(value) -> str:
    if value == '🤷‍':
        return value
    if value == 'None' or not bool(value):
        return '❌'
    return '✅'


def generate_organization_report() -> None:
    repositories: tuple = github_organization.get_repositories()
    organization_report_name: str = get_organization_report_name()
    table_headers: List[str] = ["Name", "Latest version", "Language", "Exposure", "Supported?", "Last Updated",
                                "Open Issues", "License",
                                "Health %", "Description", "Content reports enabled?", "Code of Conduct?",
                                "Contributing Guide?", "Issue template?", "Pull request template?", "README?", "Stars"]
    table: List[str] = list(table_headers)
    for repository in repositories:
        print(repository.name)
        community_profile: dict = repository.get_repository_community_profile()
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
        latest_release_info: dict = repository.get_repository_latest_version()
        latest_release: str = f"[{latest_release_info.get('name', '🤷‍')}]({latest_release_info.get('html_url')})"
        repository_additional_info: dict = repository.additional_info
        table.extend(
            [
                f"[{repository_additional_info['full_name']}]({repository_additional_info['html_url']})",
                latest_release,
                repository_additional_info['language'],
                '🔒' if bool(repository_additional_info['private']) else '🌏',
                get_boolean_representation(not bool(repository_additional_info['archived'])),
                repository_additional_info['updated_at'],
                f"[{repository_additional_info['open_issues_count']}]({repository_additional_info['html_url']}/issues)",
                repository_additional_info['license']['name'] if repository_additional_info['license'] else '🤷‍',
                community_profile['health_percentage'],
                community_profile['description'],
                get_boolean_representation(community_profile.get('content_reports_enabled', '🤷‍')),
                get_boolean_representation(community_profile_files['code_of_conduct']),
                get_boolean_representation(community_profile_files['contributing']),
                get_boolean_representation(community_profile_files['issue_template']),
                get_boolean_representation(community_profile_files['pull_request_template']),
                get_boolean_representation(community_profile_files['readme']),
                repository_additional_info['stargazers_count']
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
