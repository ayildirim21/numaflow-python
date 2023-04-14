from datetime import datetime, timezone
from typing import Iterator, List

from pynumaflow.function import (
    Message,
    Messages,
    MessageT,
    MessageTs,
    Datum,
    Metadata,
)


def map_handler(keys: List[str], datum: Datum) -> Messages:
    val = datum.value
    msg = "payload:%s event_time:%s watermark:%s" % (
        val.decode("utf-8"),
        datum.event_time,
        datum.watermark,
    )
    val = bytes(msg, encoding="utf-8")
    messages = Messages()
    messages.append(Message(val, keys=keys))
    return messages


def mapt_handler(keys: List[str], datum: Datum) -> MessageTs:
    val = datum.value
    msg = "payload:%s event_time:%s watermark:%s" % (
        val.decode("utf-8"),
        datum.event_time,
        datum.watermark,
    )
    val = bytes(msg, encoding="utf-8")
    messagets = MessageTs()
    messagets.append(MessageT(val, mock_new_event_time(), keys=keys))
    return messagets


async def reduce_handler(keys: List[str], datums: Iterator[Datum], md: Metadata) -> Messages:
    interval_window = md.interval_window
    counter = 0
    async for _ in datums:
        counter += 1
    msg = (
        f"counter:{counter} interval_window_start:{interval_window.start} "
        f"interval_window_end:{interval_window.end}"
    )
    return Messages(Message(str.encode(msg), keys=keys))


def err_map_handler(_: str, __: Datum) -> Messages:
    raise RuntimeError("Something is fishy!")


def err_mapt_handler(_: str, __: Datum) -> MessageTs:
    raise RuntimeError("Something is fishy!")


def mock_message():
    msg = bytes("test_mock_message", encoding="utf-8")
    return msg


def mock_event_time():
    t = datetime.fromtimestamp(1662998400, timezone.utc)
    return t


def mock_new_event_time():
    t = datetime.fromtimestamp(1663098400, timezone.utc)
    return t


def mock_watermark():
    t = datetime.fromtimestamp(1662998460, timezone.utc)
    return t


def mock_interval_window_start():
    return 1662998400000


def mock_interval_window_end():
    return 1662998460000