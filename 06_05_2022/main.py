import csv
import json
import random


class Item:
    def __init__(self, name, weight, is_food, priority):
        self.name = name
        self.weight = weight
        self.is_food = is_food
        self.priority = priority

    def __repr__(self):
        return f"{self.priority} -> {self.name}: {self.weight} {self.is_food}"


class ListOfItems:
    def __init__(self, default=None):
        if default is None:
            default = []
        self.items = default

    def loadFromCSV(self, filename="Rucksack.csv"):
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.items.append(Item(row["name"], float(row["weight"]), bool(int(row["is_food"])), int(row["priority"])))

    def to_json(self, filename="Rucksack.json"):
        with open(filename, "w") as jsonfile:
            j = json.dumps([ob.__dict__ for ob in self.items])
            jsonfile.write(j)
            return j


class BackPack:
    def __init__(self, weight_limit, i):
        self.item_list = i
        self.used_weight = 0
        self.weight_limit = weight_limit
        self.packed_items = []

    # needs to be implemented by subclass
    def _get_next_item(self) -> Item:
        pass

    def pack(self):
        # while still space in backpack and there are items that can be put into it
        while self.used_weight < self.weight_limit and len(self.item_list.items) != 0:
            # get next item (override from subclass)
            item = self._get_next_item()
            # if there is a next time, and it fits into the backpack
            if item is not None and item.weight + self.used_weight <= self.weight_limit:
                # add it to the packed items
                self.packed_items.append(item)
                # increase the used weight
                self.used_weight += item.weight
                # remove it from the item-list, so it only gets added one time
                self.item_list.items.remove(item)
            else:
                # not enough space, abort
                break

    def getPackedItems(self):
        return ListOfItems(self.packed_items)


class RandomBackPack(BackPack):
    def _get_next_item(self):
        return random.choice(self.item_list.items)


class OptimalBackPack(BackPack):
    def _get_next_item(self):
        # sort by priority and is_food and weight as last
        # https://stackoverflow.com/questions/20145842/python-sorting-by-multiple-criteria
        items_with_priority = sorted(self.item_list.items, key=lambda i: (i.priority, i.is_food, i.weight), reverse=True)
        # now get the item with the highest weight that fits in the backpack
        items_with_priority_fits = filter(lambda i: i.weight + self.used_weight <= self.weight_limit, items_with_priority)
        # get the first item in the list or None if it doesn't exist
        result = next(items_with_priority_fits, None)
        return result


def get_ListOfItems():
    item_list = ListOfItems()
    item_list.loadFromCSV()
    return item_list


def test1_evaluateBP(name, bp, item_list):
    print(f"{name}")
    print("\tfill-rate: {:.0%}".format(bp.used_weight / bp.weight_limit))
    print(f"\tcontains all items: {set(item_list.items) == set(bp.packed_items)}")


def test1():
    item_list = get_ListOfItems()
    random_bp = RandomBackPack(2550, get_ListOfItems())
    optimal_bp = OptimalBackPack(2550, get_ListOfItems())
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
    random_bp = RandomBackPack(2050, get_ListOfItems())
    optimal_bp = OptimalBackPack(2050, get_ListOfItems())
    random_bp.pack()
    optimal_bp.pack()
    random_bp.getPackedItems().to_json("RandomBackpack.test2.json")
    optimal_bp.getPackedItems().to_json("OptimalBackpack.test2.json")
    print("======")
    print("TEST 2")
    print("RandomBackpack\n\tfill-rate: {:.0%}".format(random_bp.used_weight / random_bp.weight_limit))
    print("OptimalBackpack\n\tfill-rate: {:.0%}".format(optimal_bp.used_weight / optimal_bp.weight_limit))
    print("======")


def test3():
    random_bp = RandomBackPack(1500, get_ListOfItems())
    optimal_bp = OptimalBackPack(1500, get_ListOfItems())
    random_bp.pack()
    optimal_bp.pack()
    random_bp.getPackedItems().to_json("RandomBackpack.test3.json")
    optimal_bp.getPackedItems().to_json("OptimalBackpack.test3.json")
    print("======")
    print("TEST 3")
    print("BackPack should be: [cereal_bar, waterbottle, snacks]")
    print(f"RandomBackpack\n\t {random_bp.getPackedItems().items}")
    print(f"OptimalBackpack\n\t {optimal_bp.getPackedItems().items}")
    print("======")


def test4():
    random_bp = RandomBackPack(1550, get_ListOfItems())
    optimal_bp = OptimalBackPack(1550, get_ListOfItems())
    random_bp.pack()
    optimal_bp.pack()
    random_bp.getPackedItems().to_json("RandomBackpack.test4.json")
    optimal_bp.getPackedItems().to_json("OptimalBackpack.test4.json")
    print("======")
    print("TEST 4")
    print("BackPack should be: [cereal_bar, waterbottle, snacks, inhaler]")
    print(f"RandomBackpack\n\t {random_bp.getPackedItems().items}")
    print(f"OptimalBackpack\n\t {optimal_bp.getPackedItems().items}")
    print("======")

# Test 1: check if all items get put into the backpack if enough space
test1()

# Test 2: check with constrained weight limit how good the backpack gets filled
test2()

# Test 3: check if the backpack gets packed with the right priority
test3()

test4()