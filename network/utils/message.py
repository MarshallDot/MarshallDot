import zlib


def compress_message(msg: bytes) -> bytes:
    objj = zlib.compressobj()
    msg: bytes = objj.compress(msg)

    return msg
