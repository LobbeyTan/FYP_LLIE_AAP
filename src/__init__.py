import os

labels = []

with open(os.getcwd() + r'/models/labels.txt', 'r') as file:
    labels = list(map(str.strip, file.readlines()))
