labels = []

with open("src/label.txt", 'r') as file:
    labels = list(map(str.strip, file.readlines()))
