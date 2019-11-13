import bcrypt


def generate_password_hash(password):
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed


def check_password_hash(plain_password, password_hash):
    is_correct = bcrypt.hashpw(plain_password, password_hash) == password_hash
    return is_correct

