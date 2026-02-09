# 🎬 Movie Recommendation System

A content-based movie recommendation system built using **Machine Learning and NLP**, deployed with **Streamlit**.


## 📌 Project Overview
This project recommends movies similar to a selected movie based on movie metadata such as **genres, keywords, cast, and crew**.  
It uses Natural Language Processing techniques and **cosine similarity** to measure similarity between movies.

## 🚀 Features
- Content-based movie recommendation
- NLP-based text vectorization using CountVectorizer
- Cosine similarity for measuring movie similarity
- Interactive and user-friendly Streamlit web interface
- Displays total number of available movies
- Easy to extend with new features (posters, APIs, deployment)

## 🧠 How It Works
1. Movie metadata is cleaned and preprocessed.
2. Important features (genres, keywords, cast, crew) are combined into a single text column.
3. Text data is converted into numerical vectors using **CountVectorizer**.
4. **Cosine similarity** is calculated between all movies.
5. The top 5 most similar movies are recommended.
6. The trained model is deployed using Streamlit.


## 🛠️ Tech Stack
- Python  
- Pandas  
- NumPy  
- Scikit-learn  
- Natural Language Processing (NLP)  
- Streamlit  


## 📂 Project Structure
