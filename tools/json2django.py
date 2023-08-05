#!/usr/bin/env python
import json


def populate():
    basic = json.load(open('./basic.json', 'r'))
    advanced = json.load(open('./advanced.json', 'r'))
    expert = json.load(open('./expert.json', 'r'))

    result = [
        {
            "model": "exam.level",
            "pk": "basic",
            "fields": {}
        },
        {
            "model": "exam.level",
            "pk": "advanced",
            "fields": {}
        },
        {
            "model": "exam.level",
            "pk": "expert",
            "fields": {}
        },
        {
            "model": "core.lang",
            "pk": "en",
            "fields": {
                "long": "English"
            }
        },
        {
            "model": "core.lang",
            "pk": "fr",
            "fields": {
                "long": "Francais"
            }
        },
    ]

    question_count = 0
    question_text_count = 0
    answer_count = 0
    answer_text_count = 0
    questions = list()
    questions.append(basic['questions_basiques'])
    questions.append(advanced['questions_avancees'])
    questions.append(expert['questions_expertes'])
    for question in expert['questions_expertes']:
        question_count += 1
        question_result = {
            "model": "exam.question",
            "pk": question_count,
            "fields": {
                "level": "expert"
            }
        }
        result.append(question_result)
        for lang in question["question"]:
            question_text_count += 1
            locale_result = {
                "model": "exam.questiontext",
                "pk": question_text_count,
                "fields": {
                    "lang": lang,
                    "text": question["question"][lang],
                    "explanation": question["explication"][lang],
                    "question": question_count
                }
            }
            result.append(locale_result)
        answer_list_id = 0
        for answer in question["reponses"]["fr"]:
            answer_count += 1
            answer_result = {
                "model": "exam.answer",
                "pk": answer_count,
                "fields": {
                    "question": question_count,
                    "point": answer["points"],
                    "count": 0,
                }
            }
            for lang in question["reponses"]:
                answer_text_count += 1
                locale_answer_result = {
                    "model": "exam.answertext",
                    "pk": answer_text_count,
                    "fields": {
                        "answer": answer_count,
                        "lang": lang,
                        "text": question["reponses"][lang][answer_list_id]["reponse"]
                    }
                }
                result.append(locale_answer_result)
            answer_list_id += 1
            result.append(answer_result)

    print(json.dumps(result))
    # for question in fr['questions']:
    #     text_count += 1
    #     question_result = {
    #         "model": "exam.question",
    #         "pk": question["slug"],
    #         "fields": {
    #             "category": "workstation"
    #         }
    #     }
    #     question_text_result = {
    #         "model": "exam.questiontext",
    #         "pk": text_count,
    #         "fields": {
    #             "lang": "fr",
    #             "text": question["question"],
    #             "explanation": "TBD",
    #             "tips": "TBD",
    #             "question": question["slug"]
    #         }
    #     }
    #     for answer in question['responses']:
    #         answer_count += 1
    #         answer_result = {
    #             "model": "exam.answer",
    #             "pk": answer_count,
    #             "fields": {
    #                 "lang": "fr",
    #                 "text": answer,
    #                 "point": 0,
    #                 "question": question["slug"],
    #                 "count": 0
    #             }
    #
    #         }
    #         result.append(answer_result)
    #     result.append(question_result)
    #     result.append(question_text_result)
    # for question in en['questions']:
    #     text_count += 1
    #     question_text_result = {
    #         "model": "exam.questiontext",
    #         "pk": text_count,
    #         "fields": {
    #             "lang": "en",
    #             "text": question["question"],
    #             "explanation": "TBD",
    #             "tips": "TBD",
    #             "question": question["slug"]
    #         }
    #     }
    #     for answer in question['responses']:
    #         answer_count += 1
    #         answer_result = {
    #             "model": "exam.answer",
    #             "pk": answer_count,
    #             "fields": {
    #                 "lang": "en",
    #                 "text": answer,
    #                 "point": 0,
    #                 "question": question["slug"],
    #                 "count": 0
    #             }
    #
    #         }
    #         result.append(answer_result)
    #     result.append(question_text_result)
    #
    # jsonify = json.dumps(result, indent=4)
    # with open("./load.json", "w") as outfile:
    #     outfile.write(jsonify)

populate()