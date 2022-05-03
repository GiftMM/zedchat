from werkzeug.security import generate_password_hash, check_password_hash
import database




def forgot_pw(handle,subject,body):
    user = get_user_by_name('')
    name = user['Name']
    email = user['Email']

    message = Mail(
        from_email='sender@mail.com',
        to_email=email,
        subject=subject,
        html_content=body)

    try:
        sg = sendGridAPIClient(secrets.sendgrid_api_key)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)



def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def reset_password(handle):
    new_password = get_random_string(20)
    password = generate_password_hash(new_password)
    reset_database_password(handle,password)
    send_message(handle, 'Zedchat Reset Password','Your new password is %s' %new_password)


reset_password('Gift')