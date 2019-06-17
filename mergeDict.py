def mergeDict(Dict1, Dict2):
    res = {}
    for key, value in Dict1.items():
        if key in Dict2.keys():
            resvalue = value.intersection(Dict2[key])
            res[key] = resvalue
    return res

# Dict1 = {}
# Dict2 = {}
# set1 = set()
# set2 = set()
# set1.add(1)
# set1.add(2)
# set2.add(1)
# set2.add(3)
# Dict1["a"] = set1
# Dict2["a"] = set2
# res = mergeDict(Dict1,Dict2)
# for key, value in res.items():
#     print(key)
#     print(value)
