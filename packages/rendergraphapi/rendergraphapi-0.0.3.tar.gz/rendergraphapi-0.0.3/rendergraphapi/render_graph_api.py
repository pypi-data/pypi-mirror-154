from typing import List

import requests
from authenticator import HOTP
from requests import Session

from rendergraphapi.schema import TeamsForUserList, TeamsForUserItem, DatabasesForOwnerList, DatabasesForOwnerItem, DatabaseBackupItem


class RenderGraphApi:
    GRAPH_URL = 'https://api.render.com/graphql'
    session: Session
    user_id: str

    def __init__(self, email: str, password: str, otp_secret: str):
        self.email = email
        self.password = password
        self.otp_secret = otp_secret
        self.session = requests.session()
        self.session.headers.update({'Content-Type': 'application/json'})

    def generate_otp(self, secret: str) -> str:
        secret = "".join(secret.split()).upper()

        code_string, _ = HOTP().generate_code_from_time(
            secret,
            code_length=6,
            period=30
        )
        return code_string

    def post(self, data) -> dict:
        response = self.session.post(self.GRAPH_URL, json=data)
        if response.status_code >= 400:
            raise Exception(response.text)
        result = response.json()
        if 'errors' in result:
            raise Exception(response.text)
        return result

    def login(self):
        data = {
            "operationName": "signIn",
            "variables": {
                "email": self.email,
                "password": self.password
            },
            "query": "mutation signIn($email: String!, $password: String!) {\n  signIn(email: $email, password: $password) {\n    ...authResultFields\n    __typename\n  }\n}\n\nfragment authResultFields on AuthResult {\n  idToken\n  user {\n    ...userFields\n    sudoModeExpiresAt\n    __typename\n  }\n  __typename\n}\n\nfragment userFields on User {\n  id\n  active\n  createdAt\n  email\n  featureFlags\n  githubId\n  gitlabId\n  name\n  notEligibleFeatureFlags\n  notifyOnFail\n  notifyOnPrUpdate\n  otpEnabled\n  passwordExists\n  tosAcceptedAt\n  intercomHMAC\n  __typename\n}\n"
        }
        sign_in_response = self.post(data)

        token = sign_in_response['data']['signIn']['idToken']
        self.session.headers.update({'Authorization': f'Bearer {token}'})

        otp_response = self.post(
            {
                "operationName": "verifyOneTimePassword",
                "variables": {
                    "code": self.generate_otp(self.otp_secret)
                },
                "query": "mutation verifyOneTimePassword($code: String!) {\n  verifyOneTimePassword(code: $code) {\n    ...authResultFields\n    __typename\n  }\n}\n\nfragment authResultFields on AuthResult {\n  idToken\n  user {\n    ...userFields\n    sudoModeExpiresAt\n    __typename\n  }\n  __typename\n}\n\nfragment userFields on User {\n  id\n  active\n  createdAt\n  email\n  featureFlags\n  githubId\n  gitlabId\n  name\n  notEligibleFeatureFlags\n  notifyOnFail\n  notifyOnPrUpdate\n  otpEnabled\n  passwordExists\n  tosAcceptedAt\n  intercomHMAC\n  __typename\n}\n"
            }
        )
        otp_token = otp_response['data']['verifyOneTimePassword']['idToken']
        self.session.headers.update({'Authorization': f'Bearer {otp_token}'})

        self.user_id = otp_response['data']['verifyOneTimePassword']['user']['id']

    def get_teams(self) -> List[TeamsForUserItem]:
        response = self.post({
            "operationName": "teamsForUser",
            "variables": {
                "userId": self.user_id
            },
            "query": "query teamsForUser($userId: String!) {\n  teamsForUser(userId: $userId) {\n    ...teamFields\n    __typename\n  }\n}\n\nfragment teamFields on Team {\n  id\n  name\n  email\n  __typename\n}\n"
        })
        model = TeamsForUserList(**response['data'])
        return model.teamsForUser

    def get_databases(self, owner_id: str) -> List[DatabasesForOwnerItem]:
        response = self.post({
            "operationName": "databasesForOwner",
            "variables": {
                "ownerId": owner_id
            },
            "query": "query databasesForOwner($ownerId: String!) {\n  databasesForOwner(ownerId: $ownerId) {\n    id\n    name\n    type\n    status\n    suspenders\n    pendingMaintenanceBy\n    createdAt\n    updatedAt\n    userFacingType\n    postgresMajorVersion\n    region {\n      id\n      description\n      __typename\n    }\n    __typename\n  }\n}\n"
        })
        return DatabasesForOwnerList(**response['data']).databasesForOwner

    def get_database_backups(self, database_id: str) -> List[DatabaseBackupItem]:
        response = self.post({
            "operationName": "databaseBackupsQuery",
            "variables": {
                "databaseId": database_id
            },
            "query": "query databaseBackupsQuery($databaseId: String!) {\n  database(id: $databaseId) {\n    id\n    backups {\n      edges {\n        node {\n          id\n          createdAt\n          baseUrl\n          sqlUrl\n          status\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
        })
        return [DatabaseBackupItem(**x['node']) for x in response['data']['database']['backups']['edges']]
