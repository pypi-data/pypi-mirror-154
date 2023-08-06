import logging
import os

from rumpy.api import BaseAPI, FullNodeAPI, PaidGroup
from rumpy.client._flask_extensions import _init_app
from rumpy.client._requests import HttpRequest
from rumpy.types.data import ApiBaseURLS

logger = logging.getLogger(__name__)


class FullNode:
    _group_id = None

    def __init__(self, port=None, host="127.0.0.1", crtfile=None):
        if port is None:
            port = os.getenv("RUM_PORT", 51194)
        if crtfile is None:
            local_crtfile = r"C:\Users\75801\AppData\Local\Programs\prs-atm-app\resources\quorum-bin\certs\server.crt"
            crtfile = os.getenv("RUM_CRTFILE", local_crtfile)
        _apis = ApiBaseURLS(port=port, host=host)
        self.http = HttpRequest(_apis.FULL_NODE)
        self.api = self.http.api = FullNodeAPI(self.http)
        self.paid = self.http.paid = PaidGroup(self.http)

    @property
    def group_id(self):
        return self._group_id

    @group_id.setter
    def group_id(self, group_id):
        self._group_id = group_id
        self.http.group_id = group_id

    def init_app(self, app, rum_kspasswd=None, rum_port=None):
        return _init_app(self, app, rum_kspasswd, rum_port)
