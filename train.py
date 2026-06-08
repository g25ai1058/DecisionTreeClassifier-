from sklearn.datasets import fetch_olivetti_faces
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import joblib

# Load Olivetti Faces dataset
faces = fetch_olivetti_faces()

X = faces.data
y = faces.target

# Split data into 70% training and 30% testing
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.30,
    random_state=42,
    stratify=y
)

# Create and train Decision Tree model
model = DecisionTreeClassifier(random_state=42)
model.fit(X_train, y_train)

# Save trained model
joblib.dump(model, "savedmodel.pth")

print("Model trained successfully.")
print("Model saved as 'savedmodel.pth'")
print(f"Training samples: {len(X_train)}")
print(f"Testing samples: {len(X_test)}")