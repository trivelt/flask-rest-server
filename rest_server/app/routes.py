from app import app, db


@app.route("/")
def main():
    return "It works!"
