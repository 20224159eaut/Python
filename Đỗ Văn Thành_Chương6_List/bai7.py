
_list = ['abc', 'xyz', 'abc', '12', 'ii', '12', '5a']

# 7.1
new_1 = []

for i in _list:
    if _list.count(i) == 1:
        new_1.append(i)

print("Ket qua 7.1:", new_1)

# 7.2
new_2 = []

for i in _list:
    if i not in new_2:
        new_2.append(i)

print("Ket qua 7.2:", new_2)