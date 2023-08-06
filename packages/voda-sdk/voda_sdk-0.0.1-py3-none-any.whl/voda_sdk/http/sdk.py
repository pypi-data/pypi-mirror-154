from datetime import datetime
from enum import Enum
from typing import Optional, Any, TypedDict, AnyStr, Dict, IO, List

import urllib.parse
from zoneinfo import ZoneInfo

import requests

from voda_sdk.sdk import SDK
from voda_sdk.utils import sanitize_isoformat


class LogLevel(Enum):
    NOTSET = 0
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


class AnalysisStatus(Enum):
    SUCCESS = '01'
    FAILURE = '02'


class DataType(Enum):
    COMMON = '00'
    TEXT = '01'  # txt
    IMAGE = '02'  # jpg, png, gif, bmp, svg, webp
    AUDIO = '03'  # wav, aiff, mp3, au, flac, m4a, ogg
    TIME_SERIES = '04'  # csv, tsv
    STREAMING_AUDIO = '05'
    STREAMING_VIDEO = '06'


class Endpoint(TypedDict):
    id: str
    station: dict
    name: str
    order: int
    data_type: str
    is_active: bool
    last_active: Optional[str]
    auth: dict
    is_authenticated: bool


class Payload(TypedDict):
    id: Optional[str]
    station: Optional[str]
    endpoint: Optional[str]
    data: Any
    data_type: str
    origin_name: str
    origin_time: str
    created: Optional[str]
    modified: Optional[str]


class Analysis(object):
    def __init__(self,
                 sdk: Any,
                 endpoint: Endpoint):
        self.endpoint = endpoint
        self.sdk = sdk

        self.id = None
        self.status = '00'
        self.is_ok = None
        self.identifier = None
        self.category = []

    @staticmethod
    def create(sdk: Any,
               endpoint: Endpoint,
               identifier: Optional[AnyStr] = None,
               category: Optional[List[AnyStr]] = None) -> 'Analysis':
        res = requests.post(
            urllib.parse.urljoin(sdk.server_url, '/api/sdk/analysis/'),
            data={
                'endpoint': endpoint['id'],
                'identifier': identifier,
                'category': category if category is not None else [],
            },
            headers={
                'X-Voda-SDK-Key': sdk.api_key
            }
        )
        if res.status_code > 300:
            raise RuntimeError(f'Can not create analysis instance')

        data = res.json()

        analysis = Analysis(sdk, endpoint)
        analysis.id = data['id']
        analysis.status = data['status']
        analysis.is_ok = data['is_ok']
        analysis.identifier = data['identifier']
        analysis.category = data['category']

        return analysis

    def log(self, message: AnyStr, level: LogLevel = LogLevel.INFO):
        """Record logs during analysis"""
        res = requests.post(
            urllib.parse.urljoin(self.sdk.server_url, '/api/sdk/log/'),
            data={
                'analysis_id': self.id,
                'data': message,
                'level': level,
            },
            headers={
                'X-Voda-SDK-Key': self.sdk.api_key
            }
        )
        if res.status_code > 300:
            raise RuntimeError(f'Can not create log')

    def upload_preview(self,
                       data: IO,
                       data_type: DataType,
                       name: Optional[AnyStr] = None,
                       timestamp: Optional[AnyStr] = None):
        """Upload data file for preview of analysis"""
        try:
            if timestamp is None:
                raise ValueError
            origin_time = datetime.fromisoformat(sanitize_isoformat(timestamp)).isoformat()
        except ValueError:
            origin_time = datetime.now(tz=self.sdk.timezone).isoformat()

        res = requests.post(
            urllib.parse.urljoin(self.sdk.server_url, '/api/sdk/payloads/'),
            data={
                'endpoint': self.endpoint['id'],
                'data': data,
                'data_type': data_type,
                'origin_name': name,
                'origin_time': origin_time,
            },
            headers={
                'X-Voda-SDK-Key': self.sdk.api_key
            }
        )
        if res.status_code > 300:
            raise RuntimeError(f'Can not upload preview data')

        payload: Payload = res.json()
        res = requests.patch(
            urllib.parse.urljoin(self.sdk.server_url, f'/api/sdk/analysis/{self.id}/'),
            data={
                'payload': payload['id'],
            },
            headers={
                'X-Voda-SDK-Key': self.sdk.api_key
            }
        )
        if res.status_code > 300:
            raise RuntimeError(f'Can not make relation preview data to analysis')

    def update(self,
               identifier: Optional[AnyStr] = None,
               category: Optional[List[AnyStr]] = None):
        """Update information related to analysis"""
        data = dict()
        if identifier is not None:
            data['identifier'] = identifier
        if category is not None:
            data['category'] = category

        res = requests.patch(
            urllib.parse.urljoin(self.sdk.server_url, '/api/sdk/analysis/'),
            data=data,
            headers={
                'X-Voda-SDK-Key': self.sdk.api_key
            }
        )
        if res.status_code > 300:
            raise RuntimeError(f'Can not update analysis')

    def close(self,
              result: Dict,
              status: AnalysisStatus = AnalysisStatus.SUCCESS,
              is_ok: Optional[bool] = None):
        """End the analysis and save the results"""
        res = requests.post(
            urllib.parse.urljoin(self.sdk.server_url, f'/api/sdk/analysis-results/'),
            data={
                'analysis': self.id,
                'result': result,
            },
            headers={
                'X-Voda-SDK-Key': self.sdk.api_key
            }
        )
        if res.status_code > 300:
            raise RuntimeError(f'Can not save analysis result')

        res = requests.patch(
            urllib.parse.urljoin(self.sdk.server_url, f'/api/sdk/analysis/{self.id}/'),
            data={
                'status': status,
                'is_ok': is_ok,
            },
            headers={
                'X-Voda-SDK-Key': self.sdk.api_key
            }
        )
        if res.status_code > 300:
            raise RuntimeError(f'Can not close analysis instance')


class HttpSDK(SDK):
    """
    SDK Client based HTTP
    """

    def __init__(self,
                 server_url: str,
                 api_key: str,
                 timezone='Asia/Seoul'):
        self.server_url = server_url
        self.api_key = api_key
        self._is_authenticated = False
        self.timezone = ZoneInfo(timezone)
        self.healthcheck()
        self.auth()

    def healthcheck(self):
        """Check alive status of VODA Core server"""
        try:
            response = requests.get(urllib.parse.urljoin(self.server_url, '/api/sdk/healthcheck/'))
            if response.status_code != 200:
                raise RuntimeError(f'Can not connect to VODA Core server({self.server_url})')
        except requests.exceptions.RequestException:
            raise RuntimeError(f'Can not connect to VODA Core server({self.server_url})')

    def auth(self):
        """Authorization to use the SDK"""
        if self._is_authenticated:
            raise RuntimeError('The current session has already been authenticated.')

        try:
            response = requests.post(
                urllib.parse.urljoin(self.server_url, '/api/sdk/auth/'),
                data={
                    'api_key': self.api_key
                }
            )
            if response.status_code != 200:
                raise RuntimeError(f'Can not authenticate to VODA Core server({self.server_url}) with Key({self.api_key})')
            self._is_authenticated = True
        except requests.exceptions.RequestException:
            raise RuntimeError(f'Can not authenticate to VODA Core server({self.server_url})')

    def get_endpoint(self, endpoint_id: str) -> Endpoint:
        """Get endpoint information"""
        response = requests.post(
            urllib.parse.urljoin(self.server_url, f'/api/sdk/endpoints/{endpoint_id}/'),
            data={
                'api_key': self.api_key
            }
        )
        if response.status_code != 200:
            raise RuntimeError(f'Can not get Endpoint({endpoint_id})')
        endpoint: Endpoint = response.json()
        return endpoint

    def open_analysis(self,
                      endpoint: Endpoint,
                      identifier: Optional[AnyStr] = None,
                      category: Optional[List[AnyStr]] = None) -> Analysis:
        """Open analysis object"""
        analysis = Analysis.create(self, endpoint, identifier, category)
        return analysis

    def run_model(self,
                  model_name: str,
                  input_data: Any,
                  model_version: Optional[int] = None,
                  analyzer_server_url: Optional[str] = None):
        """Run AI model on VODA Analyzer Server"""
        pass
