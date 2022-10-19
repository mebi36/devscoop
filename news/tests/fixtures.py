import uuid

job1 = {
    "id": uuid.uuid4(),
    "type": "job",
    "title": "Hello, world",
    "url": "http://localhost:8000",
    "text": "Google is Hiring Software Engineers"
}
poll1 = {
    "id": uuid.uuid4(),
    "type": "poll",
    "title": "Best Programming Language",
    "text": "Time to settle this once and for all. Which language is the best programming language out there?",
    "url": "http://localhost:8000"
}
poll1_opt1 = {
    "id": uuid.uuid4(),
    "type": "pollopt",
    "score": 100,
    "text": "Perl",
    "parent": "".join(["L", str(poll1["id"])]),
    "url": "http://localhost:8000"
}
poll1_opt2 = {
    "id": uuid.uuid4(),
    "type": "pollopt",
    "score": 30,
    "text": "Perl",
    "parent": "".join(["L", str(poll1["id"])]),
    "url": "http://localhost:8000"
}
poll2_opt3 = {
    "id": uuid.uuid4(),
    "type": "job",
    "score": 80,
    "text": "Rust",
    "parent": "".join(["L", str(poll1["id"])]),
    "url": "http://localhost:8000"
}


story1 = {
    "id": uuid.uuid4(),
    "type": "story",
    "score": 30,
    "title": "Hello, world",
    "url": "http://localhost:8000"
}

story2 = {
    "id": uuid.uuid4(),
    "type": "story",
    "score": 80,
    "title": "Another funny story",
    "url": "http://localhost:8000"
}

story1_comment = {
    "id": uuid.uuid4(),
    "type": "comment",
    "parent": "".join(["L2", str(story1["id"])]),
    "text": "cool"
}

story1_comment2 = {
    "id": uuid.uuid4(),
    "type": "comment",
    "parent": "".join(["L", str(poll1["id"])]),
    "text": "cool"
}
