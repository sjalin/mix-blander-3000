from flask import Flask, render_template, request, redirect, url_for

import mixer
from recipes import recipes


class Webapp(Flask):
    def setMixer(self, mixer_queue):
        self.mq = mixer_queue


app = Webapp(__name__)

drinks = [(i, n) for i, n in enumerate(recipes)]
drinks.append((len(drinks), 'Slumpgrogg'))


@app.get("/")
def home():
    return render_template("base.html", drink_list=drinks)


@app.get("/make/<int:drink_id>")
def make(drink_id):
    print(f'start making {drink_id} {drinks[drink_id][1]}')
    app.mq.put(drinks[drink_id][1])
    return redirect(url_for("home"))
