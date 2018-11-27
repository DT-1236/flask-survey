from flask import Flask, render_template, request, session, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys as s_dict

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


@app.route("/")
def question():
    # session['title'] = ss.title (BASIC version)
    # session['instructions'] = ss.instructions (BASIC version)
    # session['questions'] = ss.questions THIS DIDNT WORK
    session.permanent = True
    session['responses'] = []
    session['comments'] = []
    session['questions'] = []
    session['surveys'] = list(s_dict.keys())

    return render_template('startpage.html')


@app.route("/questions/<int:qnum>", methods=["POST"])
def questiondisplay(qnum):
    # We use qnum != 0 check to ensure we have the answer from previous response and we dont get an error when we try to add to the session list
    if qnum != 0:
        session['responses'] = session['responses'] + [request.form["choice"]]
        session['comments'] = session['comments'] + [
            request.form.get("freetext", "")
        ]

    else:
        # global ss
        session["survey"] = request.form["select"]
        session['questions'] = [
            s.question for s in s_dict[session["survey"]].questions
        ]

        if session["survey"] in session['complete']:
            flash(
                f'Survey {session["survey"]} already taken. Please select another one!'
            )
            return redirect('/')

    if qnum != len(session["questions"]):
        ss = s_dict[session["survey"]]
        session['question'] = ss.questions[qnum].question
        session['choices'] = ss.questions[qnum].choices
        session['text'] = ss.questions[qnum].allow_text
        # return render_template('qpage.html', qnum=qnum)
    return redirect(f"/questions/{qnum}")


@app.route("/questions/<int:qnum>")
def reroute(qnum):

    if qnum == len(session["questions"]):
        session['complete'] = session.get('complete', []) + [session["survey"]]
        print(session['complete'])
        return render_template('thanks.html', qnum=qnum)

    return render_template('qpage.html', qnum=qnum)
