import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

data = pd.read_csv("data.csv", header=None)

X = data.iloc[:, :-1].values
y = data.iloc[:, -1].values

labels = list(set(y))
label_dict = {label:i for i, label in enumerate(labels)}

y = np.array([label_dict[label] for label in y])
y = to_categorical(y)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2
)

model = Sequential([
    Dense(128, activation='relu', input_shape=(42,)),
    Dense(64, activation='relu'),
    Dense(len(labels), activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.fit(X_train, y_train, epochs=30)

model.save("model/hand_model.h5")

with open("labels.txt", "w", encoding="utf-8") as f:
    for label in labels:
        f.write(label + "\n")