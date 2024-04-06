from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

anime_data = pd.read_csv("anime-list.csv")
anime_data["synopsis"] = anime_data["synopsis"].fillna("")

anime_names = anime_data["name"].tolist()
anime_plots = anime_data["synopsis"].tolist()



def find_similar_plots(selected_anime_name):
    selected_index = None
    for i, name in enumerate(anime_names):
        if selected_anime_name.lower() in name.lower():
            selected_index = i
            break

    if selected_index is None:
        return "Anime bulunamadı. Lütfen tekrar deneyin."
        

    selected_plot = anime_plots[selected_index]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(anime_plots)

    selected_tfidf = vectorizer.transform([selected_plot])

    similarities = cosine_similarity(selected_tfidf, tfidf_matrix)

    similar_anime_indices = similarities.argsort(axis=1)[0][:-1]

    similar_anime_names = []
    count = 0
    for index in similar_anime_indices[::-1]:
        similar_anime_name = anime_names[index]
        if selected_anime_name.lower() not in similar_anime_name.lower():
            similar_anime_names.append(similar_anime_name)
            count += 1
            if count >= 5:
                break
    return similar_anime_names


def benzeranime(name):
    out=find_similar_plots(name)
    out=", ".join(out)
    return out
