# -------------------------------------------------------------------------
# AUTHOR: George Matta
# FILENAME: indexing.py
# SPECIFICATION: creates a Document-Term matrix based on the contents of
# collection.csv
# FOR: CS 4250 - Assignment #1
# TIME SPENT: 1.5 hours
# -------------------------------------------------------------------------

# IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE
# SUCH AS numpy OR pandas. You have to work here only with standard arrays

# Importing some Python libraries
import csv
import math

# Reading the data in a csv file
documents: list[str] = []
with open('collection.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for i, row in enumerate(reader):
        if i > 0:  # Skip header
            documents.append(row[0])
doc_count = len(documents)

# Conducting stopword removal for pronouns/conjunctions.
# Hint: use a set to define your stopwords.
stop_words = {"i", "and", "she", "her", "they", "their", "and"}
for i in range(doc_count):
    fixed = [
        word.lower() for word in documents[i].split(" ")
        if word.lower() not in stop_words
    ]
    documents[i] = ' '.join(fixed)

# Conducting stemming.
# Hint: use a dictionary to map word variations to their stem.
stemming = {
  "loves": "love",
  "cats": "cat",
  "dogs": "dog"
}
for i in range(doc_count):
    fixed = []
    for word in documents[i].split(" "):
        if word in stemming.values():
            fixed.append(word.lower())
        if word in stemming:
            fixed.append(stemming[word])

    documents[i] = ' '.join(fixed)

# Identifying the index terms.
terms = list(stemming.values())
term_count = len(terms)

# Building the document-term matrix by using the tf-idf weights.
# Access via doc_term_matrix[doc_index][term_index]
doc_term_matrix = []

# tf
# Access via term_frequency[doc_index][term]
term_frequency = [dict.fromkeys(terms, 0.0) for _ in documents]
for doc_index, document in enumerate(documents):
    for term in (words := document.split(" ")):
        term_frequency[doc_index][term] += 1 / len(words)

# df
# Access via document_frequency[term]
document_frequency = dict.fromkeys(terms, 0)
for term in terms:
    for document in documents:
        if term in document:
            document_frequency[term] += 1

# idf
# Access via inverse_df[term]
inverse_df = {
    term: math.log(doc_count / document_frequency[term], 10) for term in terms
}

# tf-idf
for doc_index in range(doc_count):
    tf_idf = []
    for term_index in range(term_count):
        term = terms[term_index]
        tf_idf.append(term_frequency[doc_index][term] * inverse_df[term])
    doc_term_matrix.append(tf_idf)

# Printing the document-term matrix.
print("\t " + "\t".join(terms))
for doc_index in range(doc_count):
    print(f"d{str(doc_index + 1)}\t", end="")
    print(
        "\t".join(
            ['0' if not i else f'{i:.3f}' for i in doc_term_matrix[doc_index]]
        )
    )
"""
        love   cat     dog
d1      0       0.117   0
d2      0       0       0.088
d3      0       0.059   0.059
"""
