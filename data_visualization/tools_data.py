def get_pairs(col_a, col_b):
	'''Return two lists without the rows where one value is NaN'''
	a, b = [], []
	for x, y in zip(col_a, col_b):
		if x == x and y == y:   # NaN != NaN
			a.append(x)
			b.append(y)
	return a, b


