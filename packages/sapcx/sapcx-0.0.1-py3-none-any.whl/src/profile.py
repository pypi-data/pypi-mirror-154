#!/usr/bin/env python3
import json
import os.path


class Profile:
    config_path = os.path.join(os.path.expanduser('~'), '.sap-cli')
    profile_path = os.path.join(config_path, 'profiles')

    def __init__(self, identifier, username='admin', password='nimda', server='127.0.0.1', port=9002, ssl=True,
                 webroot='/'):
        self.identifier = identifier
        self.username = username
        self.password = password
        self.server = server
        self.port = int(port)
        self.ssl = ssl
        self.webroot = webroot

        if not os.path.exists(self.config_path):
            os.mkdir(self.config_path)

    def save(self):
        with open(self.profile_path, 'w+') as f:
            profiles = json.loads(f.read())
            profiles[self.identifier] = {
                'username': self.username,
                'password': self.password,
                'server': self.server,
                'port': self.port,
                'ssl': self.ssl,
                'webroot': self.webroot
            }
            json.dump(profiles, f)

    def remove(self):
        with open(self.profile_path, 'w+') as f:
            profiles = json.load(f)
            if self.identifier in profiles.keys():
                del profiles[self.identifier]
                json.dump(profiles, f)

    def load(self):
        if os.path.exists(self.profile_path):
            with open(self.profile_path, 'r+') as f:
                profiles = json.load(f)
                if self.identifier in profiles.keys():
                    profile = profiles[self.identifier]
                    self.username = profile['username'],
                    self.password = profile['password'],
                    self.ssl = profile['ssl'],
                    self.server = profile['server'],
                    self.port = profile['port'],
                    self.webroot = profile['webroot']
                else:
                    AttributeError(f"Profile {self.identifier} does NOT exists !!!")
