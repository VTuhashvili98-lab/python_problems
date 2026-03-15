"""
Столбец RSS показывает информацию о потребляемой памяти в килобайтах.

Напишите функцию get_summary_rss, которая на вход принимает путь до файла с результатом выполнения команды ps aux,
а возвращает суммарный объём потребляемой памяти в человекочитаемом формате.
Это означает, что ответ надо перевести в байты, килобайты, мегабайты и так далее.
"""

import os


UNITS = ["KB", "MB", "GB", "TB"]


def normalize_size(size: float) -> str:

    """ Transforms 'size' to human-readable format."""

    for unit in UNITS:
        if size < 1024:
            return f"{size:.1f}{unit}"
        size /= 1024

    return f"{size:.1f}{UNITS[-1]}"


path = os.path.join(os.path.dirname(__file__), "output.txt")


def get_summary_rss(path_to_file: str) -> str:

    """ Counts total rss of file
    and returns human-readable format"""

    with open(path_to_file, "r", encoding="utf-8") as file:
        next(file)

        total = 0
        for line in file:
            parts = line.split()
            if len(parts) > 5:
                total += int(parts[5])

    return normalize_size(total)

print(get_summary_rss(path_to_file=path))