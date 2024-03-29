# -*- coding: utf-8 -*-
"""Fraud Detection

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1giCQStaprlwgKM9plvGGaODNbw0VqBv-
"""

import numpy as np #matrixes
import sklearn as sk #prediction models
import pandas as pd #data processing
import matplotlib.pyplot as plt #plot graphs
from sklearn.preprocessing import scale
import random
import seaborn as sns #interactive graphs
import matplotlib.gridspec as gridspec

df = pd.read_csv('creditcard.csv', low_memory=True)
df = df.sample(frac=1).reset_index(drop=True)
df.head()

#Check the amounts of fraudulant and normal transactions
fraud = df.loc[df['Class'] == 1]
non_frauds = df.loc[df['Class'] == 0]
print(len(fraud))
print(len(non_frauds))

# Scatter plot to see the 'Amounts' relation between the Fraud and Normal transactions
ax = fraud.plot.scatter(x='Amount', y='Class', color='Orange', label='Fraud')
non_frauds.plot.scatter(x='Amount', y='Class', color='Blue', label = 'Normal', ax=ax)
plt.show()

# Plot all features using the histograms
df.hist(figsize=(20,20))
plt.show()

#Plot the dollar 'Amount' to see the relation between normal and fraud transactions
plt.figure(figsize=(14,6))
plt.subplot(1,2,1)
fraud.Amount.plot.hist(title="Fraud Transaction" , color = 'red')
plt.subplot(1,2,2)
non_frauds.Amount.plot.hist(title="Normal Transaction", color = "blue")

#Plot heatmap to see correlation between the V parameters
corr = df.corr()
fig = plt.figure(figsize = (24,8))
sns.heatmap(corr, vmax = 0.5, square = True)

#get all the V features
v_features = df.iloc[:,1:29].columns
#plot histograms of the v features for fraud and normal transactions and check the differences to signify importance for inferences
plt.figure(figsize=(12,28*4))
gs = gridspec.GridSpec(28,1)
for i, cn in enumerate(df[v_features]):
  ax = plt.subplot(gs[i])
  sns.distplot(df[cn][df.Class == 1], bins=50, label = "Fraud", color = "red")
  sns.distplot(df[cn][df.Class == 0], bins=50, label = "Normal", color = "green")
  ax.legend()
  ax.set_xlabel('')
  ax.set_title('histogram of feature: '+cn)
plt.show()

#Data Preprocessing 
#Drop the time column since it will not be used in the model
df = df.drop(['Time'], axis=1)
df.head()



from google.colab import drive
drive.mount('/content/drive')

#Machine Learning imports

from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

#Create x and y variables using the features and the class column
x = df.iloc[:, :-1]
y = df['Class']
print(x.shape)
print(y.shape)

#Standardize the data so that it is at the same scale and it is normally distributed for better prediction
scaler = StandardScaler()
scaler.fit(x)

#Split the data using 'train_test_split' function
X_train, X_test, y_train, y_test = train_test_split( x, y, test_size=0.3)

#Logistic Regression model 
# create and configure model
logistic = linear_model.LogisticRegression(C=1e5)
logistic.fit(X_train, y_train)
print('Score:', (logistic.score(X_test, y_test))*100,"%")

y_predicted = np.array(logistic.predict(X_test))
print(y_predicted)

#Print the classification report
from sklearn.metrics import classification_report
print(classification_report(y_test, y_predicted))

print(y_predicted)

from sklearn.metrics import confusion_matrix, classification_report
from sklearn.metrics import confusion_matrix

print(confusion_matrix(y_test, y_pred.round()))

#Random Forest Classifier

from sklearn.ensemble import RandomForestClassifier
# train model
rforest = RandomForestClassifier(n_estimators=100).fit(X_train, y_train)
#predict on test set 
rforest_pred = rforest.predict(X_test)
print(rforest_pred)

print(confusion_matrix(y_test, rforest_pred.round()))

#31 False Positive from the random forest classifier compared to the 62 from logistic regression. Random Forest Classifier is better in this situation.

#Oversampling to handle imbalanced datasets
from sklearn.utils import resample

#Separate input features and target
y = df.Class
X = df.drop('Class', axis=1)

# concatenate our training data back together
X = pd.concat([X_train, y_train], axis=1)

#separate minority and majority classes
not_fraud = X[X.Class==0]
fraud = X[X.Class==1]

#upsample minority
fraud_upsampled = resample(fraud, 
                           replace=True, #sample with replacement
                           n_samples=len(not_fraud), #match number in majority class
                           random_state=27) #reproducible results

# combine majority and unsampled minority
upsampled = pd.concat([not_fraud, fraud_upsampled])

#check new class counts
upsampled.Class.value_counts()

#try logistic regression with balanced dataset
y_train = upsampled.Class
X_train = upsampled.drop('Class', axis=1)
upsampled_lr = LogisticRegression().fit(X_train, y_train)
upsampled_pred = upsampled_lr.predict(X_test)

print(confusion_matrix(y_test, upsampled_pred.round()))

#try Random Forest Classifier
upsampled_rf = RandomForestClassifier(n_estimators=10).fit(X_train, y_train)
#Predict on Test Set
upsampled_rf_pred = upsampled_rf.predict(X_test)

print(confusion_matrix(y_test, upsampled_rf_pred.round()))

#Using the Over-samping, the logistic regression classifier seems to do better as there are 12 false positives in comparison to 33 for the Random Forest classifier. This is also much better than without over-sampling.

#Informed Over Sampling: Synthetic Minority Over-sampling Technique
#Import SMOTE
from imblearn.over_sampling import SMOTE 

#Separate input features and target
y = df.Class
X = df.drop('Class', axis=1)

#Setting up testing and training sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state=27)

sm = SMOTE(random_state=27, ratio=1.0)
X_train, y_train = sm.fit_sample(X_train, y_train)

#Try Logistic Regression with the balanced dataset
smote_lr = LogisticRegression().fit(X_train, y_train)
smote_pred_lr = smote_lr.predict(X_test)

print(confusion_matrix(y_test, smote_pred_lr.round()))

#try Random Forest classifier with 
smote_rf = RandomForestClassifier(n_estimators=10).fit(X_train, y_train)
#Predict on the test set 
smote_rf_pred = smote_rf.predict(X_test)

print(confusion_matrix(y_test, smote_rf_pred.round()))

#Using the Synthetic minority over-sampling technique, the logistic regression classifier seems to do better as there are 12 false positives in comparison to 28 for the Random Forest classifier.