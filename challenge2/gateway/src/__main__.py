import grpc
import logging
import sys

import file_service_pb2
import file_service_pb2_grpc


def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = file_service_pb2_grpc.FileServiceStub(channel)
        res0 = stub.ListFiles(file_service_pb2.ListFilesRequest(limit=100))
        print("ListFiles -- received: \n" + res0.file_list)

        res1 = stub.SearchFiles(file_service_pb2.SearchFilesRequest(limit=50, pattern="*.txt"))
        print("SearchFiles -- received: \n" + res1.file_list)


def main(argv):
    logging.basicConfig()
    run()


if __name__ == "__main__":
    main(sys.argv[1:])
