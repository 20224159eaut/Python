_tuple = ('ab', 'b', 'e', 'c', 'd', 'e', 'ab')

temp = []

for i in _tuple:
    if _tuple.count(i) == 1:
        temp.append(i)

_new_tuple = tuple(temp)

print("Tuple moi:", _new_tuple)