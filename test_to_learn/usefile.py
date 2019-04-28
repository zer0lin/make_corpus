fd = open("../../ttttt", "r", encoding="UTF-8")
s = fd.read()
x = s.split("\n")[:-1]
print(x)
fd.close()

xx = len(x)
for i in range(0, xx):
    print(x[i] + "ddddd")
