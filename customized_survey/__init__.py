from otree.api import *

import json
import random

doc = """ """


class C(BaseConstants):
    NAME_IN_URL = 'customized_survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    survey_template_name = __name__ + '/survey_template.html'
    crt_template_name = __name__ + '/crt.html'
    gentrust_template_name = __name__ + '/gentrust.html'

    ## Frederick, S. (2005).
    ## "Cognitive reflection and decision making,"
    ## Journal of Economic perspectives, 19(4), 25-42.
    materials_crt = {
        "field": models.FloatField,
        "items": {
            "crt1": {
                "question": """
                    A bat and a ball cost $1.10 in total.
                    The bat costs $1.00 more than the ball.
                    How much does the ball cost?
                """,
                "unit": "cent(s)",
                "correct": 5.0
            },
            "crt2": {
                "question": """
                    If it takes 5 machines 5 minutes to make 5 widgets,
                    how long would it take 100 machines to make 100 widgets?
                """,
                "unit": "minute(s)",
                "correct": 5.0
            },
            "crt3": {
                "question": """
                    In a lake, there is a patch of lily pads.
                    Every day, the patch doubles in size.
                    If it takes 48 days for the patch to cover the entire lake,
                    how long would it take for the patch to cover half of the lake?
                """,
                "unit": "day(s)",
                "correct": 47
            }
        }
    }


    ## Yamagishi, T. & Yamagishi, M. (1994).
    ## "Trust and commitment in the United States and Japan,"
    ## Motivation and Emotion, 18, 129-166.
    materials_gentrust = {
        "field": models.IntegerField,
        "opts": [
            [1, "Strongly Disagree"],
            [2, "Disagree"],
            [3, "Neutral"],
            [4, "Agree"],
            [5, "Strongly Agree"]
        ],
        "items": {
            "gentrust1": "Most people are basically honest.",
            "gentrust2": "Most people are trustworthy.",
            "gentrust3": "Most people are basically good and kind.",
            "gentrust4": "Most people are trustful of others.",
            "gentrust5": "I am trustful.",
            "gentrust6": "Most people will respond in kind when they are trusted by others."
        }
    }



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    order_pages = models.LongStringField()
    order_crt = models.LongStringField()
    order_gentrust = models.LongStringField()

    score_crt = models.FloatField()
    score_gentrust = models.FloatField()


for k, v in C.materials_crt["items"].items():
    setattr(
        Player,
        k,
        C.materials_crt["field"](
            label = v["question"],
            help_text = v["unit"]
        )
    )
    setattr(
        Player,
        k + "_score",
        models.BooleanField(
            initial = False
        )
    )

for k, v in C.materials_gentrust["items"].items():
    setattr(
        Player,
        k,
        C.materials_gentrust["field"](
            label = v,
            choices = C.materials_gentrust["opts"],
            widget = widgets.RadioSelectHorizontal
        )
    )



def creating_session(subsession: Subsession):
    list_crt = [k for k in C.materials_crt["items"].keys()]
    list_gentrust = [k for k in C.materials_gentrust["items"].keys()]

    for p in subsession.get_players():
        p.order_pages = json.dumps(
            random.sample(["crt", "gentrust"], 2)
        )

        p.order_crt = json.dumps(
            random.sample(list_crt, len(list_crt))
        )

        p.order_gentrust = json.dumps(
            random.sample(list_gentrust, len(list_gentrust))
        )


def calc_score_crt(player: Player, timeout_happened):
    if not timeout_happened:
        sumscore = 0
        for k, v in C.materials_crt["items"].items():
            answer = getattr(player, k)
            correct = v["correct"]
            if answer == correct:
                setattr(player, k + "_score", True)
                sumscore += 1
        player.score_crt =  sumscore
    else:
        player.score_crt =  -1


def calc_score_gentrust(player: Player, timeout_happened):
    if not timeout_happened:
        list_answer = [
            getattr(player, k) for k in C.materials_gentrust["items"].keys()
        ]
        player.score_gentrust = sum(list_answer) / len(list_answer)
    else:
        player.score_gentrust = -1


def my_get_form_fields(player: Player, pgidx):
    if json.loads(player.order_pages)[pgidx - 1] == "crt":
        return json.loads(player.order_crt)
    else:
        return json.loads(player.order_gentrust)


def my_vars_for_template(player: Player, pgidx):
    return {
        "page_num": pgidx,
        "page_name": json.loads(player.order_pages)[pgidx - 1]
    }


def my_before_next_page(player: Player, timeout_happened, pgidx):
    if json.loads(player.order_pages)[pgidx - 1] == "crt":
        calc_score_crt(player, timeout_happened)
    else:
        calc_score_gentrust(player, timeout_happened)



# PAGES
class Survey1(Page):
    template_name = C.survey_template_name
    form_model = "player"
    pgidx = 1

    @staticmethod
    def get_form_fields(player: Player):
        return my_get_form_fields(player, __class__.pgidx)

    @staticmethod
    def vars_for_template(player: Player):
        return my_vars_for_template(player, __class__.pgidx)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        my_before_next_page(player, timeout_happened, __class__.pgidx)


class Survey2(Page):
    template_name = C.survey_template_name
    form_model = "player"
    pgidx = 2

    @staticmethod
    def get_form_fields(player: Player):
        return my_get_form_fields(player, __class__.pgidx)

    @staticmethod
    def vars_for_template(player: Player):
        return my_vars_for_template(player, __class__.pgidx)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        my_before_next_page(player, timeout_happened, __class__.pgidx)


class Results(Page):
    pass



page_sequence = [Survey1, Survey2, Results]
