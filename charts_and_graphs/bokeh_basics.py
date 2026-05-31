# MULTILINE

from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.palettes import Dark2_5 as palette
import pickle

output_file('multiline.html')

with open('prog-langs-popularity.pickle', 'rb') as f:
    data = pickle.load(f)

languages, rankings = zip(*data)

fig = figure(x_axis_label='year', y_axis_label='rank', title='Rankings of Programming Languages')

for i in range(len(languages)):
    years, ranks = zip(*rankings[i])
    # legend & color for this particular line
    fig.line(years, ranks, line_width=2, legend_label=languages[i], color=palette[i])

# interactive legend:
fig.legend.click_policy = 'hide'

show(fig)

# HOVER

from bokeh.io import show, output_file
from bokeh.plotting import figure
import pickle

output_file('hover.html')

with open('coding-exp-by-dev-type.pickle', 'rb') as f:
    data = pickle.load(f)
    
dev_types, years_exp = zip(*data)
data_source = {'dev_types': dev_types, 'years_exp': years_exp}

# tool tips: "years of experience: actual val"
TOOLTIPS = [('years of experience', '@years_exp')]
plot = figure(y_range=dev_types, x_axis_label='years', title='Coding Experience by Developer Type', tools='hover', tooltips=TOOLTIPS)
# set data source: looks up values in data source dictionary
plot.hbar(y='dev_types', right='years_exp', height=0.9, source=data_source)

show(plot)

# COLUMN PLOT

from bokeh.io import show
from bokeh.plotting import figure
import pickle

# load data
with open('fruit-sales.pickle', 'rb') as f:
    data = pickle.load(f)

# split into two lists
fruit, num_sold = zip(*data)

plot = figure(x_range=fruit, y_axis_label='Fruit sold (millions)', title='Fruit sold (2017)')
plot.vbar(x=fruit, top=num_sold, width=0.9)

show(plot)

# BAR PLOT

from bokeh.io import show, output_file
from bokeh.plotting import figure
import pickle

output_file('bar.html')

with open('coding-exp-by-dev-type.pickle', 'rb') as f:
    data = pickle.load(f)
    
dev_types, years_exp = zip(*data)

plot = figure(y_range=dev_types, x_axis_label='years', title='Coding Experience by Developer Type')
plot.hbar(y=dev_types, right=years_exp, height=0.9)

show(plot)

# SCATTER PLOT

from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.palettes import Dark2_5 as palette
import pickle

output_file('scatter.html')

# load data
with open('iris.pickle', 'rb') as f:
    iris = pickle.load(f)

# load sepal length and sepal width for all classes
sepal_length = iris['data'][:, 0]
sepal_width = iris['data'][:, 1]
classes = iris['target']

# separate data via class
setosa_sepal_length = sepal_length[classes == 0]
setosa_sepal_width = sepal_width[classes == 0]
versicolor_sepal_length = sepal_length[classes == 1]
versicolor_sepal_width = sepal_width[classes == 1]
virginica_sepal_length = sepal_length[classes == 2]
virginica_sepal_width = sepal_width[classes == 2]

fig = figure(x_axis_label='Sepal length (cm)', y_axis_label='Sepal width (cm)')
fig.circle(setosa_sepal_length, setosa_sepal_width, color=palette[0], legend='setosa')
# plot versicolor sepal length v. width
fig.circle(versicolor_sepal_length, versicolor_sepal_width, color=palette[1], legend='versicolor')
# plot virginica sepal length v. width
fig.circle(virginica_sepal_length, virginica_sepal_width, color=palette[2], legend='virginica')

show(fig)

# PANNING

from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.layouts import row, column, gridplot
from bokeh.palettes import Dark2_5 as palette
import pickle

output_file('panning.html')

# load data
with open('iris.pickle', 'rb') as f:
    iris = pickle.load(f)

# load all features for all classes
sepal_length = iris['data'][:, 0]
sepal_width = iris['data'][:, 1]
petal_length = iris['data'][:, 2]
petal_width = iris['data'][:, 3]
classes = iris['target']

# separate features via class
setosa_sepal_length = sepal_length[classes == 0]
setosa_sepal_width = sepal_width[classes == 0]
setosa_petal_length = petal_length[classes == 0]
setosa_petal_width = petal_width[classes == 0]

versicolor_sepal_length = sepal_length[classes == 1]
versicolor_sepal_width = sepal_width[classes == 1]
versicolor_petal_length = petal_length[classes == 1]
versicolor_petal_width = petal_width[classes == 1]

virginica_sepal_length = sepal_length[classes == 2]
virginica_sepal_width = sepal_width[classes == 2]
virginica_petal_length = petal_length[classes == 2]
virginica_petal_width = petal_width[classes == 2]

# sepal length v. sepal width
fig1 = figure(x_axis_label='Sepal length (cm)', y_axis_label='Sepal width (cm)')
fig1.circle(setosa_sepal_length, setosa_sepal_width, color=palette[0], legend='setosa')
fig1.circle(versicolor_sepal_length, versicolor_sepal_width, color=palette[1], legend='versicolor')
fig1.circle(virginica_sepal_length, virginica_sepal_width, color=palette[2], legend='virginica')

# sepal length v. petal length
fig2 = figure(x_axis_label='Sepal length (cm)', y_axis_label='Petal length (cm)', x_range=fig1.x_range)
fig2.circle(setosa_sepal_length, setosa_petal_length, color=palette[0], legend='setosa')
fig2.circle(versicolor_sepal_length, versicolor_petal_length, color=palette[1], legend='versicolor')
fig2.circle(virginica_sepal_length, virginica_petal_length, color=palette[2], legend='virginica')

show(column(fig1, fig2))

# MULTIPLOTS

from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.layouts import row, column, gridplot
from bokeh.palettes import Dark2_5 as palette
import pickle

output_file('multiplot.html')

# load data
with open('iris.pickle', 'rb') as f:
    iris = pickle.load(f)

# load all features for all classes
sepal_length = iris['data'][:, 0]
sepal_width = iris['data'][:, 1]
petal_length = iris['data'][:, 2]
petal_width = iris['data'][:, 3]
classes = iris['target']

# separate features via class
setosa_sepal_length = sepal_length[classes == 0]
setosa_sepal_width = sepal_width[classes == 0]
setosa_petal_length = petal_length[classes == 0]
setosa_petal_width = petal_width[classes == 0]

versicolor_sepal_length = sepal_length[classes == 1]
versicolor_sepal_width = sepal_width[classes == 1]
versicolor_petal_length = petal_length[classes == 1]
versicolor_petal_width = petal_width[classes == 1]

virginica_sepal_length = sepal_length[classes == 2]
virginica_sepal_width = sepal_width[classes == 2]
virginica_petal_length = petal_length[classes == 2]
virginica_petal_width = petal_width[classes == 2]

fig1 = figure(x_axis_label='Sepal length (cm)', y_axis_label='Sepal width (cm)')
fig1.circle(setosa_sepal_length, setosa_sepal_width, color=palette[0], legend='setosa')
fig1.circle(versicolor_sepal_length, versicolor_sepal_width, color=palette[1], legend='versicolor')
fig1.circle(virginica_sepal_length, virginica_sepal_width, color=palette[2], legend='virginica')

fig2 = figure(x_axis_label='Petal length (cm)', y_axis_label='Petal width (cm)')
fig2.circle(setosa_petal_length, setosa_petal_width, color=palette[0], legend='setosa')
fig2.circle(versicolor_petal_length, versicolor_petal_width, color=palette[1], legend='versicolor')
fig2.circle(virginica_petal_length, virginica_petal_width, color=palette[2], legend='virginica')

# sepal length v. petal length
fig3 = figure(x_axis_label='Sepal length (cm)', y_axis_label='Petal length (cm)')
fig3.circle(setosa_sepal_length, setosa_petal_length, color=palette[0], legend='setosa')
fig3.circle(versicolor_sepal_length, versicolor_petal_length, color=palette[1], legend='versicolor')
fig3.circle(virginica_sepal_length, virginica_petal_length, color=palette[2], legend='virginica')

# sepal width v. petal width
fig4 = figure(x_axis_label='Sepal width (cm)', y_axis_label='Petal width (cm)')
fig4.circle(setosa_sepal_width, setosa_petal_width, color=palette[0], legend='setosa')
fig4.circle(versicolor_sepal_width, versicolor_petal_width, color=palette[1], legend='versicolor')
fig4.circle(virginica_sepal_width, virginica_petal_width, color=palette[2], legend='virginica')

show(gridplot([[fig1, fig2], [fig3, fig4]]))
