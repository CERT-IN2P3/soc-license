#!/usr/bin/env python
import json
from license.models import Question


def populate():
    en = json.load(open('./cli/en.json', 'r'))
    fr = json.load(open('./cli/fr.json', 'r'))

    result = [
        {
            "model": "license.category",
            "pk": "workstation",
            "fields": {}
        },
        {
            "model": "license.lang",
            "pk": "en",
            "fields": {
                "long": "English"
            }
        },
        {
            "model": "license.lang",
            "pk": "fr",
            "fields": {
                "long": "Français"
            }
        },
    ]

    text_count = 0
    answer_count = 0
    for question in fr['questions']:
        text_count += 1
        question_result = {
            "model": "license.question",
            "pk": question["slug"],
            "fields": {
                "category": "workstation"
            }
        }
        question_text_result = {
            "model": "license.questiontext",
            "pk": text_count,
            "fields": {
                "lang": "fr",
                "text": question["question"],
                "explanation": "TBD",
                "tips": "TBD",
                "question": question["slug"]
            }
        }
        for answer in question['responses']:
            answer_count += 1
            answer_result = {
                "model": "license.answer",
                "pk": answer_count,
                "fields": {
                    "lang": "fr",
                    "text": answer,
                    "point": 0,
                    "question": question["slug"],
                    "count": 0
                }

            }
            result.append(answer_result)
        result.append(question_result)
        result.append(question_text_result)
    for question in en['questions']:
        text_count += 1
        question_text_result = {
            "model": "license.questiontext",
            "pk": text_count,
            "fields": {
                "lang": "en",
                "text": question["question"],
                "explanation": "TBD",
                "tips": "TBD",
                "question": question["slug"]
            }
        }
        for answer in question['responses']:
            answer_count += 1
            answer_result = {
                "model": "license.answer",
                "pk": answer_count,
                "fields": {
                    "lang": "en",
                    "text": answer,
                    "point": 0,
                    "question": question["slug"],
                    "count": 0
                }

            }
            result.append(answer_result)
        result.append(question_text_result)

    jsonify = json.dumps(result, indent=4)
    with open("./load.json", "w") as outfile:
        outfile.write(jsonify)

