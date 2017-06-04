import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, metrics, linear_model, naive_bayes, neighbors, tree, svm, neural_network
import csv
from freq_reaper import FreqReaper
import pandas as pandas

freq_reaper = FreqReaper()

X = pandas.read_csv('all_features.csv')
X_append = freq_reaper.runAll()
X = np.hstack((X, X_append))
y = pandas.read_csv('all_outcomes.csv')

y = y['label']

X_test = X[X.shape[0] - 41: X.shape[0] - 1][:]
y_test = y[len(y) - 41:len(y) - 1]

X = X[: X.shape[0] - 41][:]
y = y[:len(y) - 41]

# LOGISTIC REGRESSION

# fit a logistic regression model to the data
logistic = linear_model.LogisticRegression()
logistic.fit(X,y)
print(logistic)

# make predictions
expected = y
predicted = logistic.predict(X)

# summarize the fit of the model
print(metrics.classification_report(expected, predicted))
print(metrics.confusion_matrix(expected, predicted))

expected = y_test
predicted = logistic.predict(X_test)
print(metrics.classification_report(expected, predicted))
print(metrics.confusion_matrix(expected, predicted))


# GAUSSIAN NAIVE BAYES

# fit a Naive Bayes model to the data
gaussian = naive_bayes.GaussianNB()
gaussian.fit(X, y)
print(gaussian)

# make predictions
expected = y
predicted = gaussian.predict(X)

# summarize the fit of the model
print(metrics.classification_report(expected, predicted))
print(metrics.confusion_matrix(expected, predicted))

expected = y_test
predicted = gaussian.predict(X_test)
print(metrics.classification_report(expected, predicted))
print(metrics.confusion_matrix(expected, predicted))


# K-NEAREST NEIGHBORS

# fit a k-nearest neighbor model to the data
k_neighbors = neighbors.KNeighborsClassifier()
k_neighbors.fit(X, y)
print(k_neighbors)

# make predictions
expected = y
predicted = k_neighbors.predict(X)

# summarize the fit of the model
print(metrics.classification_report(expected, predicted))
print(metrics.confusion_matrix(expected, predicted))

expected = y_test
predicted = k_neighbors.predict(X_test)
print(metrics.classification_report(expected, predicted))
print(metrics.confusion_matrix(expected, predicted))


# DECISION TREE CLASSIFIER

# fit a CART model to the data
decision_tree = tree.DecisionTreeClassifier()
decision_tree.fit(X, y)
print(decision_tree)

# make predictions
expected = y
predicted = decision_tree.predict(X)

# summarize the fit of the model
print(metrics.classification_report(expected, predicted))
print(metrics.confusion_matrix(expected, predicted))

expected = y_test
predicted = decision_tree.predict(X_test)
print(metrics.classification_report(expected, predicted))
print(metrics.confusion_matrix(expected, predicted))


# SUPPORT VECTOR MACHINES

# fit a SVM model to the data
svm = svm.SVC()
svm.fit(X, y)
print(svm)

# make predictions
expected = y
predicted = svm.predict(X)

# summarize the fit of the model
print(metrics.classification_report(expected, predicted))
print(metrics.confusion_matrix(expected, predicted))

expected = y_test
predicted = svm.predict(X_test)
print(metrics.classification_report(expected, predicted))
print(metrics.confusion_matrix(expected, predicted))


#NEURAL NETWORK

nn = neural_network.MLPClassifier()
nn.fit(X, y)
print(nn)

# make predictions
expected = y
predicted = nn.predict(X)

# summarize the fit of the model
print(metrics.classification_report(expected, predicted))
print(metrics.confusion_matrix(expected, predicted))

expected = y_test
predicted = nn.predict(X_test)
print(metrics.classification_report(expected, predicted))
print(metrics.confusion_matrix(expected, predicted))