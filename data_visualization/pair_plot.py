import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from load_csv import load
from tools_data import get_pairs

HOUSES = {
	"Gryffindor": "#ae0001",
	"Hufflepuff": "#ecb939",
	"Ravenclaw": "#2c5fa8",
	"Slytherin": "#2a623d",
}

def split_by_house(datas):
	'''Return a dict {house: rows of that house}'''
	return {house: datas[datas["Hogwarts House"] == house] for house in HOUSES}



def format_cell(ax, courses, i, j):
	'''Remove ticks, write course names only on the bottom row and left column'''
	ax.set_xticks([])
	ax.set_yticks([])
	if i == len(courses) - 1:
		ax.set_xlabel(courses[j][:12], fontsize=8, rotation=30)
	if j == 0:
		ax.set_ylabel(courses[i][:12], fontsize=8, rotation=0, ha="right")


	def draw_cell(ax, courses, i, j, houses_data):
		'''Draw a histogram if i == j, else draw a scatter plot'''
		for house, rows in houses_data.items():
			color = HOUSES[house]
			if i == j:
				values = [v for v in rows[courses[j]] if v == v]
				ax.hist(values, bins=15, color=color, alpha=0.6)
			else:
				x, y = get_pairs(rows[courses[j]], rows[courses[i]])
				ax.scatter(x, y, s=2, color=color, alpha=0.5)



def main():
	datas = load("../datasets/dataset_train.csv")
	if datas is None:
		print("Error, dataset not loaded")
		return -1

	courses = list(datas.select_dtypes(include="number").columns.drop("Index"))
	n = len(courses)
	houses_data = split_by_house(datas)
	fig, axes = plt.subplots(n, n, figsize=(16, 16))

	for i in range(n):
		for j in range(n):
			ax = axes[i][j]
			draw_cell(ax, courses, i, j, houses_data)
			format_cell(ax, courses, i, j)

	handles = [Line2D([0], [0], marker="o", linestyle="", color=c, label=h)
			for h, c in HOUSES.items()]
	fig.legend(handles=handles, loc="upper right", fontsize=12)
	plt.tight_layout()
	plt.show()
	return 0


if __name__ == "__main__":
	main()