import csv
import json
import random
from collections.abc import Iterable
import abc
from typing import List


class Item:
    def __init__(self, name: str, weight: float, is_food: bool, priority: int):
        self.name = name
        self.weight = weight
        self.is_food = is_food
        self.priority = priority

    def __repr__(self):
        return f"{self.priority} -> {self.name}: {self.weight} {self.is_food}"


class ListOfItems(list):
    def __init__(self, i: Iterable[Item]):
        super().__init__(i)

    @staticmethod
    def loadFromCSV(filename="Rucksack.csv"):
        items = []
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                items.append(Item(row["name"], float(row["weight"]), bool(int(row["is_food"])), int(row["priority"])))
        return ListOfItems(items)

    def to_json(self, filename="Rucksack.json"):
        with open(filename, "w") as jsonfile:
            j = json.dumps([ob.__dict__ for ob in self])
            jsonfile.write(j)
            return j


class BackPack(abc.ABC):
    def __init__(self, weight_limit: float, i: List[Item]):
        self.item_list = i
        self.used_weight = 0
        self.weight_limit = weight_limit
        self.packed_items: List[Item] = []

    @abc.abstractmethod
    def _get_next_item(self) -> Item:
        pass

    def pack(self):
        while self.used_weight < self.weight_limit and len(self.item_list) != 0:
            item = self._get_next_item()
            if item.weight + self.used_weight <= self.weight_limit:
                # still enough space in backpack
                self.packed_items.append(item)
                self.used_weight += item.weight
                self.item_list.remove(item)
            else:
                # not enough space, abort
                break

    def getPackedItems(self):
        return ListOfItems(self.packed_items)


class RandomBackPack(BackPack):
    def _get_next_item(self):
        return random.choice(self.item_list)


class OptimalBackPack(BackPack):
    def _get_next_item(self):
        # sort by priority and is_food
        items_with_highest_priority = sorted(self.item_list, key=lambda i: (i.priority, not i.is_food))
        # now get the item with the highest weight that fits in the backpack
        max_weight = 0
        result = None
        for i in items_with_highest_priority:
            if i.weight > max_weight and i.weight + self.used_weight <= self.weight_limit:
                max_weight = i.weight
                result = i
        return result


def test1_evaluateBP(name: str, bp: BackPack, item_list):
    print(f"{name}")
    print("\tfill-rate: {:.0%}".format(bp.used_weight / bp.weight_limit))
    print(f"\tcontains all items: {set(item_list) == set(bp.packed_items)}")


def test1():
    item_list = ListOfItems.loadFromCSV()
    random_bp = RandomBackPack(2550, item_list.copy())
    optimal_bp = OptimalBackPack(2550, item_list.copy())
    random_bp.pack()
    optimal_bp.pack()
    random_bp.getPackedItems().to_json("RandomBackpack.test1.json")
    optimal_bp.getPackedItems().to_json("OptimalBackpack.test1.json")
    print("======")
    print("TEST 1")
    test1_evaluateBP("RandomBackpack", random_bp, item_list)
    test1_evaluateBP("OptimalBackpack", optimal_bp, item_list)
    print("======")


def test2():
    item_list = ListOfItems.loadFromCSV()
    random_bp = RandomBackPack(2000, item_list.copy())
    optimal_bp = OptimalBackPack(2000, item_list.copy())
    random_bp.pack()
    optimal_bp.pack()
    random_bp.getPackedItems().to_json("RandomBackpack.test2.json")
    optimal_bp.getPackedItems().to_json("OptimalBackpack.test2.json")
    print("======")
    print("TEST 2")
    print("RandomBackpack\n\tfill-rate: {:.0%}".format(random_bp.used_weight / random_bp.weight_limit))
    print("OptimalBackpack\n\tfill-rate: {:.0%}".format(optimal_bp.used_weight / optimal_bp.weight_limit))
    print("======")


# Test 1: check if all items get put into the backpack if enough space
test1()

# Test 2: check with constrained weight limit how good the backpack gets filled
test2()

# TODO more tests
