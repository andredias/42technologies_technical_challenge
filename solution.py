import csv
import sys
from pathlib import Path

DELIMITER = '|'


def hierachical_sort(rows: list, metric: str, reverse=True) -> list:
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
    for row in hierachical_sort(rows, metric):
        print(DELIMITER.join(row))
