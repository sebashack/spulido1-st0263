from concurrent import futures
import os
import logging
import grpc
import glob
import pathlib
import json

import file_service_pb2
import file_service_pb2_grpc


class FileService(file_service_pb2_grpc.FileService):
    logger = None
    dir_papth = None

    def __init__(self, dir_path):
        FORMAT = "%(asctime)s -- %(message)s"
        logging.basicConfig(
            format=FORMAT, level=logging.INFO, datefmt="%Y-%m-%d %H:%M:%S"
        )
        self.logger = logging.getLogger("grpc-server")
        self.dir_path = dir_path

    def ListFiles(self, req, context):
        self.logger.info(f"New list request, limit={req.limit}")
        result = self.list_files(limit=req.limit)
        return file_service_pb2.FilesReply(file_list=json.dumps(result))

    def SearchFiles(self, req, context):
        self.logger.info(
            f"New search request, limit={req.limit}, pattern={req.pattern}"
        )
        result = self.list_files(req.pattern, req.limit)
        return file_service_pb2.FilesReply(file_list=json.dumps(result))

    def list_files(self, pattern="*", limit=None):
        files = list(
            map(lambda p: str(p), pathlib.Path(self.dir_path).glob("**/" + pattern))
        )
        if limit < 1 or limit is None:
            return {"found": len(files), "files": files}
        else:
            return {"found": len(files), "files": files[:limit]}


def serve(port, dir_path):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    file_service_pb2_grpc.add_FileServiceServicer_to_server(
        FileService(dir_path), server
    )
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


def main():
    port = "50051"
    dir_path = "/home/sebastian/univeristy/networking/spulido1-st0263/challenge2"
    serve(port, dir_path)


if __name__ == "__main__":
    main()
