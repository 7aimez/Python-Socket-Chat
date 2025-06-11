def format_message(username, message):
    return f"{username}: {message}"

def log_message(message):
    with open("chat.log", "a") as log_file:
        log_file.write(message + "\n")