def foo():
    global x1
    print(x1)
    x1 = 5
    print(x1)


if __name__ == "__main__":
    x1 = 6
    foo()
