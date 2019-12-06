from enum import Enum


class RequestMetaData:
    TIME = '__START_TIME__'
    ROUTER = '__ROUTER_URI__'


class BaseMetrics(Enum):
    LATENCY = 'sanic_request_latency_sec'
    COUNT = 'sanic_request_count'
