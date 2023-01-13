import os

from report.report_generator import ReportGenerator

if __name__ == '__main__':
    if not os.environ.get("GITHUB_TOKEN"):
        raise PermissionError("GITHUB_TOKEN environment variable isn't set.")
    github_organization: str = 'padaiyal'
    report_generator = ReportGenerator('https://api.github.com', github_organization)

    report_generator.generate_report(
        'repositories_active',
        ["Name", "Latest version", "License", "Description", "Language", "Exposure", "Supported?", "Last Updated",
         "Open Issues"],
        True)

    report_generator.generate_report(
        'repositories_archived',
        ["Name", "Latest version", "License", "Description", "Language", "Exposure", "Supported?", "Last Updated",
         "Open Issues"],
        False)

    report_generator.generate_report(
        'repositories_documentation',
        ["Name", "Description", "Health %", "Content reports enabled", "Code of Conduct", "Contributing Guide",
         "Issue template", "Pull request template", 'License', "README", "Stars"],
        True)

    report_generator.generate_report(
        'repositories_health',
        ["Name", "Exposure", "Supported?", "Last Updated", "Health %", "Open Issues"],
        True)

    report_generator.generate_report(
        'repositories_activity',
        ["Name", "Latest version", "Last Updated"],
        True)

    report_generator.generate_report(
        'repositories_traction',
        ["Name", "Stars"],
        True)
