from web_app_sql import app, db, User, Conversation
with app.app_context():
    users = User.query.all()
    convs = Conversation.query.all()
    for user in users:
        print(f"{user.email} - {user.first_name} {user.last_name}")
    for conv in convs:
        print(f"{conv.question} - {conv.answer}")

