from content_base import content_based_recommend
from collaborative_filter import cf_model, ratings

def recommend_for_user(user_id):
    # Get all books rated by User with ID is user_id
    rated_books = ratings[ratings['UserID'] == user_id]['BookID'].tolist()
    
    # Get similar books using content-based filtering
    recommended_books = set()
    for book in rated_books:
        similar_books = content_based_recommend(book, 2)
        recommended_books.update(similar_books)

    # Remove books already rated by User 
    recommended_books = [b for b in recommended_books if b not in rated_books]

    # Predict ratings for each recommended book
    predicted_ratings = [(book, cf_model.pred(1, book, normalized=0)) for book in recommended_books]
    
    # Sort books by predicted rating in descending order
    sorted_books = sorted(predicted_ratings, key=lambda x: x[1], reverse=True)

    return sorted_books