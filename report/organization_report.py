import datetime

from mdutils import MdUtils
from typing import List

from github.organization import GitHubOrganization
from report.report import Report


class OrganizationReadMeReport(Report):

    def __init__(self, name: str, github_instance: str, github_organization: str, skip_archived: bool) -> None:
        super().__init__(name, skip_archived)
        self.github_instance: str = github_instance
        self.github_organization: GitHubOrganization = GitHubOrganization(
            server=github_instance,
            name=github_organization
        )

    def generate_report(self) -> None:
        repositories: tuple = self.github_organization.get_repositories()
        table_headers: List[str] = ["Name", "Latest version", "Language", "Exposure", "Supported?", "Last Updated",
                                    "Open Issues", "License",
                                    "Health %", "Description", "Content reports enabled?", "Code of Conduct?",
                                    "Contributing Guide?", "Issue template?", "Pull request template?", "README?",
                                    "Stars"]
        table: List[str] = list(table_headers)
        row_count: int = 0
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
            is_archived: bool = bool(repository_additional_info['archived'])
            if self.skip_archived and is_archived:
                continue
            table.extend(
                [
                    f"[{repository_additional_info['full_name']}]({repository_additional_info['html_url']})",
                    latest_release,
                    repository_additional_info['language'],
                    '🔒' if bool(repository_additional_info['private']) else '🌏',
                    self.get_boolean_representation(not is_archived),
                    repository_additional_info['updated_at'],
                    f"[{repository_additional_info['open_issues_count']}]"
                    f"({repository_additional_info['html_url']}/issues)",
                    repository_additional_info['license']['name'] if repository_additional_info[
                        'license'] else '🤷‍',
                    community_profile['health_percentage'],
                    community_profile['description'],
                    self.get_boolean_representation(community_profile.get('content_reports_enabled', '🤷‍')),
                    self.get_boolean_representation(community_profile_files['code_of_conduct']),
                    self.get_boolean_representation(community_profile_files['contributing']),
                    self.get_boolean_representation(community_profile_files['issue_template']),
                    self.get_boolean_representation(community_profile_files['pull_request_template']),
                    self.get_boolean_representation(community_profile_files['readme']),
                    repository_additional_info['stargazers_count']
                ]
            )
            row_count += 1

        now: str = datetime.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
        md_file: MdUtils = MdUtils(file_name=self.name,
                                   title=f'{self.github_organization.name} report - {now}')
        md_file.new_line()
        md_file.new_table(columns=len(table_headers), rows=row_count + 1, text=table, text_align='center')
        md_file.create_md_file()
