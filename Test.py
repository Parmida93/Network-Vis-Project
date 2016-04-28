import math

__author__ = 'ghahr'

array_result = [0,2,4,6,8,2,7,8]
n = 3
length_group = int(math.ceil(len(array_result) * 1.0 / n))
print length_group
grouped = [0 for i in range(n)]
index = 0
for i in range(0, len(array_result)):
    index = int(math.floor(i * 1.0 / length_group))
    print "grouped ", grouped[index]
    grouped[index] += array_result[i]
    print i
    print "index ", index
    print "grouped ", grouped[index]
    print "arr ", array_result[i]
for i in range(0, len(grouped)):
    if i == len(grouped) - 1:
        grouped[i] = grouped[i] * 1.0 / (len(array_result) - (n - 1) * length_group)
    else:
        grouped[i] = grouped[i] * 1.0 / length_group

print grouped
