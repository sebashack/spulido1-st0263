from concurrent import futures
import argparse
import file_service_pb2
import file_service_pb2_grpc
import glob
import grpc
import json
import logging
import os
import pathlib
import sys


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


def serve(port, dir_path, workers):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=workers))
    file_service_pb2_grpc.add_FileServiceServicer_to_server(
        FileService(dir_path), server
    )
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"Server started, listening on {port}")
    server.wait_for_termination()


def main(argv):
    parser = argparse.ArgumentParser(description="File service API gateway")

    parser.add_argument("config", type=str, help="Path to config file")

    args = parser.parse_args(argv[1:])

    config_path = args.config
    conf = json.loads(open(config_path, "r").read())

    serve(conf['port'], conf['dir_path'], conf['max_workers'])


if __name__ == "__main__":
    main(sys.argv)
