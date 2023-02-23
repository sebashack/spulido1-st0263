import file_service_pb2
import file_service_pb2_grpc
import grpc


def list(addr, limit=None):
    with grpc.insecure_channel(addr) as channel:
        stub = file_service_pb2_grpc.FileServiceStub(channel)
        res = stub.ListFiles(file_service_pb2.ListFilesRequest(limit=limit))
        return res.file_list


def search(addr, pattern, limit=None):
    with grpc.insecure_channel(addr) as channel:
        stub = file_service_pb2_grpc.FileServiceStub(channel)
        res = stub.SearchFiles(
            file_service_pb2.SearchFilesRequest(pattern=pattern, limit=limit)
        )
        return res.file_list
