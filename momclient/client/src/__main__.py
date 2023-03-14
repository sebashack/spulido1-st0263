import uuid
import asyncio
import logging

import grpc
import messages_pb2
import messages_pb2_grpc


async def run() -> None:
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = messages_pb2_grpc.MessageStreamStub(channel)

        message_stream = stub.ConnectToChannel(messages_pb2.ConnectionRequest(queue_label="q1", channel_id=str(uuid.uuid4())))
        while True:
            res = await message_stream.read()
            if res == grpc.aio.EOF:
                break
            print(f"Message client received from direct read: {(res.message_id, res.topic)}")


if __name__ == "__main__":
    logging.basicConfig()
    asyncio.run(run())
