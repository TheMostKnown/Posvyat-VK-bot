def send_message(session, user_id, message, keyboard=None):
    post = {
        "user_id": user_id,
        "message": message,
        "random_id": 0 ,
    }

    if keyboard != None:
        post["keyboard"] = keyboard.get_keyboard()
    else:
        post = post
        
    session.method("messages.send", post)