from concurrent import futures
import asyncio
import grpc
import logging
import sys

import file_service_pb2
import file_service_pb2_grpc

class FileService(file_service_pb2_grpc.FileService):
    def ListFiles(self, request, context):
        print(f"Limit: {request.limit}")
        return file_service_pb2.FilesReply(file_list=f"foo.txt\nbar.txt\n")

    def SearchFiles(self, request, context):
        print(f"Limit: {request.limit}")
        print(f"Pattern: {request.pattern}")
        return file_service_pb2.FilesReply(file_list=f"foo.txt\nbar.txt\n")


def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    file_service_pb2_grpc.add_FileServiceServicer_to_server(FileService(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


def main(argv):
    logging.basicConfig()
    serve()


if __name__ == "__main__":
    main(sys.argv[1:])
