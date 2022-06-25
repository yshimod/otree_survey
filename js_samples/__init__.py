from otree.api import *

doc = """ """


class C(BaseConstants):
    NAME_IN_URL = 'js_samples'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    switching_point = models.IntegerField()

    yellow = models.FloatField()
    red = models.FloatField()
    black = models.FloatField()


# PAGES
class Samples1(Page):
    form_model = "player"
    form_fields = ["switching_point"]

    def vars_for_template(player: Player):
        return {
            "optR": [200, 250, 300, 350, 400]
        }


class Samples2(Page):
    form_model = "player"
    form_fields = ["yellow", "red", "black"]


class Results(Page):
    pass



page_sequence = [Samples1, Samples2, Results]
