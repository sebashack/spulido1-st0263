import file_service_pb2
import file_service_pb2_grpc
import grpc
import json


def list(addr, limit=None):
    with grpc.insecure_channel(addr) as channel:
        stub = file_service_pb2_grpc.FileServiceStub(channel)
        res = stub.ListFiles(file_service_pb2.ListFilesRequest(limit=limit))
        result = json.loads(res.file_list)
        result["status"] = 200

        return result


def search(addr, pattern, limit=None):
    with grpc.insecure_channel(addr) as channel:
        stub = file_service_pb2_grpc.FileServiceStub(channel)
        res = stub.SearchFiles(
            file_service_pb2.SearchFilesRequest(pattern=pattern, limit=limit)
        )
        result = json.loads(res.file_list)
        result["status"] = 200

        return result
