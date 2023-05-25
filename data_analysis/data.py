import numpy as np
from numpy.linalg import inv
import scipy.io

# Load Facebook dataset
dataFb = scipy.io.loadmat('Facebook.mat')['dataFb']

# Randomly permute the data
idx = np.random.permutation(dataFb.shape[0])
dataFb = dataFb[idx]

# Split dataset into train and test set
train_idx, _, test_idx = np.split(np.arange(dataFb.shape[0]), [int(dataFb.shape[0] * 0.9), int(dataFb.shape[0] * 0.1)])
trainset = dataFb[train_idx]
testset = dataFb[test_idx]

# Split the training set into k=5 folds
k = 5
foldsize = trainset.shape[0] // k

# Predefine RMSE size
RMSE = np.zeros((k, 12))
RMSE_test = np.zeros((k, 12))

for clas in range(7, 19):
    trainsize = 0
    for fold in range(k):
        trainsize += foldsize
        b = trainset[:trainsize, clas]
        x = trainset[:trainsize, :7]
        A = np.column_stack((np.ones(x.shape[0]), x))
        xhat = inv(A.T @ A) @ A.T @ b

        Y_test = testset[:, clas]
        x_test = testset[:, :7]
        X_test = np.column_stack((np.ones(x_test.shape[0]), x_test))
        y_pred = np.zeros(b.shape)
        y_test_pred = np.zeros(Y_test.shape)

        for i in range(A.shape[1]):
            y_pred += xhat[i] * A[:, i]
            y_test_pred += xhat[i] * X_test[:, i]

        RMSE[fold, clas - 7] = np.sqrt(np.mean((y_pred - b) ** 2))
        RMSE_test[fold, clas - 7] = np.sqrt(np.mean((y_test_pred - Y_test) ** 2))

    # Print results for each class
    print(f"Facebook Dataset - Class {clas}")
    for fold in range(k):
        print(f"Fold {fold + 1}:")
        print(f"  Train RMSE: {RMSE[fold, clas - 7]}")
        print(f"  Test RMSE: {RMSE_test[fold, clas - 7]}")
    print()

# Load Wine types dataset
winedata = scipy.io.loadmat('wine_type.mat')
winedataset = np.column_stack((winedata['x'], winedata['y']))

# Randomly split the dataset into train and test set
train_idx, _, test_idx = np.split(np.arange(winedataset.shape[0]), [int(winedataset.shape[0] * 0.83), int(winedataset.shape[0] * 0.17)])
trainset = winedataset[train_idx]
testset = winedataset[test_idx]

# Split the training set into k=4 folds
k = 4
foldsize = trainset.shape[0] // k

RMSE = np.zeros(k)
RMSE_test = np.zeros(k)
train_accuracy = np.zeros(k)
test_accuracy = np.zeros(k)

trainsize = 0
for fold in range(k):
    trainsize += foldsize
    b = trainset[:trainsize, 13]
    x = trainset[:trainsize, :13]
    A = np.column_stack((np.ones(x.shape[0]), x))
    xhat = inv(A.T @ A) @ A.T @ b

    Y_test = testset[:, 13]
    x_test = testset[:, :13]
    X_test = np.column_stack((np.ones(x_test.shape[0]), x_test))
    y_pred = np.zeros(b.shape)
    y_test_pred = np.zeros(Y_test.shape)

    for i in range(A.shape[1]):
        y_pred += xhat[i] * A[:, i]
        y_test_pred += xhat[i] * X_test[:, i]

    RMSE[fold] = np.sqrt(np.mean((y_pred - b) ** 2))
    RMSE_test[fold] = np.sqrt(np.mean((y_test_pred - Y_test) ** 2))

    y_pred = np.round(y_pred)
    train_accuracy[fold] = np.sum(y_pred == b) / len(b)
    y_test_pred = np.round(y_test_pred)
    test_accuracy[fold] = np.sum(y_test_pred == Y_test) / len(Y_test)

# Print results for Wine Types dataset
print("Wine Types Dataset")
for fold in range(k):
    print(f"Fold {fold + 1}:")
    print(f"  Train RMSE: {RMSE[fold]}")
    print(f"  Test RMSE: {RMSE_test[fold]}")
    print(f"  Train Accuracy: {train_accuracy[fold]}")
    print(f"  Test Accuracy: {test_accuracy[fold]}")
    print()