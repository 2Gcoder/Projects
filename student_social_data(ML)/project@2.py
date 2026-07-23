import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

# Loading dataset
df = pd.read_csv(
    "C:/Users/Gaurav Gupta/Desktop/python/project/student_performance.csv"
)

# Convert grades to Pass/Fail --> (A,B,C) == PASS and (D,E) == fail
df['result'] = df['grade'].apply(
    lambda x: 1 if x in ['A', 'B', 'C'] else 0
)

# Features
features = [
    'weekly_self_study_hours',
    'attendance_percentage',
    'total_score',
    'class_participation'
]

X = df[features]
Y = df['result']

# Train-test split
X_train, X_test, Y_train, Y_test = train_test_split(
    X,
    Y,
    test_size=0.25,
    random_state=42
)

# Scaling
scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Model
model = LogisticRegression(max_iter=5000)
model.fit(X_train, Y_train)

# Prediction
Y_pred = model.predict(X_test)

# Classification report
print(
    classification_report(
        Y_test,
        Y_pred,
        target_names=['Fail', 'Pass']
    )
)

# Confusion Matrix
cm = confusion_matrix(Y_test, Y_pred)

plt.figure(figsize=(8, 6))

sns.heatmap(
    cm,
    annot=True,
    fmt='d',
    cmap='Blues',
    xticklabels=['Fail', 'Pass'],
    yticklabels=['Fail', 'Pass']
)

plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.show()

# ---------------- User Prediction ----------------

print("\n------ Enter Student Details ------")

weekly_self_study_hours = float(
    input("weekly_self_study_hours: ")
)

attendance_percentage = float(
    input("attendance_percentage: ")
)

total_score = float(
    input("total_score: ")
)

class_participation = float(
    input("class_participation: ")
)

user_data = pd.DataFrame([{
    "weekly_self_study_hours": weekly_self_study_hours,
    "attendance_percentage": attendance_percentage,
    "total_score": total_score,
    "class_participation": class_participation
}])

user_scaled = scaler.transform(user_data)

prediction = model.predict(user_scaled)

result = "Pass" if prediction[0] == 1 else "Fail"

print("\nPredicted Result:", result)