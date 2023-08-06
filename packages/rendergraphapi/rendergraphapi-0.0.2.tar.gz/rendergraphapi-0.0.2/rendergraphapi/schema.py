from io import BytesIO
from typing import List, Any

import requests
from pydantic import BaseModel


class TeamsForUserItem(BaseModel):
    id: str
    name: str
    email: str
    __typename: str


class TeamsForUserList(BaseModel):
    teamsForUser: List[TeamsForUserItem]


class Region(BaseModel):
    id: str
    description: str
    __typename: str


class DatabasesForOwnerItem(BaseModel):
    id: str
    name: str
    type: str
    status: str
    suspenders: List
    pendingMaintenanceBy: Any
    createdAt: str
    updatedAt: str
    userFacingType: str
    postgresMajorVersion: str
    region: Region
    __typename: str


class DatabasesForOwnerList(BaseModel):
    databasesForOwner: List[DatabasesForOwnerItem]


class DatabaseBackupItem(BaseModel):
    id: str
    createdAt: str
    baseUrl: str
    sqlUrl: str
    status: str
    __typename: str

    def _url_to_bytes(self, url: str) -> BytesIO:
        response = requests.get(url)
        return BytesIO(response.content)

    def download_sql(self) -> BytesIO:
        return self._url_to_bytes(self.sqlUrl)

    def download_base(self) -> BytesIO:
        return self._url_to_bytes(self.baseUrl)
