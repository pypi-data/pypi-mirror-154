# -----------------------------------------------------------------------------
# Header类型
# client protocol初始化连接的时候发送的信息，信息符合Header协议。
# MsgType代码：H
# 内容样例：
#  {'header':"XXXX"}
# fields中key的取值为：'header'。
HEADER_META = [0x48, "H"]
HEADER_INDEX = b"\x01\x00"
HEADER_FIELD_MAP = {HEADER_INDEX: "header"}
HEADER_REVERSE_FIELD_MAP = {v: k for k, v in HEADER_FIELD_MAP.items()}


# -----------------------------------------------------------------------------
# StdOut类型
# client protocol的stdout有新内容时，发送的消息，信息符合Message协议。
# MsgType代码：O
# 内容样例：
# "XXXX"
STDOUT_META = [0x4F, "O"]

# -----------------------------------------------------------------------------
# StdErr类型
# client protocol的stderr有新内容时，发送的消息，信息符合Message协议。
# MsgType代码：E
# 内容样例：
# "XXXX"
STDERR_META = [0x45, "E"]

# -----------------------------------------------------------------------------
# SubTaskUpdate类型
# client protocol的子作业全量初始化时，发送的消息，信息符合Header协议。
# MsgType代码：U
# 内容样例：
# {'key':'xxx','status':'GO','endTime':None}
# fields中key的取值为：'key'、'status'、'endTime'。
SUBTASKUPDATE_META = [0x55, "U"]
KEY_INDEX = b"\x01\x00"
STATUS_INDEX = b"\x02\x00"
ENDTIME_INDEX = b"\x03\x00"
NAME_INDEX = b"\x04\x00"
SUBTASKUPDATE_FIELD_MAP = {
    KEY_INDEX: "key",
    STATUS_INDEX: "status",
    ENDTIME_INDEX: "endTime",
    NAME_INDEX: "name",
}
SUBTASKUPDATE_REVERSE_FIELD_MAP = {
    v: k for k, v in SUBTASKUPDATE_FIELD_MAP.items()
}

# -----------------------------------------------------------------------------
# SubTaskInit类型
# client protocol的子作业全量初始化时，发送的消息，信息符合DetailList协议。
# MsgType代码：I
# 内容样例：
# [{'key':'xxx','name':'xxxx'},....]
# elements的每一个成员的value(Field类型)的key取值情况为：'key'、'name'。
SUBTASKINIT_META = [0x49, "I"]
SUB_KEY_INDEX = b"\x01\x00"
SUB_NAME_INDEX = b"\x02\x00"
SUBTASKINIT_FIELD_MAP = {
    SUB_KEY_INDEX: "key",
    SUB_NAME_INDEX: "name",
}
SUBTASKINIT_REVERSE_FIELD_MAP = {
    v: k for k, v in SUBTASKINIT_FIELD_MAP.items()
}

HEADER_PROTOCOL = sum([HEADER_META], [])
MESSAGE_PROTOCOL = sum([STDERR_META, STDOUT_META], [])
DETAILLIST_PROTOCOL = sum([SUBTASKINIT_META, SUBTASKUPDATE_META], [])
