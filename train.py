# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
import pickle
df = pd.read_csv("spam-dataset.csv")
df.head()
# %%
df.groupby('Category').describe()
# %%
df['spam'] = df['Category'].apply(lambda x: 1 if x == 'spam' else 0)
# %%
df.head()

# %%
# slit data
X_train, X_val, y_train, y_val = train_test_split(df.Message, df.spam)

# %%
model = Pipeline([
    ('vectorizer', CountVectorizer()),
    ('nb', MultinomialNB())
])


# %%
# train
model.fit(X_train, y_train)


# %%
model.score(X_val, y_val) * 100


# %%
# export the model
# with open("model_pickle", "wb") as file:
#     pickle.dump(model, file)


# %%
# # test import
# with open('model_pickle', "rb") as f:
#     test_imported_model = pickle.load(f)


# %%
# test_imported_model.score(X_val, y_val) * 100
