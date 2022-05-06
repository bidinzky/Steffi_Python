import csv
import random
from typing import List
import abc


class BackPackItem:
    def __init__(self, name: str, size: float):
        self.name = name
        self.size = size

    def __repr__(self):
        return f"{self.name}: {self.size}"


class ProtoBackPack(abc.ABC):
    def __init__(self, size: float = 100, csv_name: str = "backpack.csv"):
        self.size = size
        self.used_space = 0.0
        self.packed_items = []
        self.item_list = list(self._provide(csv_name))

    @staticmethod
    def _provide(name) -> List[BackPackItem]:
        with open(name, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                yield BackPackItem(row["name"], float(row["size"]))

    @abc.abstractmethod
    def _get_next_item(self):
        pass

    def pack(self):
        while self.used_space < self.size and len(self.item_list) != 0:
            item = self._get_next_item()
            if item.size + self.used_space <= self.size:
                # still enough space in backpack
                self.packed_items.append(item)
                self.used_space += item.size
                self.item_list.remove(item)
            else:
                # not enough space, abort
                break
        return self.packed_items


class RandomBackPack(ProtoBackPack):
    def _get_next_item(self):
        return random.choice(self.item_list)


class OptimalBackPack(ProtoBackPack):
    def _get_next_item(self):
        return max(self.item_list, key=lambda li: li.size)


backpack = RandomBackPack(11)
backpack2 = OptimalBackPack(11)
packed = backpack.pack()
packed2 = backpack2.pack()
print(packed)
print(sum((sv.size for sv in packed)))
print(packed2)
print(sum((sv.size for sv in packed2)))

