_tuple = ('ab', 'b', 'e', 'c', 'd', 'e', 'ab')

temp = []

for i in _tuple:
    if i not in temp:
        temp.append(i)

_new_tuple = tuple(temp)

print("Tuple moi:", _new_tuple)