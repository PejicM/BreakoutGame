from base import Location, Vector


loc1 = Location(3, 3)
loc2 = Location(5, 5)

rez = loc1.__sub__(loc2)
print(rez.__str__())
