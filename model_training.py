import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from data_preprocessing import load_and_preprocess_data

def build_model(input_shape, num_classes):
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(num_classes, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

def train_model():
    X_train, X_test, y_train, y_test = load_and_preprocess_data()
    model = build_model(input_shape=(224, 224, 3), num_classes=len(set(y_train)))
    
    model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, batch_size=32)
    model.save("models/crop_disease_model.h5")
    print("Model training complete and saved!")

if __name__ == "__main__":
    train_model()
