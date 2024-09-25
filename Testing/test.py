dict1 = {'a': 1, 'b': 2}
dict2 = {'b': 3, 'c': 4}

merged_dict = dict(dict1, **dict2)
merge2 = dict1 | dict2

print(merged_dict)
print(merge2)
print(dict1)
print(dict2)