from fastapi import FastAPI
from recommend import recommend_for_user
from content_base import content_based_recommend
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow requests from specific ports (e.g., frontend on localhost:3000)
origins = [
    "http://localhost:9000", 
    "http://127.0.0.1:9000", 
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # origins allowed to make requests
    allow_credentials=True,
    allow_methods=["*"],    # allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],    # allow all headers
)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}

@app.get("/recommend/{user_id}")
def get_recommendations(user_id: str):
    recommendations = recommend_for_user(user_id, 10)

    # Convert recommendations (tuples) to a list of dictionaries
    recommendations_dict = [
        {"book_id": str(rec[0]), "predicted_rating": float(rec[1])}
        for rec in recommendations
    ]
    
    return {"user_id": user_id, "recommendations": recommendations_dict}

@app.get("/recommend/book/{book_id}")
def get_book_recommendations(book_id: str):
    recommendations = content_based_recommend(book_id, 6)
    return {"book_id": book_id, "recommendations": recommendations}