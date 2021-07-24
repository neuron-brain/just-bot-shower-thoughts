# This is just a tool for the irregular verbs file.

from typing import List, Set, Tuple, Dict

file = open("irregular_verbs.csv", "r+")
header = None
items: Set[Tuple[str, str, str]] = set()
for line in file:
    line = line.strip()
    if header is None:
        header = line
        continue
    if line != "":
        items.add(tuple(line.lower().split(",")))

# Move everything into a dict so we can isolate potential duplicates
itemd: Dict[str, List[Tuple[str, str, str]]] = {}
for i in items:
    if i[0] in itemd:
        itemd[i[0]].append(i)
    else:
        itemd[i[0]] = [i]
# Now that it's in the dict, go through and ask user about potential duplicates
for key in itemd:
    if len(itemd[key]) > 1:
        lastinput = "-1"
        while lastinput != "" and len(itemd[key]) > 1:
            print("\n\n\n\n\nChoose a number to remove or enter empty to keep the remaining items:")
            for i in range(len(itemd[key])):
                print(f"{i}: {itemd[key][i]}")
            lastinput = input()
            if lastinput.isdecimal():
                try:
                    print(f"Removed {itemd[key].pop(int(lastinput))}")
                except IndexError:
                    pass

iteml: List[Tuple[str, str, str]] = []
for group in itemd.values():
    iteml.extend(group)
iteml = sorted(iteml)

newtext = header
for item in iteml:
    newtext += f"\n{item[0]},{item[1]},{item[2]}"
file.seek(0)
file.write(newtext)
file.truncate()
file.close()