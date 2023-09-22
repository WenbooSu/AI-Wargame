class Animals:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def show_info(self):
        return f"{self.name}{self.age}"


obj1 = Animals('Do', 1)
obj2 = Animals('Dg', 2)
obj3 = Animals('og', 3)
obj4 = Animals('Dg', 4)
obj5 = Animals('Ct', 1)
obj6 = Animals('Ct', 2)
obj7 = Animals('Ct', 3)
obj8 = Animals('Ct', 4)
print(type(obj8))

graph = {
    'A': [obj1, obj2, obj3, None, None],
    'B': [obj4, None, None, None, None],
    'C': [None, None, None, None, obj5],
    'D': [None, None, obj6, obj7, obj8]
}

graph2 = [
    [obj1, obj2, obj3, None, None],
    [obj4, None, None, None, None],
    [None, None, None, None, obj5],
    [None, None, obj6, obj7, obj8]
]
# 00 01 02 03 04
# 10 11 12 13 14
# 20 21 22 23 24
# 30 31 32 33 34

print(graph2[3][2].show_info())


def display_board():
    for row in graph2:
        for obj in row:
            if isinstance(obj, Animals):
                print(obj.show_info(), end=' ')
            else:
                print(' * ', end=' ')
        print()


# Game Board Cleared
display_board()

print()


def switch(o1, o2):
    o1, o2 = o2, o1


# Call the function with graph2 and the positions you want to switch
# graph2[3][2], graph2[2][2] = graph2[2][2], graph2[3][2]
switch(graph2[3][2], graph2[2][2])

display_board()
