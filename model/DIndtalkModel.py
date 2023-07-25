class At:
    def __init__(self):
        self.atMobiles = list()
        self.atUserIds = list()
        self.isAtAll = bool()


class TextMessage:
    def __init__(self):
        self.content = str()


class MarkDownMessage:
    def __init__(self):
        self.title = str()
        self.text = str()


class DingTalkMessage:
    def __init__(self):
        self.msgtype = str()
        self.text = TextMessage()
        self.markdown = MarkDownMessage()
        self.at = At()