from collections import Counter
import random

_NUMBER_DICE = 6

def _claim_remainder(roll, count_values):
    claim = []
    remainder = []
    counter = Counter(roll)
    for die in sorted(roll):
        if counter[die] in count_values:
            claim.append(die)
        else:
            remainder.append(die)
    if sorted(Counter(claim).values()) == sorted(count_values):
        return claim, remainder
    else:
        return [], list(roll)

class Score(object):
    def __init__(self):
        self.can_reroll = True
        self.is_farkle = False
        self.score = 0

    @property
    def is_match(self):
        return self.score != 0

    def append_me(self, scores):
        if self.score != 0:
            scores.append(self)

class SixOfAKind(Score):
    def __init__(self, dice):
        super(SixOfAKind, self).__init__()
        self.claim, self.remainder = _claim_remainder(dice, [6])
        self.score = 3000 if self.claim else 0

    @property
    def next_score(self):
        return TwoTriplets


class TwoTriplets(Score):
    def __init__(self, dice):
        super(TwoTriplets, self).__init__()
        self.claim, self.remainder = _claim_remainder(dice, [3,3])
        self.score = 2500 if self.claim else 0

    @property
    def next_score(self):
        return FourAndTwo


class FourAndTwo(Score):
    def __init__(self, dice):
        super(FourAndTwo, self).__init__()
        self.claim, self.remainder = _claim_remainder(dice, [2, 4])
        self.score = 1500 if self.claim else 0

    @property
    def next_score(self):
        return ThreePair


class ThreePair(Score):
    def __init__(self, dice):
        super(ThreePair, self).__init__()
        self.claim, self.remainder = _claim_remainder(dice, [2,2,2])
        self.score = 1500 if self.claim else 0

    @property
    def next_score(self):
        return Straight


class Straight(Score):
    def __init__(self, dice):
        super(Straight, self).__init__()
        self.claim, self.remainder = _claim_remainder(dice, [1,1,1,1,1,1])
        self.score = 1500 if self.claim else 0

    @property
    def next_score(self):
        return FiveOfAKind


class FiveOfAKind(Score):
    def __init__(self, dice):
        super(FiveOfAKind, self).__init__()
        self.claim, self.remainder = _claim_remainder(dice, [5])
        self.score = 2000 if self.claim else 0

    @property
    def next_score(self):
        return FourOfAKind


class FourOfAKind(Score):
    def __init__(self, dice):
        super(FourOfAKind, self).__init__()
        self.claim, self.remainder = _claim_remainder(dice, [4])
        self.score = 1000 if self.claim else 0

    @property
    def next_score(self):
        return ThreeOfAKind

class ThreeOfAKind(Score):
    SCORES = {1:300, 2:200, 3:300, 4:400, 5:500, 6:600}

    def __init__(self, dice):
        super(ThreeOfAKind, self).__init__()
        self.claim, self.remainder = _claim_remainder(dice, [3])
        if self.claim:
            self.score = ThreeOfAKind.SCORES[self.claim[0]]
        else:
            self.score= 0

    @property
    def next_score(self):
        return One


class One(Score):
    def __init__(self, dice):
        super(One, self).__init__()
        (self.claim,
         self.remainder,
         self.score) = self._claim_remainder_score(dice)

    @staticmethod
    def _claim_remainder_score(dice):
        remainder = list(dice)
        for die in dice:
            if die == 1:
                remainder.remove(die)
                return [die], remainder, 100
        return [], dice, 0

    @property
    def next_score(self):
        if self.claim:
            return One
        else:
            return Five


class Five(Score):
    def __init__(self, dice):
        super(Five, self).__init__()
        (self.claim,
         self.remainder,
         self.score) = self._claim_remainder_score(dice)

    @staticmethod
    def _claim_remainder_score(dice):
        remainder = list(dice)
        for die in dice:
            if die == 5:
                remainder.remove(die)
                return [die], remainder, 50
        return [], dice, 0

    @property
    def next_score(self):
        if self.claim:
            return Five
        else:
            return Farkle


class Farkle(Score):
    def __init__(self, dice):
        super(Farkle, self).__init__()
        self.claim = []
        self.remainder = []
        self.score = 0
        self.is_farkle = True
        self.can_reroll = False

    def append_me(self, scores):
        if not scores:
            scores.append(self)

    @property
    def next_score(self):
        return None

class Roll(object):
    def __init__(self, dice):
        self.dice = dice
        self.partial_scores = self._build_partial_scores(dice)
        self.can_reroll = self.partial_scores[-1].can_reroll
        self.remainder = self.partial_scores[-1].remainder
        self.score = sum([x.score for x in self.partial_scores])
        self.is_farkle = self.partial_scores[-1].is_farkle

    def _build_partial_scores(self, dice):
        partial_scores = []
        partial_score = SixOfAKind(dice)
        remaining_dice = partial_score.remainder
        partial_score.append_me(partial_scores)
        while partial_score.next_score:
            partial_score = partial_score.next_score(remaining_dice)
            partial_score.append_me(partial_scores)
            remaining_dice = partial_score.remainder
        return partial_scores


    def dump_partial_scores(self, player_name):
        msg_fmt = 'player {}: | rolled: {}'
        print(msg_fmt.format(player_name, ','.join(map(str, self.dice))))
        msg_fmt = '\t{score_name} : {claim} | {score} points'
        for partial_score in self.partial_scores:
            print(msg_fmt.format(player_name=player_name,
                                    score_name=partial_score.__class__.__name__,
                                    claim=partial_score.claim,
                                    score=partial_score.score))


class Turn(object):
    def __init__(self, player):
        self.rolls, self.score = self._build_rolls(player)

    @staticmethod
    def _roll(total_dice):
        return [random.randint(1, 6) for x in range(0, total_dice)]

    def _build_rolls(self, player):
        rolls = []
        roll = Roll(self._roll(_NUMBER_DICE))
        rolls.append(roll)
        roll.dump_partial_scores(player.name)
        total_dice = _NUMBER_DICE if not roll.remainder else len(roll.remainder)
        while roll.can_reroll and player.roll_again(total_dice):
            roll = Roll(self._roll(total_dice))
            rolls.append(roll)
            roll.dump_partial_scores(player.name)
            total_dice = _NUMBER_DICE if not roll.remainder else len(roll.remainder)
        if roll.is_farkle:
            score = 0
        else:
            score = sum([roll.score for roll in rolls])
        return rolls, score


class Player(object):
    def __init__(self, name):
        self.name = name
        self.turns = []

    @property
    def score(self):
        return sum([x.score for x in self.turns])

    def take_turn(self):
        turn = Turn(self)
        self.turns.append(turn)
        print('player {} | score {}'.format(self.name, self.score))

    def roll_again(self, roll_remainder):
        msg = '(r)oll {} dice, (s)top? (r): '.format(roll_remainder)
        roll_again = input(msg)
        roll_again = roll_again if roll_again else 'r'
        return roll_again.startswith('r')

    def keep_going(self):
        msg_fmt = '\nplayer {} | (r)oll or (q)uit? (r): '
        keep_going = input(msg_fmt.format(self.name))
        keep_going = keep_going if keep_going else 'r'
        return not keep_going.startswith('q')


class Game(object):
    def __init__(self, players):
        self.players = players

    def play(self):
        players = list(self.players)
        while players:
            for player in list(players):
                if player.keep_going():
                    player.take_turn()
                else:
                    players.remove(player)


def main():
    player_a = Player('chris')
    player_b = Player('jules')

    game = Game([player_a, player_b])
    game.play()

if __name__ == '__main__':
    main()
