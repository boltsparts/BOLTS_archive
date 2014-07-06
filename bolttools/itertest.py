def check_iterator_arguments(items,primary,optional,kwargs):
	#check items
	if primary not in items:
		raise PrimaryItemMissingError(primary)
	for it in items:
		if it == primary:
			continue
		if not it in optional:
			raise UnknownItemError(it)
	#check filters
	filters = ["filter_%s" % o for o in optional]
	for k in kwargs:
		if not k in filters:
			raise ValueError("Unknown argument %s for iterator" % k)

def filter_iterator_items(its,kwargs):
	for i in its:
		fil = "filter_" + i
		if fil in kwargs and not its[i] in kwargs[fil]:
			return False
	return True



animals = ["Lion", "Icebear", "Kangaroo", "Rabbit"]
continents = {"Africa" : ["Lion"], "Australia" : ["Kangaroo"], "Europe" : ["Rabbit"], "Antarctica" : ["Icebear"]}
food = {"Lion" : "Meat", "Icebear" : "Penguin", "Kangaroo" : "Plants", "Rabbit" : "Plants"}

def iteranimals(items=["animal"],**kwargs):
	check_iterator_arguments(items,"animal",["continent","food"],kwargs)
	its = {}
	for a in animals:
		its["animal"] = a
		its["food"] = food[a]
		for c in continents:
			if a in continents[c]:
				its["continent"] = c
		if filter_iterator_items(its,kwargs):
			yield tuple(its[i] for i in items)

for a,c in iteranimals(["animal","continent"],filter_continent=["Europe","Africa"],filter_food=["Plants"]):
	print a,c

for a, in iteranimals():
	print a
