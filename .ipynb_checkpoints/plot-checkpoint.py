import csv
import matplotlib.pyplot as plt

filename = 'all_with_score.csv'

with open(filename, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    info = [row[1:] for row in reader][1:]

with open(filename, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    score = [row[-1] for row in reader][1:]

print(max(score))
print(min(score))

for i in info:
    if i[-1] == max(score):
        print('max(score): ' + i[0])
    elif i[-1] == min(score):
        print('min(score) ' + i[0])