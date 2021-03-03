import hashlib
from datetime import datetime
from time import sleep

import slackweb
from pytz import timezone
from slack_sdk import WebClient

from config.secret.const import BOT_TOKEN, SLACK_HOOK


## incomming web hook(SLACK_HOOKはincoming hookのURL)の使い方 https://qiita.com/vmmhypervisor/items/18c99624a84df8b31008
def send_message(message, parent_ts=None):
    slack = slackweb.Slack(url=SLACK_HOOK)
    if parent_ts is not None:
        return slack.notify(text=message, mrkdwn_in=["text"], thread_ts=parent_ts)
    return slack.notify(text=message, mrkdwn_in=["text"])


class SlackManager:
    """
    Slack上に実験状況をログ.
    ログしたい実験状況.
    - [x] サーバ名
    - [x] GPU名
    - [x] 実験初期設定(なんのモデルを使ってるのか? なんの実験か)
    - [x] 実験開始時間
    - [x] 実験終了時間
    - [x] 実験状況(1epoch毎の過程)
    """
    def __init__(self,
                 experiment_name,
                 server_name="",
                 gpu_name=""):
        self.initial_date = datetime.now(timezone("Asia/Tokyo"))
        self.experiment_name = experiment_name
        self.server_name = server_name if server_name != "" else "laptop"
        self.gpu_name = gpu_name if gpu_name != "" else "cpu"
        unique = experiment_name + str(self.initial_date)
        self.parent_thread_timestamp = None
        self.hash = str(hashlib.md5(unique.encode()).hexdigest())
        initialize_message = """BEGINING: {experiment_name} on {server_name} {gpu_name}
INIT AT: {initial_date}
HASH(exp + init_date): {hash}"""
        initialize_message = initialize_message.format(experiment_name=self.experiment_name,
                                                       server_name=self.server_name,
                                                       gpu_name=self.gpu_name,
                                                       initial_date=self.initial_date,
                                                       hash=self.hash)
        self._send(initialize_message)

        client = WebClient(token=BOT_TOKEN)
        channel_cond = "in:z_tm_otter"
        for i in range(5):
            sleep(10)
            result = client.search_messages(query=channel_cond + " " + self.hash, count=1, sort="timestamp", sort_dir="asc")
            thread_ts = result.data["messages"]["matches"]
            if len(thread_ts) != 0:
                thread_ts = thread_ts[0]["ts"]
                self.parent_thread_timestamp = thread_ts
                break

    def send_message(self, message):
        now = datetime.now(timezone("Asia/Tokyo")).strftime('%y/%m/%d %H:%M')
        if not isinstance(message, str):
            try:
                message = str(message)
            except:
                self._send("illegal message type.")
        message = " ".join([self.hash, now, message])
        self._send(message)

    def halt(self):
        self.send_message("The fourth studio album by Kendrick Lamar.")

    def _send(self, message):
        try:
            result = send_message(message, parent_ts=self.parent_thread_timestamp)
        except:
            pass

if __name__ == '__main__':
    slack_manager = SlackManager("test")
    slack_manager.send_message("**Hold on, Hold on**")
    slack_manager.halt()
