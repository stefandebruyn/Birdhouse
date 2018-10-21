import os

inp = open(os.getcwd() + "/data/cities.csv", "r", errors="replace")
outp = open(os.getcwd() + "/data/us_cities.txt", "w")
cities = []
count = 0

for line in inp.readlines():
    open_quote = line.index('"')
    close_quote = line[1:len(line)].index('"')
    city_name = line[open_quote+1:close_quote+1]
    count += 1
    print("Parsed", count, city_name)

    pos = 0

    while pos < len(cities) and cities[pos] < city_name:
        pos += 1

    cities.insert(pos, city_name)

uniques = []

for city in cities:
    try:
        if city not in uniques:
            outp.write(city.lower() + "\n")
            uniques.append(city)
    except Exception:
        pass
