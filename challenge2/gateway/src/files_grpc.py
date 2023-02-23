import file_service_pb2
import file_service_pb2_grpc
import grpc


def list(addr):
    with grpc.insecure_channel(addr) as channel:
        stub = file_service_pb2_grpc.FileServiceStub(channel)
        res = stub.ListFiles(file_service_pb2.ListFilesRequest(limit=100))
        return res.file_list


def search(addr):
    with grpc.insecure_channel(addr) as channel:
        stub = file_service_pb2_grpc.FileServiceStub(channel)
        res = stub.SearchFiles(
            file_service_pb2.SearchFilesRequest(limit=50, pattern="*.txt")
        )
        return res.file_list
