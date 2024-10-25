import pandas as pd
import numpy as np

from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from matplotlib import pyplot as plt


flights = pd.read_csv('flights.csv', index_col=False).dropna()
# features (X)
airline_encoder = LabelEncoder()
flights['AIRLINE_ID'] = airline_encoder.fit_transform(flights['AIRLINE_ID'])
features = [
    flights['AIR_TIME'],
    flights['DISTANCE'],
    #flights['AIRLINE_ID']
]

X = pd.concat(features, axis=1)

# is this flight arriving late? (y - binary values)
y = ((flights['ARR_TIME'] - flights['CRS_ARR_TIME']) > 30) & ((flights['ARR_TIME'] - flights['CRS_ARR_TIME']) < 2000)
y = y.astype(np.uint8)
X_train, X_test, y_train, y_test = train_test_split(X, y)

# training the classifier
naive_bayes = GaussianNB()
naive_bayes.fit(X_train, y_train)

# evaluating the classifier
y_pred = naive_bayes.predict(X_test)
print(accuracy_score(y_test, y_pred))

# plotting test data
plt.scatter(X_test.iloc[:,0], X_test.iloc[:,1], c=y_pred, cmap='Dark2')
plt.colorbar()
plt.title('Late Flights Given Air Time and Distance of Flight')
plt.xlabel('Air Time (min)')
plt.ylabel('Distance (mi)')
plt.show()
