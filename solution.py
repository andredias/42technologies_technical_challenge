import csv
import sys
from pathlib import Path

DELIMITER = '|'


def hierarchical_sort(rows: list, metric: str, reverse=True) -> list:
    header = rows[0]
    metric_index = header.index(metric)
    partial_rows = partial_hierachical_sort(rows, metric, reverse)
    stack = []
    intervals = []

    def handle_interval(totals: int, metric_value: float, line: int) -> None:
        while len(stack) and stack[-1][0] <= totals:
            interval = stack.pop()
            interval[2] = slice(interval[2], line)
            intervals.append(interval)
        stack.append([totals, metric_value, line])

    for line, row in enumerate(partial_rows):
        totals = row.count('$total')
        if totals:
            handle_interval(totals, float(row[metric_index]), line)
    handle_interval(2 ** 10, 0, line)  # empty remaining intervals

    return partial_rows


def partial_hierachical_sort(rows: list, metric: str, reverse=True) -> list:
    header = rows[0]
    metric_index = header.index(metric)
    p_index = max(i for i, name in enumerate(rows[0]) if name.startswith('property'))

    def _sort_func(row: list) -> list:
        result = (
            [(int(row[i] == '$total'), row[i]) for i in range(p_index)] +
            [(int(row[p_index] == '$total'), float(row[metric_index]))]
        )
        return result

    return [header] + sorted(rows[1:], key=_sort_func, reverse=reverse)


if __name__ == '__main__':
    assert len(sys.argv) == 3
    filename = Path(sys.argv[1])
    assert filename.exists()
    metric = sys.argv[2]
    rows = []
    with filename.open() as f:
        reader = csv.reader(f, delimiter=DELIMITER)
        rows = [r for r in reader]
    for row in hierarchical_sort(rows, metric):
        print(DELIMITER.join(row))
