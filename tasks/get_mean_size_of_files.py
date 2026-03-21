"""
Удобно направлять результат выполнения команды напрямую в программу с помощью конвейера (pipe):

$ ls -l | python3 get_mean_size.py

Напишите функцию get_mean_size, которая на вход принимает результат выполнения команды ls -l,
а возвращает средний размер файла в каталоге.
"""

import sys


def get_mean_size(output: list[str]) -> float:
    total_size = 0
    lines_count = 0

    for line in output[1:]:
        parts = line.split()
        if len(parts) > 4 and parts[0].startswith("-"):
            total_size += int(parts[4])
            lines_count += 1

    if lines_count == 0:
        return 0.0

    return round(total_size / lines_count, 1)


if __name__ == "__main__":
    lines = sys.stdin.readlines()
    result = get_mean_size(lines)
    print(result)
