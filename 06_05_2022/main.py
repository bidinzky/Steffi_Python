import csv
import json
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
        return PackedBackPack(self.size, self.packed_items)


class RandomBackPack(ProtoBackPack):
    def _get_next_item(self):
        return random.choice(self.item_list)


class OptimalBackPack(ProtoBackPack):
    def _get_next_item(self):
        return max(self.item_list, key=lambda li: li.size)


class PackedBackPack:
    def __init__(self, max_size: float, items: List[BackPackItem]):
        self.items = items
        self.max_size = max_size
        self.size = sum(sv.size for sv in items)

    def __repr__(self):
        return f"items: {self.items}\nsize: {self.size}"

    def to_json(self):
        return  json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


backpack = RandomBackPack(11.5)
backpack2 = OptimalBackPack(11.5)
packed = backpack.pack()
packed2 = backpack2.pack()
print(packed)
print(packed.to_json())
print(packed2)
print(packed2.to_json())

