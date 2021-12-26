from City import City


def distance(city1: City, city2: City) -> int:
    return ((city1.x - city2.x) ** 2 + (city1.y - city2.y) ** 2) ** (1 / 2)


def get_cities(path: str) -> list[City]:
    cities = []
    with open(path, 'r') as file:
        line = file.readline()
        while line != "":
            i, x, y = line.split()
            cities.append(City(i, int(x), int(y)))
            line = file.readline()
    return cities
