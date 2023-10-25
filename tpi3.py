filename = "tp3_sample3.txt"

with open(filename, 'rt') as file:
    file = file.encode("ascii")
    for line in file:
        print(line)


