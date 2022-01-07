from random import randint


def generate_id():

    x = randint(1, 200000)
    with open('used_IDs.txt', 'r') as f:
        contents = f.readlines()

    while x in contents:
        x = randint(1, 200000)

    with open('used_IDs.txt', 'a') as f:
        f.write(str(x) + ' ')

    return str(x)


print(generate_id())
