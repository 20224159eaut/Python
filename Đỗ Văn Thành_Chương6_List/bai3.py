_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]

so_chan = []
so_le = []

for i in _list:
    if i % 2 == 0:
        so_chan.append(i)
    else:
        so_le.append(i)

print("So chan:", so_chan)
print("So le:", so_le)