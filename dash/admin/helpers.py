import requests, json

from openstack import connection, profile

from ..models import Provider


class Connect():
    def create_connection(self, auth_url, region, project_name, username, password):
        prof = profile.Profile()
        prof.set_version('identity', 'v3')
        prof.set_api_version('identity','v3')
        prof.set_region(profile.Profile.ALL, region)

        return connection.Connection(
            profile=prof,
            user_agent='examples',
            auth_url=auth_url,
            identity_api_version='3',
            project_name=project_name,
            username=username,
            password=password
        )