from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb://mongo:27017/")  

db = client["library"]
collection = db["books"]

@app.route("/")
def home():
    return "Ласкаво просимо до нашої бібліотеки! Приємного перегляду книжок."

@app.route("/books", methods=["GET"])
def get_books():
    books = []
    for book in collection.find():
        books.append({"_id": str(book["_id"]), "title": book["title"], "author": book["author"], "year": book["year"]})
    return jsonify(books)

@app.route("/book", methods=["POST"])
def add_book():
    data = request.get_json()
    title = data["title"]
    author = data["author"]
    year = data["year"]
    book = {"title": title, "author": author, "year": year}
    collection.insert_one(book)
    return "Книгу додано успішно!"

@app.route("/book/<id>", methods=["DELETE"])
def delete_book(id):
    collection.delete_one({"_id": ObjectId(id)})
    return "Книгу успішно видалено!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
 