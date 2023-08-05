import base64
import datetime
import hashlib
import json
import logging
import math
import os
import sys
import time
import urllib
from typing import Any, Dict, List

import filetype

from rumpy.api.base import BaseAPI
from rumpy.types.data import *
from rumpy.utils import sha256, timestamp_to_datetime, zip_image_file

logger = logging.getLogger(__name__)

CHUNK_SIZE = 150 * 1024  # 150kb


def _check_mode(mode: str):
    if mode.lower() not in ["dny", "deny", "allow", "alw"]:
        raise ValueError(f"{mode} mode must be one of ['deny','allow']")
    if mode.lower() in ["dny", "deny"]:
        return "dny"
    if mode.lower() in ["alw", "allow"]:
        return "alw"


def _check_trx_type(trx_type: str):
    if trx_type.upper() not in TRX_TYPES:
        raise ValueError(f"{trx_type} must be one of {TRX_TYPES}")
    return trx_type.lower()


def _quote(text):
    return "".join(["> ", "\n> ".join(text.split("\n")), "\n"]) if text else ""


def _nickname(pubkey, nicknames):
    try:
        name = nicknames[pubkey]["name"] + f"({pubkey[-10:-2]})"
    except:
        name = pubkey[-10:-2] or "某人"
    return name


def _trxs_unique(trxs: List):
    """remove the duplicate trx from the trxs list"""
    new = {}
    for trx in trxs:
        if trx["TrxId"] not in new:
            new[trx["TrxId"]] = trx
    return [new[i] for i in new]


class FullNodeAPI(BaseAPI):
    @property
    def node_info(self):
        """return node info, dataclasses.dataclass type"""
        resp = self._get("/api/v1/node")
        return NodeInfo(**resp)

    @property
    def node_id(self) -> str:
        """return node_id of this node"""
        return self.node_info.node_id

    @property
    def node_pubkey(self) -> str:
        """return pubkey of this node; be attention: node will get different pubkey in groups"""
        return self.node_info.node_publickey

    @property
    def node_status(self) -> str:
        """return status of this node; unknown, online or offline"""
        return self.node_info.node_status

    @property
    def peers(self) -> Dict:
        """return dict of different peers which this node has connected"""
        return self.node_info.peers

    def connect(self, peers: List):
        """直连指定节点

        peers = [
            "/ip4/94.23.17.189/tcp/10666/p2p/16Uiu2HAmGTcDnhj3KVQUwVx8SGLyKBXQwfAxNayJdEwfsnUYKK4u"
            ]
        """
        return self._post("/api/v1/network/peers", peers)

    def get_peers(self):
        """获取能 ping 通的节点"""
        return self._get("/api/v1/network/peers/ping")

    def psping(self, peer_id: str):
        """ping 一个节点

        peer_id: 节点 ID, 例如 "16Uiu2HAxxxxxx...xxxxzEYBnEKFnao"
        """
        return self._post("/api/v1/psping", {"peer_id": peer_id})

    @property
    def network(self) -> Dict:
        """return network info of this node"""
        return self._get("/api/v1/network")

    @property
    def node_eth_addr(self):
        return self.network.get("eth_addr")

    def groups(self) -> List:
        """return list of group info which node has joined"""
        return self._get("/api/v1/groups")["groups"]

    @property
    def groups_id(self) -> List:
        """return list of group_id which node has joined"""
        return [i["group_id"] for i in self.groups()]

    def backup(self):
        """Backup my group seed/keystore/config"""
        return self._get("/api/v1/backup")

    def token(self):
        """Get a auth token for authorizing requests from remote"""
        return self._post("/app/api/v1/token/apply")

    def token_refresh(self):
        """Get a new auth token"""
        return self._post("/app/api/v1/token/refresh")

    def network_stats(self, start: str = None, end: str = None):
        """Get network stats summary

        param: start/end, str, query, "2022-04-28" or "2022-04-28 10:00" or "2022-04-28T10:00Z08:00"
        """
        api = "/api/v1/network/stats"

        if start or end:
            query = "?"
            if start:
                query += f"&start={start}"
            if end:
                query += f"&end={end}"
            api += urllib.parse.quote(query, safe="?&/")

        return self._get(api)

    def create_group(
        self,
        group_name: str,
        app_key: str = "group_timeline",
        consensus_type: str = "poa",
        encryption_type: str = "public",
    ) -> Dict:
        """create a group, return the seed of the group.

        group_name: 组名, 自定义, 不可更改
        consensus_type: 共识类型, "poa", "pos", "pow", 当前仅支持 "poa"
        encryption_type: 加密类型, "public" 公开, "private" 私有
        app_key: 可以为自定义字段，只是如果不是 group_timeline,
            group_post, group_note 这三种，可能无法在 rum-app 中识别，
            如果是自己开发客户端，则可以自定义类型

        创建成功, 返回值是一个种子, 通过它其他人可加入该组
        """
        # check encryption_type
        if encryption_type.lower() not in ("public", "private"):
            raise ValueError("encryption_type should be `public` or `private`")

        # check consensus_type
        if consensus_type.lower() not in ("poa",):
            raise ValueError("consensus_type should be `poa` or `pos` or `pow`, but only `poa` is supported now.")

        payload = {
            "group_name": group_name,
            "consensus_type": consensus_type,
            "encryption_type": encryption_type,
            "app_key": app_key,
        }

        return self._post("/api/v1/group", payload)

    def seed(self, group_id=None) -> Dict:
        """get the seed of a group which you've joined in."""
        group_id = self.check_group_id_as_required(group_id)
        seed = self._get(f"/api/v1/group/{group_id}/seed")
        if "error" not in seed:
            return seed
        else:
            raise ValueError(seed["error"])

    def group_info(self, group_id=None):
        """return group info,type: datacalss"""

        group_id = self.check_group_joined_as_required(group_id)

        info = {}
        for _info in self.groups():
            if _info["group_id"] == group_id:
                info = _info
                break

        if info.get("snapshot_info") is None:
            info["snapshot_info"] = {}

        return GroupInfo(**info)

    @property
    def pubkey(self):
        return self.group_info().user_pubkey

    @property
    def owner(self):
        return self.group_info().owner_pubkey

    @property
    def eth_addr(self):
        return self.group_info().user_eth_addr

    def join_group(self, seed: Dict):
        """join a group with the seed of the group"""
        if not is_seed(seed):
            raise ValueError("not a seed or the seed could not be identified.")
        resp = self._post("/api/v1/group/join", seed)
        if "error" in resp:
            if resp["error"] == "Group with same GroupId existed":
                resp = True
            else:
                raise ValueError(resp["error"])
        return resp

    def is_joined(self, group_id=None) -> bool:
        group_id = self.check_group_id_as_required(group_id)
        if group_id in self.groups_id:
            return True
        return False

    def leave_group(self, group_id=None):
        """leave a group"""
        group_id = self.check_group_id_as_required(group_id)
        return self._post("/api/v1/group/leave", {"group_id": group_id})

    def clear_group(self, group_id=None):
        """clear data of a group"""
        group_id = self.check_group_id_as_required(group_id)
        return self._post("/api/v1/group/clear", {"group_id": group_id})

    def startsync(self, group_id=None):
        """触发同步"""
        group_id = self.check_group_id_as_required(group_id)
        return self._post(f"/api/v1/group/{group_id}/startsync")

    def content_trxs(
        self,
        group_id=None,
        is_reverse: bool = False,
        trx_id: str = None,
        num: int = 20,
        is_include_starttrx: bool = False,
        senders: List = None,
    ) -> List:
        """requests the content trxs of a group,return the list of the trxs data.

        按条件获取某个组的内容并去重返回

        is_reverse: 默认按顺序获取, 如果是 True, 从最新的内容开始获取
        trx_id: 某条内容的 Trx ID, 如果提供, 从该条之后(不包含)获取
        num: 要获取内容条数, 默认获取最前面的 20 条内容
        is_include_starttrx: 如果是 True, 获取内容包含 Trx ID 这条内容
        """
        group_id = self.check_group_joined_as_required(group_id, quiet=True)
        if not group_id:
            return []

        if trx_id:
            apiurl = f"/app/api/v1/group/{group_id}/content?num={num}&starttrx={trx_id}&reverse={str(is_reverse).lower()}&includestarttrx={str(is_include_starttrx).lower()}"
        else:
            apiurl = f"/app/api/v1/group/{group_id}/content?num={num}&reverse={str(is_reverse).lower()}"

        trxs = self._post(apiurl) or []
        return _trxs_unique(trxs)

    def _send(self, obj=None, sendtype=None, group_id=None, **kwargs) -> Dict:
        """return the {trx_id:trx_id} of this action if send successded

        obj: 要发送的对象
        sendtype: 发送类型, "Add"(发送内容), "Like"(点赞), "Dislike"(点踩)
        返回值 {"trx_id": "string"}
        """
        group_id = self.check_group_joined_as_required(group_id)
        payload = NewTrx(group_id=group_id, obj=obj, sendtype=sendtype, **kwargs).__dict__
        return self._post("/api/v1/group/content", payload)

    def like(self, trx_id: str, group_id=None) -> Dict:
        return self._send(trx_id=trx_id, sendtype="Like", group_id=group_id)

    def dislike(self, trx_id: str, group_id=None) -> Dict:
        return self._send(trx_id=trx_id, sendtype="Dislike", group_id=group_id)

    def _file_to_objs(self, file_path):
        file_total_size = os.path.getsize(file_path)
        file_name = os.path.basename(file_path).encode().decode("utf-8")
        file_obj = open(file_path, "rb")
        fileinfo = {
            "mediaType": filetype.guess(file_path).mime,
            "name": file_name,
            "title": file_name.split(".")[0],
            "sha256": sha256(file_obj.read()),
            "segments": [],
        }

        chunks = math.ceil(file_total_size / CHUNK_SIZE)
        objs = []

        for i in range(chunks):
            if i + 1 == chunks:
                current_size = file_total_size % CHUNK_SIZE
            else:
                current_size = CHUNK_SIZE
            file_obj.seek(i * CHUNK_SIZE)
            ibytes = file_obj.read(current_size)
            fileinfo["segments"].append({"id": f"seg-{i+1}", "sha256": sha256(ibytes)})
            obj = FileObj(
                name=f"seg-{i + 1}",
                content=ibytes,
                mediaType="application/octet-stream",
            )
            objs.append(obj)

        content = json.dumps(fileinfo).encode()
        obj = FileObj(content=content, name="fileinfo", mediaType="application/json")

        objs.insert(0, obj)
        file_obj.close()
        return objs

    def upload_file(self, file_path):
        if not os.path.isfile(file_path):
            logger.info(f"{sys._getframe().f_code.co_name}, {file_path} is not a file.")
            return
        for obj in self._file_to_objs(file_path):
            self._send(obj=obj, sendtype="Add")

    def _file_infos(self, trx_id=None):
        trxs = self.all_content_trxs(trx_id)
        infos = []
        filetrxs = []
        for trx in trxs:
            if trx["Content"].get("name") == "fileinfo":
                info = eval(base64.b64decode(trx["Content"]["file"]["content"]).decode("utf-8"))
                logger.debug(f"{sys._getframe().f_code.co_name}, {info}")
                infos.append(info)
            if trx["Content"].get("type") == "File":
                filetrxs.append(trx)
        return infos, filetrxs

    def _down_load(self, file_dir, info, trxs):

        ifilepath = os.path.join(file_dir, info["name"])
        if os.path.exists(ifilepath):
            logger.info(f"{sys._getframe().f_code.co_name}, file exists {ifilepath}")
            return

        # _check_trxs
        right_shas = [i["sha256"] for i in info["segments"]]
        contents = {}

        for trx in trxs:
            content = base64.b64decode(trx["Content"]["file"]["content"])
            csha = hashlib.sha256(content).hexdigest()
            if csha in right_shas:
                contents[csha] = trx

        flag = True

        for seg in info["segments"]:
            if seg["sha256"] not in contents:
                logger.info(f"{sys._getframe().f_code.co_name}, " + json.dumps(seg) + ", trx is not exists...")
                flag = False
                break
            if contents[seg["sha256"]]["Content"].get("name") != seg["id"]:
                logger.info(f"{sys._getframe().f_code.co_name}, " + json.dumps(seg) + ", name is different...")
                flag = False
                break

        if flag:
            ifile = open(ifilepath, "wb+")
            for seg in info["segments"]:
                content = base64.b64decode(contents[seg["sha256"]]["Content"]["file"]["content"])
                ifile.write(content)
            ifile.close()
            logger.info(f"{sys._getframe().f_code.co_name}, {ifilepath}, downloaded!")

    def download_file(self, file_dir):
        logger.debug(f"download file to dir {file_dir} start...")
        infos, trxs = self._file_infos()
        for info in infos:
            self._down_load(file_dir, info, trxs)
        logger.debug(f"download file to dir {file_dir} done")

    def send_note(self, group_id=None, **kwargs):
        return self._send(sendtype="Add", group_id=group_id, objtype="Note", **kwargs)

    def reply(self, content: str, trx_id: str, group_id=None, images=None):
        """回复某条内容(仅图片, 仅文本, 或两者都有)

        trx_id: 要回复的内容的 Trx ID
        content: 用于回复的文本内容
        images: 一张或多张(最多4张)图片的路径, 一张是字符串, 多张则是它们组成的列表
            content 和 images 必须至少一个不是 None
        """
        return self.send_note(content=content, images=images, group_id=group_id, inreplyto=trx_id)

    def send_text(self, content: str, name: str = None, group_id=None):
        """post text cotnent to group

        content: 要发送的文本内容
        name: 内容标题, 例如 rum-app 论坛模板必须提供的文章标题
        """
        return self.send_note(content=content, name=name, group_id=group_id)

    def send_img(self, images, group_id=None):
        """post images to group

        images: 一张或多张(最多4张)图片的路径, 一张是字符串, 多张则是它们组成的列表
        """
        if type(images) != list:
            images = [images]
        return self.send_note(images=images, group_id=group_id)

    def block(self, block_id: str, group_id=None):
        """get the info of a block in a group"""
        group_id = self.check_group_id_as_required(group_id)
        return self._get(f"/api/v1/block/{group_id}/{block_id}")

    def is_owner(self, group_id=None) -> bool:
        """return True if I create this group else False"""
        group_id = self.check_group_id_as_required(group_id)
        info = self.group_info(group_id)
        if info.owner_pubkey == info.user_pubkey:
            return True
        return False

    def all_content_trxs(self, trx_id: str = None, group_id=None, senders=None):
        """get all the trxs of content started from trx_id"""
        group_id = self.check_group_id_as_required(group_id)
        trxs = []
        checked_trxids = []
        senders = senders or []
        while True:
            if trx_id in checked_trxids:
                break
            else:
                checked_trxids.append(trx_id)
            newtrxs = self.content_trxs(trx_id=trx_id, num=100, group_id=group_id)
            if len(newtrxs) == 0:
                break
            if senders:
                trxs.extend([itrx for itrx in newtrxs if itrx.get("Publisher") in senders])
            else:
                trxs.extend(newtrxs)
            trx_id = self.last_trx_id(trx_id, newtrxs)
        return trxs

    def last_trx_id(self, trx_id: str, trxs: List):
        """get the last-trx_id of trxs which if different from given trx_id"""
        for i in range(-1, -1 * len(trxs), -1):
            tid = trxs[i]["TrxId"]
            if tid != trx_id:
                return tid
        return trx_id

    def trx_type(self, trxdata: Dict):
        """get type of trx, trx is one of group content list"""
        if "TypeUrl" not in trxdata:
            return "encrypted"
        if trxdata["TypeUrl"] == "quorum.pb.Person":
            return "person"
        content = trxdata["Content"]
        trxtype = content.get("type", "other")
        if type(trxtype) == int:
            return "announce"
        if trxtype == "Note":
            if "inreplyto" in content:
                return "reply"
            if "image" in content:
                if "content" not in content:
                    return "image_only"
                else:
                    return "image_text"
            return "text_only"
        return trxtype.lower()  # "like","dislike","other"

    def trx(self, trx_id: str, group_id=None):
        """get trx data by trx_id"""
        group_id = self.check_group_id_as_required(group_id)
        data = {}
        trxs = self.content_trxs(trx_id=trx_id, num=1, is_include_starttrx=True, group_id=group_id)
        if len(trxs) > 1:
            raise ValueError(f"{len(trxs)} trxs got from group: <{group_id}> with trx: <{trx_id}>.")
        elif len(trxs) == 1:
            data = trxs[0]
        else:
            data = self._get(f"/api/v1/trx/{group_id}/{trx_id}")
            logger.info(f"data is encrypted for trx: <{trx_id}> of group: <{group_id}>.")
        if not data:
            logger.warning(f"data is empty for trx: <{trx_id}> of group: <{group_id}>.")
        return data

    def pubqueue(self, group_id=None):
        group_id = self.check_group_id_as_required(group_id)
        resp = self._get(f"/api/v1/group/{group_id}/pubqueue")
        return resp.get("Data")

    def ack(self, trx_ids: List):
        return self._post("/api/v1/trx/ack", {"trx_ids": trx_ids})

    def autoack(self, group_id=None):
        group_id = self.check_group_id_as_required(group_id)
        tids = [i["Trx"]["TrxId"] for i in self.pubqueue(group_id) if i["State"] == "FAIL"]
        return self.ack(tids)

    def get_users_profiles(
        self,
        users_data: Dict = {},
        types=("name", "image", "wallet"),
        group_id=None,
    ) -> Dict:
        """update users_data and returns it.
        {
            group_id:  "", # the group_id
            group_name: "", # the group_name
            trx_id: "", # the trx_id of groups progress
            trx_timestamp:"",
            update_at: "",
            data:{ pubkey:{
                name:"",
                image:{},
                wallet:[],
                }
            }
        }
        """
        # check group_id

        group_id = users_data.get("group_id") or self.check_group_id_as_required(group_id)

        # get new trxs from the trx_id
        trx_id = users_data.get("trx_id", None)
        trxs = self.all_content_trxs(trx_id=trx_id, group_id=group_id)

        if len(trxs) == 0:
            logger.debug(f"get_users_profiles: got 0 new trxs. get content started from trx_id:{trx_id}.")
            return users_data

        # update trx_id: to record the progress to get new trxs

        users_data.update(
            {
                "group_id": group_id,
                "group_name": self.seed(group_id).get("group_name"),
                "trx_id": trxs[-1]["TrxId"],
                "trx_timestamp": str(timestamp_to_datetime(trxs[-1].get("TimeStamp", ""))),
            }
        )

        users = users_data.get("data", {})
        profile_trxs = [trx for trx in trxs if trx.get("TypeUrl") == "quorum.pb.Person"]

        for trx in profile_trxs:
            if "Content" not in trx:
                continue
            pubkey = trx["Publisher"]
            if pubkey not in users:
                users[pubkey] = {}
            for key in trx["Content"]:
                if key in types:
                    users[pubkey].update({key: trx["Content"][key]})
        users_data.update({"data": users, "update_at": str(datetime.datetime.now())})
        return users_data

    def trx_to_newobj(self, trx, nicknames, refer_trx=None, group_id=None):
        """trans from trx to an object of new trx to send to chain.

        Args:
            trx (dict): the trx data
            nicknames (dict): the nicknames data of the group

        Returns:
            obj: object of NewTrx,can be used as: self.send_note(obj=obj).
            result: True,or False, if True, the obj can be send to chain.
        """

        group_id = self.check_group_id_as_required(group_id)
        if "Content" not in trx:
            return None, False

        obj = {"type": "Note", "image": []}
        ttype = trx["TypeUrl"]
        tcontent = trx["Content"]
        lines = []

        if ttype == "quorum.pb.Person":
            _name = "昵称" if "name" in tcontent else ""
            _wallet = "钱包" if "wallet" in tcontent else ""
            _image = "头像" if "image" in tcontent else ""
            _profile = "、".join([i for i in [_name, _image, _wallet] if i])
            lines.append(f"修改了个人信息：{_profile}。")
        elif ttype == "quorum.pb.Object":
            if tcontent.get("type") == "File":
                lines.append(f"上传了文件。")
            else:
                text = trx["Content"].get("content", "")
                img = trx["Content"].get("image", [])
                lines.append(text)
                obj["image"].extend(img)

                t = self.trx_type(trx)
                refer_tid = None
                _info = {"like": "赞", "dislike": "踩"}
                if t == "announce":
                    lines.insert(0, f"处理了链上请求。")
                elif t in _info:
                    refer_tid = trx["Content"]["id"]
                    refer_pubkey = self.trx(refer_tid, group_id).get("Publisher", "")
                    lines.insert(
                        0,
                        f"点{_info[t]}给 `{_nickname( refer_pubkey,nicknames)}` 所发布的内容：",
                    )
                elif t == "reply":
                    lines.insert(0, f"回复说：")
                    refer_tid = trx["Content"]["inreplyto"]["trxid"]
                    refer_pubkey = self.trx(refer_tid, group_id).get("Publisher", "")
                    lines.append(f"\n回复给 `{_nickname(refer_pubkey,nicknames)}` 所发布的内容：")
                else:
                    if text and img:
                        lines.insert(0, f"发布了图片，并且说：")
                    elif img:
                        lines.insert(0, f"发布了图片。")
                    else:
                        lines.insert(0, f"说：")

                if refer_tid:

                    refer_trx = refer_trx or self.trx(refer_tid, group_id)
                    if "Content" in refer_trx:
                        refer_text = refer_trx["Content"].get("content", "")
                        refer_img = refer_trx["Content"].get("image", [])
                        lines.append(_quote(refer_text))
                        obj["image"].extend(refer_img)
        else:
            return None, False

        obj["content"] = f'{timestamp_to_datetime(trx.get("TimeStamp"))}' + " " + "\n".join(lines)
        obj["image"] = obj["image"][:4]
        obj = {key: obj[key] for key in obj if obj[key]}

        return obj, True

    def trx_mode(self, trx_type: str = "POST", group_id=None):
        """获取某个 trx 类型的授权方式

        trx_type: "POST","ANNOUNCE","REQ_BLOCK_FORWARD","REQ_BLOCK_BACKWARD",
            "BLOCK_SYNCED","BLOCK_PRODUCED" 或 "ASK_PEERID"
        """
        group_id = self.check_group_id_as_required(group_id)
        trx_type = _check_trx_type(trx_type)
        return self._get(f"/api/v1/group/{group_id}/trx/auth/{trx_type}")

    @property
    def mode(self):
        """获取所有 trx 类型的授权方式"""
        rlt = {}
        for itype in TRX_TYPES:
            resp = self.trx_mode(itype)
            rlt[resp["TrxType"]] = resp["AuthType"]
        return rlt

    def set_mode(self, mode, group_id=None):
        """将所有 trx 类型设置为一种授权方式

        mode: 授权方式, "follow_alw_list"(白名单方式), "follow_dny_list"(黑名单方式)
        """
        group_id = self.check_group_owner_as_required(group_id)
        mode = _check_mode(mode)
        for itype in TRX_TYPES:
            self.set_trx_mode(itype, mode, f"{itype} set mode to {mode}", group_id=group_id)

    def set_trx_mode(
        self,
        trx_type: str,
        mode: str,
        memo: str = "set trx auth type",
        group_id=None,
    ):
        """设置某个 trx 类型的授权方式

        trx_type: "POST","ANNOUNCE","REQ_BLOCK_FORWARD","REQ_BLOCK_BACKWARD",
            "BLOCK_SYNCED","BLOCK_PRODUCED" 或 "ASK_PEERID"
        mode: 授权方式, "follow_alw_list"(白名单方式), "follow_dny_list"(黑名单方式)
        memo: Memo
        """
        group_id = self.check_group_owner_as_required(group_id)
        mode = _check_mode(mode)

        trx_type = _check_trx_type(trx_type)
        if not memo:
            raise ValueError("say something in param:memo")

        payload = {
            "group_id": group_id,
            "type": "set_trx_auth_mode",
            "config": json.dumps({"trx_type": trx_type, "trx_auth_mode": f"follow_{mode}_list"}),
            "Memo": memo,
        }
        return self._post("/api/v1/group/chainconfig", payload)

    def _update_list(
        self,
        pubkey: str,
        mode: str,
        memo: str = "update list",
        trx_types: List = None,
        group_id=None,
    ):
        group_id = self.check_group_owner_as_required(group_id)
        mode = _check_mode(mode)

        trx_types = trx_types or ["post"]
        for trx_type in trx_types:
            _check_trx_type(trx_type)

        _params = {"action": "add", "pubkey": pubkey, "trx_type": trx_types}
        payload = {
            "group_id": group_id,
            "type": f"upd_{mode}_list",
            "config": json.dumps(_params),
            "Memo": memo,
        }
        return self._post("/api/v1/group/chainconfig", payload)

    def update_allow_list(
        self,
        pubkey: str,
        memo: str = "update allow list",
        trx_types: List = None,
        group_id=None,
    ):
        """将某个用户加入某个/某些 trx 类型的白名单中

        pubkey: 用户公钥
        memo: Memo
        trx_types: Trx 类型组成的列表, Trx 类型有 "POST","ANNOUNCE",
            "REQ_BLOCK_FORWARD","REQ_BLOCK_BACKWARD",
            "BLOCK_SYNCED","BLOCK_PRODUCED" 或 "ASK_PEERID"
        """
        group_id = self.check_group_owner_as_required(group_id)
        return self._update_list(pubkey, "alw", memo, trx_types, group_id)

    def update_deny_list(
        self,
        pubkey: str,
        memo: str = "update deny list",
        trx_types: List = None,
        group_id=None,
    ):
        """将某个用户加入某个/某些 trx 类型的黑名单中

        pubkey: 用户公钥
        memo: Memo
        trx_types: Trx 类型组成的列表, Trx 类型有 "POST","ANNOUNCE",
            "REQ_BLOCK_FORWARD","REQ_BLOCK_BACKWARD",
            "BLOCK_SYNCED","BLOCK_PRODUCED" 或 "ASK_PEERID"
        """
        group_id = self.check_group_owner_as_required(group_id)
        return self._update_list(pubkey, "dny", memo, trx_types, group_id)

    def _list(self, mode: str, group_id=None) -> List:
        if mode not in ["allow", "deny"]:
            raise ValueError("mode must be one of these: allow,deny")
        group_id = self.check_group_id_as_required(group_id)
        return self._get(f"/api/v1/group/{group_id}/trx/{mode}list") or []

    @property
    def allow_list(self):
        """获取某个组的白名单"""
        return self._list("allow")

    @property
    def deny_list(self):
        """获取某个组的黑名单"""
        return self._list("deny")

    def get_allow_list(self, group_id=None):
        """获取某个组的白名单"""
        return self._list("allow", group_id)

    def get_deny_list(self, group_id=None):
        """获取某个组的黑名单"""
        return self._list("deny", group_id)

    def group_icon(self, file_path: str):
        """将一张图片处理成组配置项 value 字段的值, 例如组的图标对象"""

        img_bytes = zip_image_file(file_path)
        icon = f'data:{filetype.guess(img_bytes).mime}base64,{base64.b64encode(img_bytes).decode("utf-8")}'

        return icon

    def set_appconfig(
        self,
        name="group_desc",
        the_type="string",
        value="增加组的简介",
        action="add",
        image=None,
        memo="add",
        group_id=None,
    ):
        """组创建者更新组的某个配置项

        name: 配置项的名称, 自定义, 以 rum-app 为例, 目前支持 'group_announcement'(组的公告),
            'group_desc'(组的简介),'group_icon'(组的图标), 均是 "string" 类型
        the_type: 配置项的类型, 可选值为 "int", "bool", "string"
        value: 配置项的值, 必须与 type 相对应
        action: "add" 或 "del", 增加/修改 或 删除
        image: 一张图片路径, 如果提供, 将转换为 value 的值,
            例如 rum-app 用作组的图标(需要 name 是 'group_icon')
        memo: Memo
        """
        group_id = self.check_group_owner_as_required(group_id)
        if image is not None:
            value = self.group_icon(image)
        payload = {
            "action": action,
            "group_id": group_id,
            "name": name,
            "type": the_type,
            "value": value,
            "memo": memo,
        }

        return self._post("/api/v1/group/appconfig", payload)

    def keylist(self, group_id=None):
        """获取组的所有配置项"""
        group_id = self.check_group_id_as_required(group_id)
        return self._get(f"/api/v1/group/{group_id}/appconfig/keylist")

    def key(self, key: str, group_id=None):
        """获取组的某个配置项的信息

        key: 配置项名称
        """
        group_id = self.check_group_id_as_required(group_id)
        return self._get(f"/api/v1/group/{group_id}/appconfig/{key}")

    def announce(self, action="add", type="user", memo="rumpy.api", group_id=None):
        """announce user or producer,add or remove

        申请 成为/退出 producer/user

        action: "add" 或 "remove", 申请成为/宣布退出
        type: "user" 或 "producer"
        memo: Memo
        """
        group_id = self.check_group_id_as_required(group_id)
        payload = {
            "group_id": group_id,
            "action": action,  # add or remove
            "type": type,  # user or producer
            "memo": memo,
        }
        return self._post("/api/v1/group/announce", payload)

    def announce_as_user(self, group_id=None):
        """announce self as user

        申请成为私有组用户

        如果已经是用户, 返回申请状态
        """
        status = self.announced_user(self.pubkey)
        if status.get("Result") == "APPROVED":
            return status
        return self.announce("add", "user", "rumpy.api,announce self as user", group_id)

    def announce_as_producer(self, group_id=None):
        """announce self as producer"""
        return self.announce("add", "producer", "rumpy.api,announce self as producer", group_id)

    def announced_producers(self, group_id=None):
        """获取申请 成为/退出 的 producers"""
        group_id = self.check_group_id_as_required(group_id)
        return self._get(f"/api/v1/group/{group_id}/announced/producers")

    def announced_users(self, group_id=None):
        """获取申请 成为/退出 的 users"""
        group_id = self.check_group_id_as_required(group_id)
        return self._get(f"/api/v1/group/{group_id}/announced/users")

    def announced_user(self, pubkey, group_id=None):
        """获取申请 成为/退出 的 user 的申请状态

        pubkey: 用户公钥
        """
        group_id = self.check_group_id_as_required(group_id)
        return self._get(f"/api/v1/group/{group_id}/announced/user/{pubkey}")

    def producers(self, group_id=None):
        """获取已经批准的 producers"""
        group_id = self.check_group_id_as_required(group_id)
        return self._get(f"/api/v1/group/{group_id}/producers")

    def update_user(self, pubkey, action="add", group_id=None):
        """组创建者添加或移除私有组用户

        action: "add" or "remove"
        """
        group_id = self.check_group_owner_as_required(group_id)
        payload = {
            "user_pubkey": pubkey,
            "group_id": group_id,
            "action": action,  # "add" or "remove"
        }
        return self._post("/api/v1/group/user", payload)

    def approve_as_user(self, pubkey=None, group_id=None):
        """approve pubkey as a user of group.

        pubkey: 用户公钥, 如果不提供该参数, 默认将 owner 自己添加为私有组用户
        """
        return self.update_user(pubkey=pubkey or self.pubkey, group_id=group_id)

    def update_producer(self, pubkey=None, group_id=None, action="add"):
        """Only group owner can update producers: add, or remove.

        pubkey: the producer's pubkey
        action: "add" or "remove"
        """
        group_id = self.check_group_owner_as_required(group_id)
        action = action.lower()
        if action not in ("add", "remove"):
            raise ValueError("action should be `add` or `remove`")
        payload = {
            "producer_pubkey": pubkey,
            "group_id": group_id,
            "action": action,
        }
        return self._post("/api/v1/group/producer", payload)

    def update_profile(self, name, image=None, mixin_id=None, group_id=None):
        """user update the profile: name, image, or wallet.

        name: nickname of user
        image: image file_path
        mixin_id: one kind of wallet
        """
        group_id = self.check_group_joined_as_required(group_id)
        if image is not None:
            image = NewTrxImg(file_path=image).__dict__
        payload = {
            "type": "Update",
            "person": {"name": name, "image": image},
            "target": {"id": group_id, "type": "Group"},
        }
        if mixin_id is not None:
            payload["person"]["wallet"] = {
                "id": mixin_id,
                "type": "mixin",
                "name": "mixin messenger",
            }
        return self._post("/api/v1/group/profile", payload)
