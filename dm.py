X = []
Y = []
d = {}
with open('input.txt', 'r') as f:
    for line in f:
        line = line.strip()  # remove any leading/trailing whitespaces
        i = 0
        x = ""
        while line[i] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            x += line[i]  # get the first value as string
            i += 1
        x += ".0"
        y = line[i+1:].strip()  # get the second value as string
        d[x] = y
        X.append(x)
        Y.append(y)

# # append additional values to X and Y
# X.append(2)
# Y.append('Rural')

# print(X)
# print(Y)
print(d)
