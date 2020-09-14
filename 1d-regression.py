'''
Created on Dec 7, 2017

@author: joigno
'''

print(__doc__)


# Code source: Jaques Grobler
# License: BSD 3 clause

from math import log

import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score

from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

diabetes = np.genfromtxt ('data/wineries-factors.csv', delimiter=",")
print diabetes



diabetes_target = diabetes[:, np.newaxis, 5]
loger = lambda t: log(t) 
vfunc = np.vectorize(loger)
#diabetes_target = vfunc(diabetes_target)
print diabetes_target
# Load the diabetes dataset
#diabetes = datasets.load_diabetes()
print diabetes.__class__


# Use only one feature
diabetes_X = diabetes[:, np.newaxis, 8]

# Split the data into training/testing sets
diabetes_X_train = diabetes_X#[:-len(diabetes_X)/2]
diabetes_X_test = diabetes_X#[-len(diabetes_X)/2:]

# Split the targets into training/testing sets
diabetes_y_train = diabetes_target#[:-len(diabetes_X)/2]
diabetes_y_test = diabetes_target#[-len(diabetes_X)/2:]

# Create linear regression object
regr = linear_model.LinearRegression()
#regr = make_pipeline(PolynomialFeatures(degree=2), Ridge())

# Train the model using the training sets
regr.fit(diabetes_X_train, diabetes_y_train)

# Make predictions using the testing set
diabetes_y_pred = regr.predict(diabetes_X_test)

# The coefficients
#print('Coefficients: \n', regr.coef_)
print('Coefficients: \n', regr)
# The mean squared error
print("Mean squared error: %.2f"
      % mean_squared_error(diabetes_y_test, diabetes_y_pred))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % r2_score(diabetes_y_test, diabetes_y_pred))

# Plot outputs
plt.scatter(diabetes_X_test, diabetes_y_test,  color='black')
plt.plot(diabetes_X_test, diabetes_y_pred, color='blue', linewidth=3)

plt.xticks(())
plt.yticks(())

plt.show()
