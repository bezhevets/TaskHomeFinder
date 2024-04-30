import functools
import json
import logging
import os
import sys
import time
from dataclasses import asdict
from typing import Callable, Any

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"


def time_counter(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        print("========Start script========")
        start = time.perf_counter()
        func(*args, **kwargs)
        duration = time.perf_counter() - start
        print(f"========Duration: {round(duration, 2)} seconds========")
        print("========Finish script========")

    return wrapper


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s]: %(message)s",
        handlers=[
            logging.FileHandler(os.path.join("data", "log.log"), mode="w"),
            logging.StreamHandler(sys.stdout),
        ],
    )


def save_data_to_json(list_data: list, json_path: str) -> None:

    data = [asdict(data_obj) for data_obj in list_data]

    with open(os.path.join("results", json_path), "w") as json_file:
        json.dump(data, json_file, indent=2)
