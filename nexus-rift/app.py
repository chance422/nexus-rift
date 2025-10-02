from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Home page
@app.route('/team')
def team():
    team_members = [
        {'name': 'Ghosty', 'bio': 'Mysterious coder.', 'image': 'ghosty.jpg'},
        {'name': 'Camiedex', 'bio': 'owner.', 'image': 'camiedex.jpg'},
        {'name': 'Taha', 'bio': 'dev.', 'image': 'taha.jpg'},
        {'name': 'Sledge', 'bio': 'dev.', 'image': 'taha.jpg'},
        {'name': 'TheNexusRiftGuy', 'bio': 'head ea security.', 'image': 'nexusriftguy.jpg'},
    ]
    return render_template('team.html', team=team_members)

# Login page
@app.route('/login')
def login():
    return render_template('login.html')

# Signup page (GET shows form, POST handles form submission)
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Here add your signup logic (save to DB, etc.)
        # For now, just redirect to home
        return redirect(url_for('index'))
    return render_template('signup.html')


if __name__ == '__main__':
    app.run(debug=True)
