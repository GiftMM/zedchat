from collections import UserString
from datetime import datetime

Comment1 = {
            "Text": "We're never far apart",
            "Name": "John",
            "DateTime": datetime(2022, 3, 2, 18, 0, 0),
            "Picture": "GiftM.jpg"
}

Comment2 = {
            "Text": "Hello",
            "Name": "Jack",
            "DateTime": datetime(2022, 3, 2, 17, 0, 0),
            "Picture": "GiftM.jpg"
}

post1 = {
        "PostId": 1,
        "Text": "What a day",
        "Name": "Jack",
        "Hearts": ["John"],
        "Comments": [Comment1, Comment2],
        "DateTime": datetime(2022, 3, 2, 15, 0, 0),
        "Picture": "GiftM.jpg"
    }

post2 = {
        "PostId": 2,
        "Text": "The sky is blue",
        "Name": "Smith",
        "Hearts": [],
        "Comments": [],
        "DateTime": datetime(2022, 3, 2, 15, 10, 0),
        "Picture": "GiftM.jpg"
    }

post3 = {
        "PostId": 3,
        "Text": "We're never far apart",
        "Name": "John",
        "Hearts": [],
        "Comments": [],
        "DateTime": datetime(2022, 3, 2, 15, 23, 0),
        "Picture": "GiftM.jpg"
        
    }

test_posts = {
    1 : post1,
    2 : post2,
    3 : post3
}


Message1 = {
    "Text": "Hello",
    "Name": "Jack",
    "DateTime": datetime(2022, 5, 3, 19, 0, 0),
    "Picture": "GiftM.jpg",
    "Messages":[]
}

Message2 = {
    "Text": "How are you?",
    "Name": "Jack",
    "DateTime": datetime(2022, 5, 3, 20, 0, 0),
    "Picture": "GiftM.jpg"
}

test_messages = [Message1]

#------------------------
#def get_user_by_handle(handle):
#    for user in users
#        if user['handle'] == handle:
#            return user
#    return None

#------------------------------

