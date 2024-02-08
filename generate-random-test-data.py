
# started 2/8/2024
# Rich W.
# with
# GitHub Copilot

import random


def generate_random_number():
    return random.randint(1, 10)

def generate_random_number_list(length):
        return list(random.randint(1, 10) for _ in range(length))

if __name__ == '__main__':
    resultnumber = generate_random_number()
    resultset = generate_random_number_list(resultnumber)
    print(resultset)