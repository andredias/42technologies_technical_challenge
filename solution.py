"""
Usage:

python solution.py INPUT_FILENAME METRIC_FIELDNAME

In order to save the output to a file, redirect the output to a file.
Example:

python solution.py data-big-input.txt net_sales_units > output.txt


ATTENTION:

There might be differences in the decimal places in number columns between
the output produced by this solution and the output data provided as reference.
"""

import csv
import sys
from pathlib import Path

from tree import Node

DELIMITER = '|'


def hierarchical_sort(rows: list, metric: str, reverse=True) -> list:

    # partial sort
    header = rows[0]
    metric_index = header.index(metric)
    p_index = max(i for i, name in enumerate(rows[0]) if name.startswith('property'))

    def _sort_func(row: list) -> list:
        result = (
            [(int(row[i] == '$total'), row[i]) for i in range(p_index)] +
            [(int(row[p_index] == '$total'), float(row[metric_index]))]
        )
        return result

    partially_sorted_rows = sorted(rows[1:], key=_sort_func, reverse=reverse)

    # second sorting pass
    ref_node = root = Node(row=partially_sorted_rows[0], metric_index=metric_index)
    for row in partially_sorted_rows[1:]:
        new_node = Node(row=row, metric_index=metric_index)
        ref_node.insert(new_node)
        ref_node = new_node
    return [header] + root.export_rows(reverse=reverse)


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
