from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '920505ba20664f2fd1146bb4fda71e32'
posts = [
    {
        "title": "The Imitation Game",
        "author": 'Agatha Christie',
        "read": "47,922",
        "date": "December 12, 1957",
        "content": """Pure chance led my friend Hercule Poirot, formerly chief of the Belgian force, to be 
connected with the Styles Case. His success brought him notoriety, and he decided to 
devote himself to the solving of problems in crime. Having been wounded on the Somme 
and invalided out of the Army, I finally took up my quarters with him in London. Since I 
have a first-hand knowledge of most of his cases, it has been suggested to me that I select 
some of the most interesting and place them on record. In doing so, I feel that I cannot do 
better than begin with that strange tangle which aroused such widespread public interest 
at the time. I refer to the affair at the Victory Ball. """
    },
    {
        "title": "The Hounds of Baskerville",
        "author": "Sir Arthur Conan Doyle",
        "read": "113,203",
        "date": "April 23, 1924",
        "content": """Dr James Mortimer calls on Sherlock Holmes in London for advice after his friend Sir Charles Baskerville 
        was found dead in the yew alley of his manor on Dartmoor in Devon. The death was attributed to a heart attack, but according to Mortimer, 
        Sir Charles's face retained an expression of horror, and not far from the corpse the footprints of a gigantic hound were clearly visible. 
        According to an old legend, a curse runs in the Baskerville family since the time of the English Civil War, when a Hugo Baskerville abducted and 
        caused the death of a maiden on the moor, only to be killed in turn by a huge demonic hound. Allegedly the same creature has been haunting the 
        anor ever since, causing the premature death of many Baskerville heirs. Sir Charles believed in the plague of the hound and so does Mortimer, 
        who now fears for the next in line, Sir Henry Baskerville."""
    },
    {
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "read": "10,127",
        "date": "July 11, 1960",
        "content": """Dr James Mortimer calls on Sherlock Holmes in London for advice after his friend Sir Charles Baskerville 
        was found dead in the yew alley of his manor on Dartmoor in Devon. The death was attributed to a heart attack, but according to Mortimer, 
        Sir Charles's face retained an expression of horror, and not far from the corpse the footprints of a gigantic hound were clearly visible. 
        According to an old legend, a curse runs in the Baskerville family since the time of the English Civil War, when a Hugo Baskerville abducted and 
        caused the death of a maiden on the moor, only to be killed in turn by a huge demonic hound. Allegedly the same creature has been haunting the 
        anor ever since, causing the premature death of many Baskerville heirs. Sir Charles believed in the plague of the hound and so does Mortimer, 
        who now fears for the next in line, Sir Henry Baskerville."""
    }
]


@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html", posts=posts)


@app.route("/about")
def about_page():
    return render_template("about.html", title='About Page')


@app.route("/register", methods=['GET', 'POST'])
def register_page():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login_page'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@gmail.com' and form.password.data == 'password':
            flash('Successfully logged in!', 'success')
            return redirect(url_for('home_page'))
        else:
            flash("Email or Password is incorrect!", 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == "__main__":
    app.run(debug=True)
