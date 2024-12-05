import json
import uuid
from flask import Flask, redirect, render_template, request, url_for, flash, get_flashed_messages



app = Flask(__name__)
app.secret_key = "secret_key"
users = json.load(open("./database/users.json", 'r'))


@app.route('/')
def index():
    return 'Welcome to Flask!'


@app.route('/users/')
def users_index():
    with open("./database/users.json", "r") as f:
        users = json.load(f)
    term = request.args.get('term', '')
    filtered_users = [user for user in users if term in user['name']]
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'users/index.html',
        users=filtered_users,
        search=term,
        messages=messages,
    )


@app.post('/users')
def users_post():
    user_data = request.form.to_dict()
    errors = validate(user_data)
    if errors:
        return render_template(
            'users/new.html',
            user=user_data,
            errors=errors,
        )
    id = str(uuid.uuid4())
    user = {
        'id': id,
        'name': user_data['name'],
        'email': user_data['email']
    }
    users.append(user)
    with open("./database/users.json", "w") as f:
        json.dump(users, f)
    flash('User was added successfully', 'success')
    return redirect(url_for('users_index'), code=302)


@app.route('/users/new/')
def users_new():
    user = {'name': '', 'email': ''}
    errors = {}
    return render_template(
        'users/new.html',
        user=user,
        errors=errors,
    )


@app.route('/users/<id>')
def users_show(id):
    with open("./database/users.json", "r") as f:
        users = json.load(f)
    user = next(user for user in users if id == str(user['id']))
    return render_template(
        'users/show.html',
        user=user,
    )


@app.route('/courses/<id>')
def courses_show(id):
    return f'Course id: {id}'


def validate(user):
    errors = {}
    if not user['name']:
        errors['name'] = "Can't be blank"
    if not user['email']:
        errors['email'] = "Can't be blank"
    return errors

@app.route('/users/<id>/edit')
def users_edit(id):
    with open("./database/users.json", "r") as f:
        users = json.load(f)
    user = next((u for u in users if u['id'] == id), None)
    errors = {}
    if not user:
        return 'User did not found', 404

    return render_template(
           'users/edit.html',
           user=user,
           errors=errors,
    )

@app.route('/users/<id>/patch', methods=['POST'])
def users_patch(id):
    with open("./database/users.json", "r") as f:
        users = json.load(f)
    data = request.form.to_dict()
    errors = validate(data)
    if errors:
        user = next((u for u in users if u['id'] == id), None)
        return render_template(
            'users/edit.html',
            user=user,
            errors=errors,
        ), 422

    for user in users:
        if user['id'] == id:
            user['name'] = user['name']
            user['email'] = user['email']
    with open("./database/users.json", "w") as f:
        json.dump(users, f)
    flash('Users has been updated', 'success')
    return redirect(url_for('users_index'))

def validate_users_patch(user):
    errors = {}
    if not user['name']:
        errors['name'] = "Can't be blank"
    if not user['email']:
        errors['email'] = "Can't be blank"
    return errors