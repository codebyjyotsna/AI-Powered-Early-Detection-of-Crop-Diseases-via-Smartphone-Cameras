import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split

DATASET_PATH = "data/plantvillage"
IMG_SIZE = 224

def load_and_preprocess_data():
    images = []
    labels = []
    classes = os.listdir(DATASET_PATH)

    for label, class_name in enumerate(classes):
        class_path = os.path.join(DATASET_PATH, class_name)
        for img_name in os.listdir(class_path):
            img_path = os.path.join(class_path, img_name)
            img = cv2.imread(img_path)
            img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
            images.append(img)
            labels.append(label)

    images = np.array(images) / 255.0  # Normalize
    labels = np.array(labels)
    return train_test_split(images, labels, test_size=0.2, random_state=42)

if __name__ == "__main__":
    X_train, X_test, y_train, y_test = load_and_preprocess_data()
    print(f"Training samples: {len(X_train)}, Testing samples: {len(X_test)}")
