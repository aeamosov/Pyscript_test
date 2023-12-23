from pyscript import document
from pyscript import display
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
def get_root(event):
	input_text=document.querySelector("#num")
	a=input_text.value
	output_div = document.querySelector("#output")
	output_div.innerText = round(np.sqrt(int(a)),2)

def draw_hist(event):
	plt.clf()
	mu, sigma = 0, 0.1 
	s = np.random.normal(mu, sigma, 1000)
	ax=sns.histplot(s)
	fig1=ax.get_figure()
	#plt.show()
	display(fig1,target="hist",append=False)