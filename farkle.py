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

    @property
    def is_match(self):
        return self.score != 0


class SixOfAKind(Score):
    def __init__(self, roll):
        super(SixOfAKind, self).__init__()
        self.claim, self.remainder = _claim_remainder(roll, [6])
        self.score = 3000 if self.claim else 0

class FiveOfAKind(Score):
    def __init__(self, roll):
        super(FiveOfAKind, self).__init__()
        self.claim, self.remainder = _claim_remainder(roll, [5])
        self.score = 2000 if self.claim else 0

class FourOfAKind(Score):
    def __init__(self, roll):
        super(FourOfAKind, self).__init__()
        self.claim, self.remainder = _claim_remainder(roll, [4])
        self.score = 1000 if self.claim else 0

class ThreeOfAKind(Score):
    SCORES = {1:300, 2:200, 3:300, 4:400, 5:500, 6:600}

    def __init__(self, roll):
        super(ThreeOfAKind, self).__init__()
        self.claim, self.remainder = _claim_remainder(roll, [3])
        if self.claim:
            self.score = ThreeOfAKind.SCORES[self.claim[0]]
        else:
            self.score= 0

class TwoTriplets(Score):
    def __init__(self, roll):
        super(TwoTriplets, self).__init__()
        self.claim, self.remainder = _claim_remainder(roll, [3,3])
        self.score = 2500 if self.claim else 0

class FourAndTwo(Score):
    def __init__(self, roll):
        super(FourAndTwo, self).__init__()
        self.claim, self.remainder = _claim_remainder(roll, [2, 4])
        self.score = 1500 if self.claim else 0

class ThreePair(Score):
    def __init__(self, roll):
        super(ThreePair, self).__init__()
        self.claim, self.remainder = _claim_remainder(roll, [2,2,2])
        self.score = 1500 if self.claim else 0

class Straight(Score):
    def __init__(self, roll):
        super(Straight, self).__init__()
        self.claim, self.remainder = _claim_remainder(roll, [1,1,1,1,1,1])
        self.score = 1500 if self.claim else 0

class OnesAndFives(Score):
    def __init__(self, roll):
        super(OnesAndFives, self).__init__()
        (self.claim,
         self.remainder,
         self.score) = self._claim_remainder_score(roll)

    @staticmethod
    def _claim_remainder_score(roll):
        score = 0
        claim = []
        remainder = []
        for die in roll:
            if die == 1:
                claim.append(die)
                score += 100
            elif die == 5:
                claim.append(die)
                score += 50
            else:
                remainder.append(die)
        return claim, remainder, score

class Farkle(Score):
    def __init__(self, roll):
        super(Farkle, self).__init__()
        self.claim = []
        self.remainder = []
        self.score = 0
        self.is_farkle = True
        self.can_reroll = False


class Roll(object):
    SCORE_CLASSES = [SixOfAKind,
                     FiveOfAKind,
                     FourAndTwo,
                     TwoTriplets,
                     Straight,
                     ThreePair,
                     FourOfAKind,
                     ThreeOfAKind,
                     OnesAndFives,
                     ]

    def __init__(self, dice):
        self.dice = dice
        self.partial_scores = self._build_partial_scores(dice)
        self.can_reroll = self.partial_scores[-1].can_reroll
        self.remainder = self.partial_scores[-1].remainder
        self.score = sum([x.score for x in self.partial_scores])
        self.is_farkle = self.partial_scores[-1].is_farkle

    @staticmethod
    def _get_partial_score(dice):
        for score_class in Roll.SCORE_CLASSES:
            partial_score = score_class(dice)
            if partial_score.is_match:
                return partial_score
        return Farkle(dice)

    def _build_partial_scores(self, dice):
        partial_scores = []
        partial_score = self._get_partial_score(dice)
        partial_scores.append(partial_score)
        while partial_score.score and partial_score.remainder:
            partial_score = self._get_partial_score(partial_score.remainder)
            if partial_score.score:
                partial_scores.append(partial_score)
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
    player_a = Player('A')
    player_b = Player('B')
    player_c = Player('C')

    game = Game([player_a, player_b, player_c])
    game.play()

if __name__ == '__main__':
    main()
