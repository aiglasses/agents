# -*- encoding: utf-8 -*-
import sys
from loguru import logger
from pathlib import Path


_FORMAT = "{time: YYYY-MM-DD HH:mm:ss} | {name}:{function}:{line} - {level} - {message}"
root_path = Path(__file__).parent.absolute()
sys.path.insert(0, str(root_path))


def _add_log_config(
        level: str = "INFO",
        log_format: str = _FORMAT,
        enqueue: bool = True,
        retention: str = "5 days",
        rotation: str = "12:00",
        sink: Path = Path(root_path, "logs/app_{time: YYYY-MM-DD}.log"),
        catch: bool = True,
        log_split_by_level: bool = True
) -> None:
    logger.remove(0)
    logger.add(sys.stderr, level="DEBUG", format=log_format)
    if not log_split_by_level:
        logger.add(sink=sink, level=level, format=log_format, enqueue=enqueue, retention=retention, rotation=rotation,
                   catch=catch)
    else:
        logger.add(Path(sink.parent, "debug_{time}.log"), level="DEBUG", format=log_format, enqueue=enqueue,
                   retention=retention, rotation=rotation, catch=catch,
                   filter=lambda record: record["level"].name == "DEBUG")
        logger.add(Path(sink.parent, "info_{time}.log"), level="INFO", format=log_format, enqueue=enqueue,
                   retention=retention, rotation=rotation, catch=catch,
                   filter=lambda record: record["level"].name == "INFO")
        logger.add(Path(sink.parent, "warning_{time}.log"), level="WARNING", format=log_format, enqueue=enqueue,
                   retention=retention, rotation=rotation, catch=catch,
                   filter=lambda record: record["level"].name == "WARNING")
        logger.add(Path(sink.parent, "error_{time}.log"), level="ERROR", format=log_format, enqueue=enqueue,
                   retention=retention, rotation=rotation, catch=catch,
                   filter=lambda record: record["level"].name == "ERROR")
        logger.add(Path(sink.parent, "critical_{time}.log"), level="CRITICAL", format=log_format, enqueue=enqueue,
                   retention=retention, rotation=rotation, catch=catch,
                   filter=lambda record: record["level"].name == "CRITICAL")


_add_log_config(log_split_by_level=False)
