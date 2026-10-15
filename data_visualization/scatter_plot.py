import matplotlib.pyplot as plt
from load_csv import load
from tools_calc import mean_calc, standard_deviation
from tools_data import get_pairs


def standardise_data(data):
	'''Standardise the data to have a mean of 0 and a standard deviation of 1'''
	mean = mean_calc(data)
	std_dev = standard_deviation(data)
	return [(x - mean) / std_dev for x in data]

def ft_correlation(col_a, col_b):
	'''Calculate the correlation coefficient between two lists of data'''
	if len(col_a) != len(col_b):
		raise ValueError("Lists must be of the same length")
	ca, cb = standardise_data(col_a), standardise_data(col_b)

	covariance = sum(x * y for x, y in zip(ca, cb)) / len(ca)
	return covariance

def main():
	try:
		datas = load("../datasets/dataset_train.csv")
		if datas is None:
			print("Error, dataset not loaded")
			return -1
		print("Datasets loaded")

		courses = datas.select_dtypes(include="number").columns.drop("Index")

		best = (None, None, 0)
		for i in range(len(courses)):
			for j in range(i + 1, len(courses)):
				a, b = get_pairs(datas[courses[i]], datas[courses[j]])
				r = ft_correlation(a, b)
				if abs(r) > abs(best[2]):
					best = (courses[i], courses[j], r)
		
		c1, c2, r = best
		print(f"Most similar features: {c1} / {c2} (r = {r:.4f})")

		a, b = get_pairs(datas[c1], datas[c2])
		plt.scatter(a, b, s=10)
		plt.xlabel(c1)
		plt.ylabel(c2)
		plt.title(f"{c1} vs {c2}")
		plt.show()
	except:
		print("Error")
		return -1
	return 


if __name__ == "__main__":
	main()