from typing import Any

def load_endpoint_json(path): ...
def merge_endpoints(defaults, additions): ...
def load_regions(): ...
def get_regions(service_name, region_cls: Any | None = ..., connection_cls: Any | None = ...): ...

class RegionInfo:
    connection: Any
    name: Any
    endpoint: Any
    connection_cls: Any
    def __init__(
        self, connection: Any | None = ..., name: Any | None = ..., endpoint: Any | None = ..., connection_cls: Any | None = ...
    ) -> None: ...
    def startElement(self, name, attrs, connection): ...
    def endElement(self, name, value, connection): ...
    def connect(self, **kw_params): ...
