import json
import os
import uuid

import requests


class Feishu:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.base = "https://open.feishu.cn/open-apis"
        r = requests.post(self.base + "/auth/v3/tenant_access_token/internal", timeout=20,
            json={"app_id": os.environ["FEISHU_APP_ID"], "app_secret": os.environ["FEISHU_APP_SECRET"]})
        self.token = self.check(r)["tenant_access_token"]

    @staticmethod
    def check(response):
        data = response.json()
        if not response.ok:
            raise RuntimeError(f"Feishu HTTP {response.status_code}, API code {data.get('code')}: {str(data.get('msg', ''))[:200]}")
        if data.get("code") != 0:
            raise RuntimeError(f"Feishu API code {data.get('code')}")
        return data

    def send(self, key, kind, content):
        r = requests.post(self.base + "/im/v1/messages", params={"receive_id_type": "chat_id"},
            headers={"Authorization": "Bearer " + self.token}, timeout=30,
            json={"receive_id": self.chat_id, "msg_type": kind,
                  "content": json.dumps(content, ensure_ascii=False),
                  "uuid": str(uuid.uuid5(uuid.NAMESPACE_URL, key))})
        return self.check(r)["data"]["message_id"]

    def card(self, key, title, markdown):
        return self.send(key, "interactive", {
            "config": {"wide_screen_mode": True},
            "header": {"template": "blue", "title": {"tag": "plain_text", "content": title}},
            "elements": [{"tag": "markdown", "content": markdown[:12000]}]})

    def file(self, key, path):
        with path.open("rb") as f:
            r = requests.post(self.base + "/im/v1/files", timeout=(15, 120),
                headers={"Authorization": "Bearer " + self.token},
                data={"file_type": "stream", "file_name": path.name}, files={"file": f})
        file_key = self.check(r)["data"]["file_key"]
        return self.send(key, "file", {"file_key": file_key})
