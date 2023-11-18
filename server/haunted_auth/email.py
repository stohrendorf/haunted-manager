def email_verified_callback(user):
    user.is_active = True
