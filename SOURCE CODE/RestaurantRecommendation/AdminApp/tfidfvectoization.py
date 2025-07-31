from sklearn.feature_extraction.text import TfidfVectorizer

# Sample documents
documents = [
    "The cat sat on the mat.",
    "The dog sat on the mat."
]

# Initialize the TfidfVectorizer
vectorizer = TfidfVectorizer()

# Fit and transform the documents into a TF-IDF matrix
tfidf_matrix = vectorizer.fit_transform(documents)

# Display the TF-IDF scores
print(tfidf_matrix.toarray())

# Get the words corresponding to the columns
print(vectorizer.get_feature_names_out())
