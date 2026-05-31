# BAR PLOT

import matplotlib.pyplot as plt
import seaborn as sns
import pickle

# load data
with open('coding-exp-by-dev-type.pickle', 'rb') as f:
    data = pickle.load(f)

# split into two lists
dev_types, years_exp = zip(*data)
dev_types = list(dev_types)
years_exp = list(years_exp)

# matplotlib: plt.barh(bar_coords, years_exp)
sns.barplot(y=dev_types, x=years_exp)
plt.xlabel('years')
plt.title('Years of Coding Experience by Developer Type')
plt.tight_layout()
plt.show()

# COLUMN PLOT

import matplotlib.pyplot as plt
import seaborn as sns
import pickle

# load our data (rb means read binary data)
with open('fruit-sales.pickle', 'rb') as f:
    data = pickle.load(f)

# splitting a list of tuples into two lists
fruit, num_sold = zip(*data)
fruit = list(fruit)
num_sold = list(num_sold)

# matplotlib: plt.bar(bar_coords, num_sold)
axes = sns.barplot(x=fruit, y=num_sold)
axes.set_title('Number of fruit sold (2017)')
axes.set_ylabel('Number of fruit (millions)')

#plt.ylabel('Number of fruit (millions)')
#plt.title('Number of fruit sold (2017)')
plt.show()

# JOINT PLOT

import matplotlib.pyplot as plt
import seaborn as sns
import pickle

# load data
with open('iris.pickle', 'rb') as f:
    iris = pickle.load(f)

# extract the first column from the data table (get all of the rows)
sepal_length = iris['data'][:, 0]
sepal_width = iris['data'][:, 1]
classes = iris['target']

# scatter, reg, kde, hex
axes = sns.jointplot(sepal_length, sepal_width, kind='hex')
axes.set_axis_labels('Sepal length (cm)', 'Sepal width (cm)')
plt.show()

# LINE PLOT

import matplotlib.pyplot as plt
import seaborn as sns
import pickle

# load data
with open('prog-langs-popularity.pickle', 'rb') as f:
    data = pickle.load(f)

# split into two lists
languages, rankings = zip(*data)

# get the Java years and ranks (split Java data into two lists)
java_years, java_ranks = zip(*rankings[0])

# matplotlib: plt.plot(java_years, java_ranks)
sns.lineplot(java_years, java_ranks)
plt.xticks(java_years)
plt.xlabel('year')
plt.ylabel('ranking')
plt.title('Java Ranking')
plt.show()

# MULTILINE PLOT

import matplotlib.pyplot as plt
import seaborn as sns
import pickle

# load data
with open('prog-langs-popularity.pickle', 'rb') as f:
    data = pickle.load(f)

# split into two lists
languages, rankings = zip(*data)

# iterate over all of the language and call "plot" on their data
for i in range(len(languages)):
    # for each language, split their data into years and rankings lists
    years, ranks = zip(*rankings[i])
    # matplotlib: plt.plot(years, ranks)
    sns.lineplot(years, ranks)

plt.xlabel('year')
plt.ylabel('ranking')
plt.title('Rankings of Programming Languages')
plt.legend(languages)
plt.show()

# SCATTER PLOT

import matplotlib.pyplot as plt
import seaborn as sns
import pickle

# load data
with open('iris.pickle', 'rb') as f:
    iris = pickle.load(f)

# extract the first column from the data table (get all of the rows)
sepal_length = iris['data'][:, 0]
sepal_width = iris['data'][:, 1]
classes = iris['target']

# matplotlib: plt.scatter(sepal_length, sepal_width, c=classes)
sns.scatterplot(sepal_length, sepal_width, hue=classes, legend=False)
plt.xlabel('Sepal length (cm)')
plt.ylabel('Sepal width (cm)')
plt.title('Iris data: sepal length v. width')
plt.show()

# SUBPLOTS

import matplotlib.pyplot as plt
import seaborn as sns
import pickle

# load data
with open('iris.pickle', 'rb') as f:
    iris = pickle.load(f)

# extract the first column from the data table (get all of the rows)
sepal_length = iris['data'][:, 0]
sepal_width = iris['data'][:, 1]
petal_length = iris['data'][:, 2]
petal_width = iris['data'][:, 3]
classes = iris['target']

fig, axes = plt.subplots(2, 2)
# matplotlib: axes[0,0].scatter(sepal_length, sepal_width, c=classes)
sns.scatterplot(sepal_length, sepal_width, hue=classes, legend=False, ax=axes[0,0])
axes[0,0].set_xlabel('Sepal length (cm)')
axes[0,0].set_ylabel('Sepal width (cm)')

# top-right: petal length v. petal width
# matplotlib: axes[0,1].scatter(petal_length, petal_width, c=classes)
sns.scatterplot(petal_length, petal_width, hue=classes, legend=False, ax=axes[0,1])
axes[0,1].set_xlabel('Petal length (cm)')
axes[0,1].set_ylabel('Petal width (cm)')

# bottom-left (2nd row, 1st col): sepal length v. petal length
# matplotlib: axes[1,0].scatter(sepal_length, petal_length, c=classes)
sns.scatterplot(sepal_length, petal_length, hue=classes, legend=False, ax=axes[1,0])
axes[1,0].set_xlabel('Sepal length (cm)')
axes[1,0].set_ylabel('Petal length (cm)')

# bottom-right (2nd row, 2nd col): sepal width v. petal width
# matplotlib: axes[1,1].scatter(sepal_width, petal_width, c=classes)
sns.scatterplot(sepal_width, petal_width, hue=classes, legend=False, ax=axes[1,1])
axes[1,1].set_xlabel('Sepal width (cm)')
axes[1,1].set_ylabel('Petal width (cm)')

fig.suptitle('Iris dataset')
plt.show()
