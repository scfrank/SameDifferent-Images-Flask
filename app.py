import random

# from uuid import uuid4 # for user ids
import itertools

consequent_integers = itertools.count()  # for user ids

from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    request,
    make_response,
    session,
)
from file_management import get_images_labelling_list, write_new_row


app = Flask(__name__)
app.secret_key = b"--a]a1k?qOd#=/VLc2*I0M6[y"

# image_list = list()
#bird_count = 0


@app.route("/")
def index():
    session["number"] = consequent_integers.__next__()
    session["bird_count"] = 0
    session["image_list"] = []
    return render_template("home.html")


@app.route("/birds", methods=["POST"])
def save_birds():
    response = make_response(redirect(url_for("birds")))
    # Saves labels to CSV file
    response_dict = dict(request.form.items())  # request the POST-ed info
    # print(labelledDict)
    write_new_row(
        response_dict, session_id=session["number"]
    )  # make sure this format works
    #global bird_count
    session["bird_count"] += 1
    return response


@app.route("/birds")
def birds():
    #global image_list  # pairs of bird files
    if len(session["image_list"]) == 0:
        session["image_list"] = get_images_labelling_list()  # default length=100
    #else:
    #    print(f"Images Left: {len(image_list) - bird_count}")
    try:
        f1, f2 = session["image_list"][session["bird_count"]]  # image pairs to rate
        if random.random() > 0.5:
            f1, f2 = f2, f1
        return render_template(
            "birds.html",
            image1=f1,
            image2=f2,
        )  # can add more options here if necessary
    except IndexError:  # no more bird pairs
        return render_template("finished.html")


app.run(debug=True, port=3000, host="0.0.0.0")
