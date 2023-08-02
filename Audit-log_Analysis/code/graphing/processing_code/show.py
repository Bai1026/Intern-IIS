with open('../data_new_entity/data_with_sigma.txt', 'r') as file:
    fileline = file.readlines()

for line in fileline[-20:]:
    print(line.strip())