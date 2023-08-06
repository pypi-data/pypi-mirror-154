import asyncio

from deepfos_ipc_protocol.const import MESSAGE_PROTOCOL, HEADER_PROTOCOL, DETAILLIST_PROTOCOL
from deepfos_ipc_protocol.utils import (
    judge_data_format,
    to_msg_protocol,
    to_header_protocol,
    to_detaillist_protocol,
    logging
)


logger = logging.getLogger(__name__)


class ClientProtocol(asyncio.Protocol):

    def __init__(self, ins):
        self.ins = ins

    def connection_made(self, transport):
        logger.debug("Connection made")
        self.transport = transport

    def data_received(self, data):
        if data == b"end":
            self.transport.close()
        if data and not self.ins.future.done():
            self.ins.future.set_result(data)
        logger.debug("Data received: {!r}".format(data.decode()))

    def connection_lost(self, error):
        if error:
            logger.error('ERROR: {}'.format(error))
        else:
            logger.debug('The server closed the connection')


class WorkerClient:

    transport = None
    path = None

    def __new__(cls, path=None):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, path: str = None):
        if not self.path:
            self.path = path
        if self.path is None:
            raise Exception("path is not None")

    def _processing_data(self, mtype: str, data):
        '''将传入的数据转为服务端可读取的数据'''
        if mtype in MESSAGE_PROTOCOL:
            buf = to_msg_protocol(mtype, data)
        elif mtype in HEADER_PROTOCOL:
            buf = to_header_protocol(mtype, data)
        elif mtype in DETAILLIST_PROTOCOL:
            buf = to_detaillist_protocol(mtype, data)
        else:
            raise ValueError("Unsupported message type: {}".format(mtype))
        return buf

    async def create_conn(self):
        '''建立和服务端的连接'''
        loop = asyncio.get_running_loop()
        if not self.transport or self.transport.is_closing():
            transport, protocol = await loop.create_unix_connection(
                lambda: ClientProtocol(self), self.path
            )
            self.transport = transport

    @classmethod
    async def send_msg(cls, mtype, message):
        '''向服务端发送数据'''
        loop = asyncio.get_running_loop()
        judge_data_format(mtype, message)
        cls.future = loop.create_future()
        data = cls._instance._processing_data(mtype, message)
        cls._instance.transport.write(data)
        return await cls.future

    @classmethod
    async def close(cls):
        loop = asyncio.get_running_loop()
        cls.future = loop.create_future()
        cls._instance.transport.write(b'end')
        await cls.future
        cls._instance.transport.close()

# async def async_main():
#     m = WorkerClient("../unix_sock.sock")
#     await m.create_conn() # 建立一个连接
#     await m.send_msg("O", "你好")

#     await WorkerClient.send_msg(
#         "U", [
#             {
#                 "key": "key",
#                 "name": "你好",
#                 "status": "status",
#                 "endTime": "endTime",
#                 "arg": "xxxx"
#             }
#         ]
#     )
#     await WorkerClient.send_msg(
#         "H", {"header": "你好"}
#     )
#     await WorkerClient.send_msg(
#         "I", [
#             {
#                 "key": "key",
#                 "name": "name",
#             }
#         ]
#     )
#     await WorkerClient.send_msg(
#         "E", "xxxss"
#     )
#     await WorkerClient.send_msg(
#         "e", {"subtask_err": "err", "arg": "arg"}
#     )
#     await WorkerClient.send_msg(
#         "o", {"subtask_out": "out", "arg": "arg"}
#     )
#     await m.close()
#     await m.send_msg("O", "hello3")

# asyncio.run(async_main())
