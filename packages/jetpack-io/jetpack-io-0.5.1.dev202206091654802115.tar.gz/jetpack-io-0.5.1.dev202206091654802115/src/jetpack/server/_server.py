import asyncio
from typing import Any, Optional, Tuple, Type

from jetpack.config import _symbols
from jetpack.core._jetpack_function import JetpackFunction
from jetpack.proto.runtime.v1alpha1 import jetworker_pb2, jetworker_pb2_grpc


class JetworkerServicer(jetworker_pb2_grpc.JetworkerServicer):

    # Need to figure out grpc request types
    def StartJetroutine(
        self, request: jetworker_pb2.StartJetroutineRequest, context: Any
    ) -> jetworker_pb2.StartJetroutineResponse:
        func = _symbols.get_symbol_table().get_registered_symbols()[
            request.qualified_symbol
        ]

        args = b""
        if request.encoded_args:
            args = request.encoded_args.encode()
        asyncio.run(JetpackFunction(func).exec(request.exec_id, args))
        return jetworker_pb2.StartJetroutineResponse()
