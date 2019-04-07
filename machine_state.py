chars = ['A', 'C', 'D', 'E', 'F']
A_places = {}
C_places = {}
D_places = {}
E_places = {}
F_places = {}
for i in range(1, 22):
    A_places[i] = str(i) + chars[0]
    C_places[i] = str(i) + chars[1]
    D_places[i] = str(i) + chars[2]
    E_places[i] = str(i) + chars[3]
    F_places[i] = str(i) + chars[4]

print(list(A_places.values()))
print(list(C_places.values()))
print(list(D_places.values()))
print(list(E_places.values()))
print(list(F_places.values()))


