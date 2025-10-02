from flask import Flask, render_template, request, redirect, url_for, session, flash
import random
import os

app = Flask(__name__)
app.secret_key = "secret"

# User storage (in-memory for now)
users = {}

# Static team members (manually added)
static_team = [
    {
        "name": "Ghosty",
        "role": "Site builder",
        "bio": "with great power comes great responibilitys.",
        "image": "static/uploads/Ghosty"
    },
    {
        "name": "Camiedex",
        "role": "Dev/community manager",
        "bio": "TBD.",
        "image": "static/uploads/jane_smith.jpg"
    },
    {
        "name": "Taha",
        "role": "Dev/community manager",
        "bio": "TBD.",
        "image": "static/uploads/jane_smith.jpg"
    },
    {
        "name": "Sledge",
        "role": "Dev/community manager",
        "bio": "TBD.",
        "image": "static/uploads/jane_smith.jpg"
    },
    {
        "name": "mr meme",
        "role": "Dev",
        "bio": "TBD.",
        "image": "static/uploads/jane_smith.jpg"
    },
    {
        "name": "neoswag",
        "role": "Dev",
        "bio": "TBD.",
        "image": "static/uploads/jane_smith.jpg"
    },
    {
        "name": "cnatt",
        "role": "Dev",
        "bio": "TBD.",
        "image": "static/uploads/jane_smith.jpg"
    },
    {
        "name": "mr man",
        "role": "Dev",
        "bio": "TBD.",
        "image": "static/uploads/jane_smith.jpg"
    },
    {
        "name": "ritz",
        "role": "Dev",
        "bio": "TBD.",
        "image": "static/uploads/jane_smith.jpg"
    },
    {
        "name": "TheNexusRiftGuy",
        "role": "head of ea security",
        "bio": "Treat everyone equally no matter what.",
        "image": "static/uploads/TheNexusRiftGuy"
    },

]

# Helpers
def current_user():
    username = session.get("username")
    return users.get(username)

@app.route("/")
def index():
    return render_template("index.html", user=current_user())

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        custom_id = request.form.get("custom_id")

        if username in users:
            flash("Username already exists.", "error")
            return redirect(url_for("signup"))

        if custom_id:
            userid = custom_id
        else:
            userid = str(random.randint(10000, 99999))

        role = "admin" if len(users) == 0 else "user"

        users[username] = {
            "password": password,
            "userid": userid,
            "role": role,
            "whitelisted_view": False,
            "whitelisted_post": False,
            "bio": "",
            "team_member": False,
        }

        session["username"] = username
        flash("Signed up and logged in!", "success")
        return redirect(url_for("index"))

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = users.get(username)

        if not user or user["password"] != password:
            flash("Invalid credentials.", "error")
            return redirect(url_for("login"))

        session["username"] = username
        flash("Logged in!", "success")
        return redirect(url_for("index"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("Logged out.", "success")
    return redirect(url_for("index"))

@app.route("/admin", methods=["GET", "POST"])
def admin():
    user = current_user()
    if not user or user["role"] != "admin":
        flash("Access denied.", "error")
        return redirect(url_for("index"))

    if request.method == "POST":
        action = request.form["action"]
        target_username = request.form["username"]
        target_user = users.get(target_username)

        if not target_user:
            flash("User not found.", "error")
        else:
            if action == "make_admin":
                target_user["role"] = "admin"
            elif action == "whitelist_view":
                target_user["whitelisted_view"] = True
            elif action == "whitelist_post":
                target_user["whitelisted_post"] = True
            elif action == "toggle_team":
                target_user["team_member"] = not target_user["team_member"]

            flash(f"Updated {target_username}.", "success")

    return render_template("admin.html", user=user, users=users)

@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    viewer = current_user()
    profile_user = users.get(username)

    if not profile_user:
        flash("User not found.", "error")
        return redirect(url_for("index"))

    if request.method == "POST" and viewer and viewer == profile_user:
        new_bio = request.form.get("bio", "").strip()
        profile_user["bio"] = new_bio
        flash("Bio updated!", "success")
        return redirect(url_for("profile", username=username))

    return render_template("profile.html", user=viewer, profile_user=profile_user, username=username)

@app.route("/meet-the-team")
def meet_the_team():
    user = current_user()
    return render_template("meet_the_team.html", user=user, users=users, static_team=static_team)

if __name__ == "__main__":
    app.run(debug=True)
