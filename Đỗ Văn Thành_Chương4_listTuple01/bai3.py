# 1. Tao file
f = open("demo_file1.txt", "w", encoding="utf-8")
f.write("Thuc hanh\n")
f.write("n voi n file\n")
f.write("in IO")
f.close()

# 2. Doc file
f = open("demo_file1.txt", "r", encoding="utf-8")
ds = f.readlines()
f.close()

# 3a. In tren 1 dong (tuple)
t = tuple(ds)
print("Noi dung tren 1 dong:")
for x in t:
    print(x.strip(), end=" ")

# 3b. In tung dong (list)
print("\nNoi dung tung dong:")
for x in ds:
    print(x.strip())