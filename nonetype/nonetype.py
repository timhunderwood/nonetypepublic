import datetime
from typing import Dict, NamedTuple
from flask import Flask, render_template

app = Flask(__name__)

# mapping article id --> article properties

Article = NamedTuple(
    "Article", [("id", str), ("title", str), ("date", str), ("visible", bool)]
)

ARTICLES: Dict[str, Article] = {

    "0002": Article(
        id="0002",
        title="Another example article",
        date="2019-10-17",
        visible=True
    ),
    "0001": Article(
        id="0001",
        title="Example unfinished article",
        date="2019-10-15",
        visible=True
    ),
    "0000": Article(
        id="0000",
        title="Example article 1",
        date="2019-10-14",
        visible=True,
    ),
}


def article_sorter(article: Article):
    """Defines the order in which articles are displayed on the article page."""
    date: str = article.date
    return datetime.datetime.strptime(date, "%Y-%m-%d")


# Sort articles by date (even if they are in the wrong order in above dictionary)
ARTICLES = {
    article.id: article
    for article in sorted(ARTICLES.values(), key=article_sorter, reverse=True)
}


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", articles=ARTICLES)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/articles/<article_id>")
def article(article_id):
    article = ARTICLES[article_id]
    return render_template(f"articles/article_{article_id}.html", article=article)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(e):
    return render_template("404.html"), 500


if __name__ == "__main__":
    app.run()
