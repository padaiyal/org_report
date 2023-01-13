from datetime import datetime

from mdutils import MdUtils
from typing import List

from github.organization import GitHubOrganization


class ReportGenerator:
    def __init__(self, github_instance: str, github_organization: str) -> None:
        self.github_instance: str = github_instance
        self.github_organization: GitHubOrganization = GitHubOrganization(
            server=github_instance,
            name=github_organization
        )
        self.repositories: tuple = self.github_organization.get_repositories()

    # noinspection PyMethodMayBeStatic
    def get_boolean_representation(self, value) -> str:
        if value == '🤷‍':
            return value
        if value == 'None' or not bool(value):
            return '❌'
        return '✅'

    # flake8: noqa: C901
    def generate_report(self, name: str, table_headers: List[str], skip_archived: bool) -> None:
        table: List[str] = list(table_headers)
        row_count: int = 0
        for repository in self.repositories:
            community_profile: dict = repository.get_repository_community_profile()
            latest_release_info: dict = repository.get_repository_latest_version()
            latest_release: str = f"[{latest_release_info.get('name', '🤷‍')}]({latest_release_info.get('html_url')})"
            repository_additional_info: dict = repository.additional_info
            is_archived: bool = bool(repository_additional_info['archived'])
            if skip_archived and is_archived:
                continue

            def get_field(field: str) -> str:
                if field == 'Name':
                    return f"[{repository_additional_info['full_name']}]({repository_additional_info['html_url']})"
                elif field == 'Latest version':
                    return latest_release
                elif field == 'Language':
                    return repository_additional_info['language']
                elif field == 'Exposure':
                    return '🔒' if bool(repository_additional_info['private']) else '🌏'
                elif field == 'Supported?':
                    return self.get_boolean_representation(not is_archived)
                elif field == 'Last Updated':
                    return repository_additional_info['updated_at']
                elif field == 'Open Issues':
                    return f"[{repository_additional_info['open_issues_count']}]" \
                           f"({repository_additional_info['html_url']}/issues)"
                elif field == 'License':
                    return (repository_additional_info['license']['name'] if repository_additional_info['license']
                            else '🤷‍')
                elif field == 'Health %':
                    return community_profile['health_percentage']
                elif field == 'Description':
                    return community_profile['description']
                elif field == 'Content reports enabled':
                    return self.get_boolean_representation(community_profile.get('content_reports_enabled', '🤷‍'))
                elif field == 'Code of Conduct':
                    return self.get_boolean_representation(community_profile['files']['code_of_conduct'])
                elif field == 'Contributing Guide':
                    return self.get_boolean_representation(community_profile['files']['contributing'])
                elif field == 'Issue template':
                    return self.get_boolean_representation(community_profile['files']['issue_template'])
                elif field == 'Pull request template':
                    return self.get_boolean_representation(community_profile['files']['pull_request_template'])
                elif field == 'README':
                    return self.get_boolean_representation(community_profile['files']['readme'])
                elif field == 'Stars':
                    return repository_additional_info['stargazers_count']
                else:
                    raise ValueError(f'Unknown field - {field}')

            row: List[str] = [get_field(field) for field in table_headers]
            table.extend(row)
            row_count += 1

        now: str = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
        md_file: MdUtils = MdUtils(file_name=name,
                                   title=f'{self.github_organization.name} - {name} report - {now}')
        md_file.new_line()
        md_file.new_table(columns=len(table_headers), rows=row_count + 1, text=table, text_align='center')
        md_file.create_md_file()
