import os

from report.organization_report import OrganizationReadMeReport

if __name__ == '__main__':
    if not os.environ.get("GITHUB_TOKEN"):
        raise PermissionError("GITHUB_TOKEN environment variable isn't set.")
    github_organization: str = 'padaiyal'
    OrganizationReadMeReport('README', 'https://api.github.com', github_organization).generate_report()
