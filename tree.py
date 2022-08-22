from bisect import insort
from functools import total_ordering


@total_ordering
class Node:
    def __init__(
        self,
        row: list,
        metric_index: int,
        parent: 'Node' = None
    ):
        self.level = row.count('$total')
        self.amount = float(row[metric_index])
        self.parent = parent
        self.row = row
        self.children = []

    def __eq__(self, other):
        return self.amount == other.amount

    def __lt__(self, other):
        return self.amount < other.amount

    def insert(self, node: 'Node') -> 'Node':
        if node.level >= self.level:
            return self.parent.insert(node)
        node.parent = self
        insort(self.children, node)
        return self

    def export_rows(self, reverse: bool = True) -> list:
        rows = []
        rows.append(self.row)
        children = reversed(self.children) if reverse else self.children
        for node in children:
            rows.extend(node.export_rows())
        return rows
