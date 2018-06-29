from user import User
from werkzeug.security import safe_str_cmp

#users = [
#    User(1, 'bob', 'asdf')

#]
#username_mapping = {u.username: u for u in users}
#userid_mapping = {u.id: u for u in users}


def authendication(username, password):
    user = User.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user


def identify(payload):
    user_id = payload['identity']
    return User.find_by_id(user_id)
