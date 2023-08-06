# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['watson_jira_next', 'watson_jira_next.src', 'watson_jira_next.tests']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'click>=8.1.3,<9.0.0',
 'colorama>=0.4.4,<0.5.0',
 'jira>=3.2.0,<4.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'pyxdg>=0.28,<0.29',
 'simplejson>=3.17.6,<4.0.0',
 'td-watson>=2.1.0,<3.0.0']

entry_points = \
{'console_scripts': ['watson-jira-next = watson_jira_next.cli:main']}

setup_kwargs = {
    'name': 'watson-jira-next',
    'version': '0.3.3',
    'description': 'Format and upload Watson time logs to Jira as Tempo worklogs',
    'long_description': "[![CircleCI](https://circleci.com/gh/PrimaMateria/watson-jira-next/tree/master.svg?style=svg)](https://circleci.com/gh/PrimaMateria/watson-jira-next/tree/master)\n\n# Watson-Jira (next)\n\nUpload Watson time logs to Jira from the CLI! Selects Watson time logs based on the configurable mapping rules, formats those logs to Tempo format, and uploads to the appropriate Jira issues.\nWill not double-write logs, and makes no local edits.\n\nThis fork from original [project](https://github.com/medwig/watson-jira). Unfortunately original author doesn't reply. Please use this repository to open issues or pull requests.\n\n## Install\n\n`$ pip install watson-jira-next`\n\n\n## Config\n\nConfig is stored in `$XDG_CONFIG_HOME/.config/watson-jira/config.yaml`.\n\n### JIRA\n\n`jira` section should contain JIRA base URL and one of the authentication methods.\n\n```\nserver: <<JIRA base URL>>\n```\n\n#### Auth: API token\n\nSee [Atlassian docs](https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/). Add the following to the config file:\n\n```\nemail: <<email>>\napiToken: <<API token>>\n```\n\n#### Auth: Personal Access Token\n\nSee [Atlassian docs](https://confluence.atlassian.com/enterprise/using-personal-access-tokens-1026032365.html). Add the following to the config file:\n\n```\npersonalAccessToken: <<PAT>>\n```\n\n#### Auth: Cookie\n\n1. login to JIRA in the browser\n1. open Network tab in the developer tools\n1. copy the cookie from the request header \n1. add the following to the config file:\n\n```\ncookie: <<cookie>>\n```\n\n### Mappings \n\n`mappings` section contains list of mapping rules.\n\nMapping rule has name and type. For each Watson log, **Watson-Jira** tries to find the name in the tags. If found, then the JIRA issue number is resolved according to the type definition.\n\nMapping precedence is of the following order:\n\n#### Single issue\n\n```\nname: vacation\ntype: single_issue\nissue: JIRA-1\n```\n\nThis type always returns the one specified JIRA issue number.\n\n**Watson example:** `watson add -f 10:00 -t 18:00 none +vacation`\n\n#### Issue per project\n\n```\nname: maintenance\ntype: issue_per_project\nprojects:\n  project1: JIRA-2\n  project2: JIRA-3\n```\n\nThis type returns JIRA issue number based on the project name.\n\n**Watson example:** `watson add -f 10:00 -t 11:00 project2 +maintenance +dependencies-upgrade`\n\n#### Issue specified in the tag\n\n```\nname: sprint\ntype: issue_specified_in_tag\n```\n\nThis type resolves the JIRA issue number from the first tag which matches the issue number regex.\n\n**Example:** `watson add -f 10:00 -t 11:00 project1 +sprint +JIRA-123 +code`\n\n#### Issue specified in the project name\n\nFor any Watson log, which doesn't match any of the mappings, the JIRA issue number will be tried to be resolved from the project name.\n\n**Watson example:** `watson add -f 10:00 -t 11:00 JIRA-123 +investigation`\n\n### Full config example\n\n```\njira:\n  server: http://localhost:8080\n  cookie: atlassian.xsrf.token=BEHZ-5GE9-RXNS-7J78_bfa98881ae96448d36fdaa94f2b3ac6b8f205885_lout; JSESSIONID=51D8547A4C356A8355F8FDAF7CC97D51\nmappings:\n  - name: sprint\n    type: issue_specified_in_tag\n  - name: vacation\n    type: single_issue\n    issue: HR-123\n  - name: maintenance\n    type: issue_per_project\n    projects:\n      project1: JIRA-1\n      project2: JIRA-2\n```\n\n## Usage\n\n#### Show Jira-specific logs from today\n\n`$ watson-jira logs --jira-only --tempo-format`\n\n#### Show existing work logs for a Jira issue\n\n`$ watson-jira logs tempo --issue JIRA-1`\n\n#### Upload logs from today interactively\n\n`$ watson-jira sync --from 3 --interactive`\n\n#### Upload logs from the last 3 days\n\n`$ watson-jira sync --from 3`\n\n#### Help\n\n`$ watson-jira --help`\n\nWill install TD-Watson https://github.com/TailorDev/Watson as one of its dependencies, not surprisingly.\n",
    'author': 'matus.benko',
    'author_email': 'matus.benko@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
