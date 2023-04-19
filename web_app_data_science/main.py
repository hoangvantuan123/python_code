import streamlit as st
from sklearn import datasets
st.title("Stramlit Example")

st.write("""
##Explore different classification

which one is the best?
""")
dataset_name = st.sidebar.selectbox(
    "Select Dataset", ("Iris", "Breast Cancer", "Wine dataset")
)
classifier_name = st.sidebar.selectbox(
    "Select Classifier", ("KNN", "SVM", "Random Normal"))


def get_dataset(dataset_name):
    if dataset_name == "Iris":
        data = datasets.load_iris()
    elif dataset_name == "Breast Cancer":
        data = datasets.load_breast_cancer()
    else:
        data = datasets.load_wine()