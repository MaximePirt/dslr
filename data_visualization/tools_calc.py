def mean_calc(args):
	res = 0
	for i in args:
		res += i
	res = res / len(args)
	return res

def median_calc(args):
	l = len(args)
	res = []
	if l % 2:
		l += 1	
	l //= 2
	res = args[l - 1]
	return l - 1

def quartile(args):
	# Get median
	median = median_calc(args)
	quart = []
	median_tab = args[0:-median]
	# calculate first quartile
	quart1 = median_calc(median_tab)
	quart.append(median_tab[quart1])
	# calculate last quartile
	last_med_tab = args[median:]
	quart3 = median_calc(last_med_tab)
	quart.append(last_med_tab[quart3])

	return quart

def variance_calc(args):
	mean = mean_calc(args)
	tmp_var = []
	for i in args:
		tmp_var.append((i - mean) ** 2)
	
	variance = sum(tmp_var)
	variance = variance / len(args)
	return variance

def standard_deviation(args):
	variance = variance_calc(args)
	return variance ** 0.5