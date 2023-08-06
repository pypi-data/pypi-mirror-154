import requests, yaml

from ..githubcontroller import GitHubController
from ..base import Base


class AtomicRedTeam(GitHubController, Base):
    """
    Data Source: https://github.com/redcanaryco/atomic-red-team
    Author: Red Canary

    This class is a wrapper for the above data set
    """
    
    __RAW_URL = 'https://raw.githubusercontent.com/redcanaryco/atomic-red-team/master/{}'
    __REPO = 'redcanaryco/atomic-red-team'

    def __init__(self):
        super(AtomicRedTeam, self).__init__()
        self.session = requests.Session()
        self._dataset = []

    def get(self):
        repo = self.github.get_repo(self.__REPO)
        contents = repo.get_contents("")
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            else:
                if file_content.path.endswith('yaml') and not file_content.path.endswith('index.yaml'):
                    if 'atomics/' in file_content.path:
                        content = self.__download_raw_content(self.__RAW_URL.format(file_content.path))
                        self.__parse_yaml_content(content, file_content.path)

    def __parse_yaml_content(self, content, url):
        if 'atomic_tests' in content:
            for test in content['atomic_tests']:
                if 'executor' in test:
                    if 'command' in test['executor']:
                        if 'input_arguments' in test:
                            self.temp_command_string = None
                            for key,val in test['input_arguments'].items():
                                replacement_string = '#{{{0}}}'.format(key)
                                if self.temp_command_string is None:
                                    try:
                                        self.temp_command_string = test['executor']['command'].replace(replacement_string, test['input_arguments'][key]['default'])
                                    except:
                                        pass
                                else:
                                    try:
                                        self.temp_command_string = self.temp_command_string.replace(replacement_string, test['input_arguments'][key]['default'])
                                    except:
                                        pass
                                self.generated_data.add_command(
                                    technique_id=content["attack_technique"],
                                    source=url,
                                    name=f"Atomic Red Team Test - {content['display_name']}",
                                    command=self.temp_command_string
                                )
                                self.temp_command_string = None
                        else:
                            self.generated_data.add_command(
                                    technique_id=content["attack_technique"],
                                    source=url,
                                    name=f"Atomic Red Team Test - {content['display_name']}",
                                    command=test['executor']['command']
                                )
            self.generated_data.add_dataset(
                technique_id=content["attack_technique"],
                content=content
            )

    def __download_raw_content(self, url):
        response = self.session.get(url)
        if response.status_code == 200:
            return yaml.load(response.content, Loader=yaml.FullLoader)