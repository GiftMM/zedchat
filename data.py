from datetime import datetime

Comment1 = {
            "Text": "We're never far apart",
            "Name": "GiftMM",
            "DateTime": datetime(2022, 3, 2, 18, 0, 0),
            "Picture": "GiftM.jpg"
}

Comment2 = {
            "Text": "Hello",
            "Name": "Gift",
            "DateTime": datetime(2022, 3, 2, 17, 0, 0),
            "Picture": "GiftM.jpg"
}

post1 = {
        "PostId": 1,
        "Text": "Hello world",
        "Name": "Gift",
        "Hearts": ["GiftMM"],
        "Comments": [Comment1, Comment2],
        "DateTime": datetime(2022, 3, 2, 15, 0, 0),
        "Picture": "GiftM.jpg"
    }

post2 = {
        "PostId": 2,
        "Text": "The sky is blue",
        "Name": "GiftM",
        "Hearts": [],
        "Comments": [],
        "DateTime": datetime(2022, 3, 2, 15, 10, 0),
        "Picture": "GiftM.jpg"
    }

post3 = {
        "PostId": 3,
        "Text": "We're never far apart",
        "Name": "GiftMM",
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