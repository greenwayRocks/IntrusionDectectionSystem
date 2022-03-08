#!/usr/bin/env python3
import os

spam_emails_path = os.path.join("spam_emails_data", "spam")
ham_emails_path = os.path.join("spam_emails_data", "ham")
labeled_file_directories = [(spam_emails_path, 0), (ham_emails_path, 1)]

email_corpus = []
labels = []

for class_files, label in labeled_file_directories:
    files = os.listdir(class_files)
    for file in files:
        file_path = os.path.join(class_files, file)
        try:
            with open(file_path, "r") as currentFile:
                email_content = currentFile.read().replace("\n", "")
                email_content = str(email_content)
                email_corpus.append(email_content)
                labels.append(label)
        except:
            pass

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    email_corpus, labels, test_size=0.2, random_state=11
)

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import HashingVectorizer, TfidfTransformer
from sklearn import tree

model = Pipeline(
    [
        ("vect", HashingVectorizer(input="content", ngram_range=(1, 3))),
        ("tfidf", TfidfTransformer(use_idf=True,)),
        ("dt", tree.DecisionTreeClassifier(class_weight="balanced")),
    ]
)
model.fit(X_train, y_train)

# save model using joblib
# from sklearn.externals import joblib
import joblib

joblib.dump(model, 'spam_model')

# load saved model
newModel = joblib.load('spam_model')
print(X_test)
y_test_pred = newModel.predict(X_test)

# accuracy and matrix
from sklearn.metrics import accuracy_score, confusion_matrix
print(y_test_pred)
print(accuracy_score(y_test, y_test_pred))
print(confusion_matrix(y_test, y_test_pred))
