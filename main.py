from flask import Flask, request, redirect, url_for, render_template
import db

app = Flask(__name__)

quiz_id = 0
question_id = 0
score = 0

@app.route('/', methods=['GET', 'POST'])
def index():
    global quiz_id, question_id
    if request.method == "GET":
        question_id = 0
        form_start = '''
        <form method="post">
        <select name="quiz">
        '''
        form_end = '''
        </select>
        <input type="submit">
        </form>
        '''
        options = ""
        for q in db.get_quizzes():
            option = f'<option value="{q[0]}">{q[1]}</option>'
            options += option
        return form_start + options + form_end
    
    if request.method == "POST":
        quiz_id = request.form.get("quiz")
        return redirect("/test")
    
@app.route('/test', methods=['GET', 'POST'])
def test():
    global question_id, score

    try:
        question = db.get_questions(quiz_id)[question_id]
    except IndexError:
        return redirect(url_for("result"))

    if request.method == "GET":
        return render_template("test.html", question=question)

    if request.method == "POST":
        question_id += 1
        user_answer = request.form.get("answer")

        if user_answer == question[1]:
            score += 1
            text = "Правильно"
        else:
            score -= 1
            text = "Неправильно"
    return render_template("test.html", text_result = text)


@app.route('/result')
def result():
    return render_template("result.html")

if __name__ == "__main__":
    app.run(debug=True)
