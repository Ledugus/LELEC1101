import os


with open("Labo1 sch4.asc") as f:
    lines = f.readlines()
    for line in lines:
        print(line.strip())
