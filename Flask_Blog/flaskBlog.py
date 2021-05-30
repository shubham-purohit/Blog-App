from flask import Flask, render_template, url_for

app = Flask(__name__)

posts = [
    {
        "title": "The Imitation Game",
        "author": 'Agatha Christee',
        "date": "December 12, 1957",
        "content": "Body was found on the floor..."
    },
    {
        "title": "The Hounds of Baskerville",
        "author": "Sherlok Holmes",
        "date": "April 23, 1924",
        "content": "The Hound could pound..."
    }
]


@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html", posts=posts)


@app.route("/about")
def about_page():
    return render_template("about.html", title='About Page')


if __name__ == "__main__":
    app.run(debug=True)
