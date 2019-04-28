import json

fd = open("../../ttttt", "w", encoding="UTF-8")
s = json.dumps({'favorite': ('coding', None, 'game', 25)})

print(s)

print("[", file=fd)
print(s+",", file=fd)
print("]", file=fd)

fd.close()
