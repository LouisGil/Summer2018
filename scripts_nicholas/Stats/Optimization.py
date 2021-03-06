################################################################################################
# Call the script as:
# python Optimization.py <data file>
################################################################################################

#------------------------------------------------------------------------------------------------
import sys # For command-line arguments
import pandas as pd # For dataframes
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
sys.path.append('/Users/nicholaslenz/Desktop/Summer2018/scripts_nicholas')
import MiscFunctions as mf
#------------------------------------------------------------------------------------------------

## Script that plots a predictor's accuracy as a function of its scoring threshold.
#  @param data_file : A csv-like file that contains both a variant's pathogenicty and its score.
#
def Optimization(data_file):
	# Creates a dataframe from data_file.
	sep = mf.determine_separator(sys.argv[1])
	df = pd.read_csv(sys.argv[1], sep=',')

	# Creates a partition of the interval [0,1]. Creates two empty lists; one will store the accuracy
	# and the other will store the threshold.
	thresholds = [float(i)/100 for i in range(101)]
	x = []
	y = []

	# Determines what term will be considered positive and which will be negative.
	positive_term = 'Pathogenic'
	negative_term = 'Benign'
	total = df['pathogenicity'].shape[0]

	# For each threshold in the partition, determines the accuracy of the predictor.
	for threshold in thresholds:
		true_positives  = 0
		true_negatives = 0
		for index, row in df.iterrows():
			score = float(row.values[2])
			if ( (score >= threshold) & (row.values[1] == positive_term) ):
				true_positives += 1
			elif ( (score < threshold) & (row.values[1] == negative_term) ):
				true_negatives += 1
		accuracy = (true_positives + true_negatives)/total
		x.append(threshold)
		y.append(accuracy)

	print('Max : ' + str(max(y)) + '\nAt  : ', end='')
	print(*[x[index] for index, value in enumerate(y) if value == max(y)], sep=', ')

	#------------------------------------------------------------------------------------------------
	# Creates an empty figure, with total area of 1.
	figure = plt.figure(figsize=(6, 6))
	ax = figure.add_subplot(1, 1, 1)
	ax.set_xlim(0, 1)
	ax.set_ylim(0, 1)
	ax.xaxis.set_major_locator(MultipleLocator(0.250))
	ax.yaxis.set_major_locator(MultipleLocator(0.250))
	ax.xaxis.set_minor_locator(MultipleLocator(0.125))
	ax.yaxis.set_minor_locator(MultipleLocator(0.125))
	ax.tick_params(which='major', length=10.0)
	ax.tick_params(which='minor', length=5.0)
	ax.set_ylabel('Accuracy')
	ax.set_xlabel('Threshold')

	# Draws the grid and plots the response curve.
	ax.grid(linestyle=':', linewidth=0.5, color='black')
	ax.plot(x, y, color='blue', linewidth='3.0')
	plt.show()

################################ Main ################################

"""
# arg1 : The file that contains a variant's pathogenicity as classified by ENIGMA or ClinVar and
# its score. The appropriate file format is:
,pathogenicity,scores
0,Benign,0.284
1,Pathogenic,0.19
...

"""
Optimization(sys.argv[1])
