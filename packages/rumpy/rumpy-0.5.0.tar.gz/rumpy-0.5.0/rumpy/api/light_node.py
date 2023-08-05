import json
import logging
from typing import Any, Dict, List

from rumpy.api.base import BaseAPI
from rumpy.types.data import NewTrx

logger = logging.getLogger(__name__)


class LightNodeAPI(BaseAPI):
    def quit(self):
        return self._get("/quit")

    def __create_alias_of_key(self, alias: str, key_type: str):
        if key_type not in ("sign", "encrypt"):
            raise ValueError("key_type must be one of `sign`, `encrypt`.")
        payload = {"alias": alias, "type": key_type}
        return self._post("/v1/keystore/create", payload)

    def create_alias_of_sign_key(self, alias="my_signe"):
        return self.__create_alias_of_key(alias, "sign")

    def create_alias_of_encrypt_key(self, alias="my_encrypt"):
        # """需要环境变量 RUM_KSPASSWD"""
        # if not os.getenv("RUM_KSPASSWD"):
        #    raise ValueError("need RUM_KSPASSWD")
        return self.__create_alias_of_key(alias, "encrypt")

    def create_keypair(self, alias_piece="my"):
        self.create_alias_of_sign_key(alias_piece + "_sign")
        self.create_alias_of_encrypt_key(alias_piece + "_encrypt")

    def keys(self):
        return self._get("/v1/keystore/listall")

    def remove_alias(self, alias):
        payload = {"alias": alias}
        return self._post("/v1/keystore/remove", payload)

    def bind_alias(self, alias, keyname, type_str):
        payload = {"alias": alias, "keyname": keyname, "type": type_str}
        return self._post("/v1/keystore/bindalias", payload)

    def join_group(self, seed: Dict, sign_alias: str, encrypt_alias: str, urls: List):
        payload = {
            "seed": seed,
            "sign_alias": sign_alias,
            "encrypt_alias": encrypt_alias,
            "urls": urls,
        }
        return self._post("/v1/group/join", payload)

    def update_apihosts(self, group_id, urls):
        payload = {
            "group_id": group_id,
            "urls": urls,
        }
        return self._post("/v1/group/apihosts", payload)

    def leave_group(self, group_id):
        payload = {
            "group_id": group_id,
        }
        return self._post("/v1/group/leave", payload)

    def groups(self):
        return self._get("/v1/group/listall")

    def group(self, group_id):
        return self._get(f"/v1/group/{group_id}/list")

    def group_info(self, group_id):
        return self._get(f"/v1/group/{group_id}/info")

    def seed(self, group_id):
        return self._get(f"/v1/group/{group_id}/seed")

    def trx(self, group_id, trx_id):
        return self._get(f"/v1/trx/{group_id}/{trx_id}")

    def block(self, group_id, block_id):
        return self._get(f"/v1/block/{group_id}/{block_id}")

    def producers(self, group_id):
        return self._get(f"/v1/group/{group_id}/producers")

    def users(self, group_id):
        return self._get(f"/v1/group/{group_id}/announced/users")

    def user(self, group_id, pubkey):
        return self._get(f"/v1/group/{group_id}/announced/user/{pubkey}")

    def appconfig_keylist(self, group_id):
        return self._get(f"/v1/group/{group_id}/appconfig/keylist")

    def appconfig_key(self, group_id, key):
        return self._get(f"/v1/group/{group_id}/appconfig/{key}")

    def get_group_content(
        self,
        group_id: str,
        reverse: bool = False,
        start_trx: str = None,
        num: int = 20,
        include_start_trx: bool = False,
    ) -> List:

        payload = {
            "group_id": group_id,
            "num": num,
            "start_trx": start_trx,
            "reverse": json.dumps(reverse),
            "include_start_trx": json.dumps(include_start_trx),
        }

        return self._post(f"/v1/group/getctn", payload)

    def _send(self, group_id: str, obj=None, sendtype=None, **kwargs) -> Dict:
        payload = NewTrx(group_id=group_id, obj=obj, sendtype=sendtype, **kwargs).__dict__
        return self._post("/v1/group/content", payload)

    def like(self, group_id: str, trx_id: str) -> Dict:
        return self._send(group_id=group_id, trx_id=trx_id, sendtype="Like")

    def dislike(self, group_id: str, trx_id: str) -> Dict:
        return self._send(group_id=group_id, trx_id=trx_id, sendtype="Dislike")

    def send_note(self, group_id: str, **kwargs):
        return self._send(group_id, sendtype="Add", objtype="Note", **kwargs)

    def reply(self, group_id: str, content: str, trx_id: str, images=None):
        return self.send_note(group_id, content=content, images=images, inreplyto=trx_id)

    def send_text(self, group_id: str, content: str, name: str = None):
        return self.send_note(group_id, content=content, name=name)

    def send_img(self, group_id: str, images):
        if type(images) != list:
            images = [images]
        return self.send_note(group_id, images=images)

    def update_profile(self, group_id, name=None, wallet=None, image=None):
        payload = {}  # todo
        return self._post(f"/v1/group/profile", payload)
