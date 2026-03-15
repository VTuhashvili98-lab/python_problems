"""
Столбец RSS показывает информацию о потребляемой памяти в байтах.

Напишите функцию get_summary_rss, которая на вход принимает путь до файла с результатом выполнения команды ps aux,
а возвращает суммарный объём потребляемой памяти в человекочитаемом формате.
Это означает, что ответ надо перевести в байты, килобайты, мегабайты и так далее.
"""

import os


def normalize_size(size: float, depth: int = 0) -> str:

    """ Function which transforms 'size' of file in normal for human format."""

    if size < 1024:
        return f"{round(size, 1)}{DEPTHS[depth]}"

    return normalize_size(size / 1024, depth + 1)

DEPTHS = {
    0: "B",
    1: "KB",
    2: "MB",
    3: "GB",
    4: "TB",
    5: "PB"
}

path = os.path.join(os.path.dirname(__file__), "output.txt")


def get_summary_rss(path_to_file: str) -> str:

    """ Function which counts total rss of file
          and returns it in normal format"""

    total_size: float = 0

    with open(path_to_file, "r", encoding="utf-8") as file:

        next(file)

        for line in file:
            parts = line.split()
            try:
                size = float(parts[5])
                total_size += size
            except (IndexError, ValueError):
                continue

    return normalize_size(total_size)