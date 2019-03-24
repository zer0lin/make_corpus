
str1 = "Line1-abcdef \nLine2-abc \nLine4-abcd"
print(str1.split(' '))       # 以空格为分隔符，包含 \n
print(str1.split(' ', 1))    # 以空格为分隔符，分隔成两个
print(str1.split('\n'))
