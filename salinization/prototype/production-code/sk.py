from typing import Tuple

from sklearn.datasets import load_digits
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, accuracy_score

from matplotlib import pyplot as plt
import numpy as np

# read data
def load_data(filename: str=None) -> Tuple[np.ndarray, np.ndarray]:
    digits = load_digits()

    data = digits['data']
    target = digits['target']

    return data, target

data, target = load_data()

# split train and test data
x_train = data[:1500]
x_test = data[1500:]

y_train = target[:1500]
y_test = target[1500:]

# modeling
model = LogisticRegression()
model.fit(x_train, y_train)

# prediction
prediction = model.predict(x_test)

# metrics
cm = confusion_matrix(y_test, prediction)
a = accuracy_score(y_test, prediction)

# plot
fig, ax = plt.subplots()

colorbar = ax.matshow(cm)
fig.colorbar(colorbar)
fig.suptitle('Confusion')

fig.savefig('sklearn.png')

# How to run:
# 1. Start iPython in the working folder:
#       ipython
# 2. Execute the python file:
#       %run sk.py
# 3. Inspect variables as in Jupyter Notebook:
#       prediction
# 4. Exit iPython console:
#       quit()