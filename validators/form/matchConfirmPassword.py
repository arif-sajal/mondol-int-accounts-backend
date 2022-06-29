def match_confirm_password(password, values):
    if 'password' not in values:
        raise ValueError('Password field is required.')
    elif password != values['password']:
        raise ValueError('Password and confirm password field does not match.')

    return password
