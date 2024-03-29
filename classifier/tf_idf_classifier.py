# coding: utf-8
import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import train_test_split
import pickle
import numpy as np
import sys
from sklearn.metrics import confusion_matrix

label_dict = {1795:"Non Violent",1796:"Violent"}

def train():
    data = pd.read_csv("file.csv")
    
    labels = data["label"].unique()
    count_class_0, count_class_1 = data["label"].value_counts()
    df_class_0 = data[data['label'] == labels[0]]
    df_class_1 = data[data['label'] == labels[1]]

    df_class_1_over = df_class_1.sample(count_class_0, replace=True)
    df_test_over = pd.concat([df_class_0, df_class_1_over], axis=0)

    print('Random over-sampling:')
    print(df_test_over.label.value_counts())
    
    X = df_test_over["text"]
    y = df_test_over["label"]


    #print(y.value_counts())
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(X_train)
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
    print(X_train_tfidf.shape)
    clf = MultinomialNB().fit(X_train_tfidf, y_train)
    
    X_test_counts = count_vect.transform(X_test)
    X_test_tfidf = tfidf_transformer.transform(X_test_counts)
    predicted = clf.predict(X_test_tfidf)
    print(np.mean(predicted == y_test))
    print(confusion_matrix(y_test, predicted))
    save_data = {"count_vec":count_vect,"tfidf_transformer":tfidf_transformer,"clf_model":clf}

    with open("classifier.model","wb") as outfile:
        pickle.dump(save_data,outfile)

def predict(sentence):
    with open("classifier.model","rb") as infile:
        model_data = pickle.load(infile)


    count_vect = model_data["count_vec"]
    tfidf_transformer = model_data["tfidf_transformer"]
    clf = model_data["clf_model"]
    X_test_counts = count_vect.transform([sentence])
    X_test_tfidf = tfidf_transformer.transform(X_test_counts)
    predicted = clf.predict(X_test_tfidf)[0]
    predicted_value = label_dict[predicted]
    return(predicted_value)


if __name__ == "__main__":
    if sys.argv[1] == "predict":
        predicted = predict(sys.argv[1])
        print(predicted)
    else:
        train()

