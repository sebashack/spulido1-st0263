# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import file_service_pb2 as file__service__pb2


class FileServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ListFiles = channel.unary_unary(
                '/fileservice.FileService/ListFiles',
                request_serializer=file__service__pb2.ListFilesRequest.SerializeToString,
                response_deserializer=file__service__pb2.FilesReply.FromString,
                )
        self.SearchFiles = channel.unary_unary(
                '/fileservice.FileService/SearchFiles',
                request_serializer=file__service__pb2.SearchFilesRequest.SerializeToString,
                response_deserializer=file__service__pb2.FilesReply.FromString,
                )


class FileServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ListFiles(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SearchFiles(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_FileServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ListFiles': grpc.unary_unary_rpc_method_handler(
                    servicer.ListFiles,
                    request_deserializer=file__service__pb2.ListFilesRequest.FromString,
                    response_serializer=file__service__pb2.FilesReply.SerializeToString,
            ),
            'SearchFiles': grpc.unary_unary_rpc_method_handler(
                    servicer.SearchFiles,
                    request_deserializer=file__service__pb2.SearchFilesRequest.FromString,
                    response_serializer=file__service__pb2.FilesReply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'fileservice.FileService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class FileService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ListFiles(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/fileservice.FileService/ListFiles',
            file__service__pb2.ListFilesRequest.SerializeToString,
            file__service__pb2.FilesReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SearchFiles(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/fileservice.FileService/SearchFiles',
            file__service__pb2.SearchFilesRequest.SerializeToString,
            file__service__pb2.FilesReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)