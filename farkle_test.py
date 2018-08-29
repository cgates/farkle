from farkle import SixOfAKind
from farkle import FiveOfAKind
from farkle import FourOfAKind
from farkle import ThreeOfAKind
from farkle import TwoTriplets
from farkle import FourAndTwo
from farkle import Straight
from farkle import ThreePair
# from farkle import One
# from farkle import Five
from farkle import Scorer

def test_SixOfAKind_noRemainder():
    assert SixOfAKind((1,1,1,1,1,1)).claim == [1,1,1,1,1,1]
    assert SixOfAKind((1,1,1,1,1,1)).remainder == []
    assert SixOfAKind((1,1,1,1,1,1)).score == 3000

    assert SixOfAKind((2,2,2,2,2,2)).claim == [2,2,2,2,2,2]
    assert SixOfAKind((2,2,2,2,2,2)).remainder == []
    assert SixOfAKind((2,2,2,2,2,2)).score == 3000

def test_SixOfAKind_claim_remainder_noClaim():
    assert SixOfAKind((2,2,2,2,2,3)).claim == []
    assert SixOfAKind((2,2,2,2,2,3)).remainder == [2,2,2,2,2,3]
    assert SixOfAKind((2,2,2,2,2,3)).score == 0
    assert SixOfAKind((2,2,2,2,2)).claim == []
    assert SixOfAKind((2,2,2,2,2)).remainder == [2,2,2,2,2]
    assert SixOfAKind((2,2,2,2,2)).score == 0

def test_FiveOfAKind_claim_remainder_noRemainder():
    assert FiveOfAKind((1,1,1,1,1)).claim == [1,1,1,1,1]
    assert FiveOfAKind((1,1,1,1,1)).remainder == []
    assert FiveOfAKind((1,1,1,1,1)).score == 2000
    assert FiveOfAKind((2,2,2,2,2)).claim == [2,2,2,2,2]
    assert FiveOfAKind((2,2,2,2,2)).remainder == []
    assert FiveOfAKind((2,2,2,2,2)).score == 2000

def test_FiveOfAKind_claim_remainder_someRemainder():
    assert FiveOfAKind((2,2,2,2,2,4)).claim == [2,2,2,2,2]
    assert FiveOfAKind((2,2,2,2,2,4)).remainder == [4]
    assert FiveOfAKind((2,2,2,2,2,4)).score == 2000
    assert FiveOfAKind((2,2,2,2,2,3)).claim == [2,2,2,2,2]
    assert FiveOfAKind((2,2,2,2,2,3)).remainder == [3]
    assert FiveOfAKind((2,2,2,2,2,3)).score == 2000

def test_FiveOfAKind_claim_remainder_noClaim():
    assert FiveOfAKind((2,2,2,2,3,3)).claim == []
    assert FiveOfAKind((2,2,2,3,3,3)).remainder == [2,2,2,3,3,3]
    assert FiveOfAKind((2,2,2,3,3,3)).score == 0
    assert FiveOfAKind((2,2,2,2)).claim == []
    assert FiveOfAKind((2,2,2,2)).remainder == [2,2,2,2]
    assert FiveOfAKind((2,2,2,2)).score == 0

def test_FourOfAKind_claim_remainder_noRemainder():
    assert FourOfAKind((1,1,1,1)).claim == [1,1,1,1]
    assert FourOfAKind((1,1,1,1)).remainder == []
    assert FourOfAKind((1,1,1,1)).score == 1000
    assert FourOfAKind((2,2,2,2)).claim == [2,2,2,2]
    assert FourOfAKind((2,2,2,2)).remainder == []
    assert FourOfAKind((2,2,2,2)).score == 1000

def test_FourOfAKind_claim_remainder_someRemainder():
    assert FourOfAKind((2,2,2,2,3,4)).claim == [2,2,2,2]
    assert FourOfAKind((2,2,2,2,3,4)).remainder == [3,4]
    assert FourOfAKind((2,2,2,2,3,4)).score == 1000
    assert FourOfAKind((2,2,2,2,3)).remainder == [3]
    assert FourOfAKind((2,2,2,2,3)).score == 1000

def test_FourOfAKind_claim_remainder_noClaim():
    assert FourOfAKind((2,2,2,3,3,3)).claim == []
    assert FourOfAKind((2,2,2,3,3,3)).remainder == [2,2,2,3,3,3]
    assert FourOfAKind((2,2,2,3,3,3)).score == 0
    assert FourOfAKind((2,2,2)).claim == []
    assert FourOfAKind((2,2,2)).remainder == [2,2,2]
    assert FourOfAKind((2,2,2)).score == 0

def test_ThreeOfAKind_claim_remainder_noRemainder():
    assert ThreeOfAKind((1,1,1)).claim == [1,1,1]
    assert ThreeOfAKind((1,1,1)).remainder == []
    assert ThreeOfAKind((1,1,1)).score == 300

    assert ThreeOfAKind((2,2,2)).claim == [2,2,2]
    assert ThreeOfAKind((2,2,2)).remainder == []
    assert ThreeOfAKind((2,2,2)).score == 200

    assert ThreeOfAKind((3,3,3)).score == 300
    assert ThreeOfAKind((4,4,4)).score == 400
    assert ThreeOfAKind((5,5,5)).score == 500
    assert ThreeOfAKind((6,6,6)).score == 600

def test_ThreeOfAKind_claim_remainder_someRemainder():
    assert ThreeOfAKind((2,2,2,3,3,4)).claim == [2,2,2]
    assert ThreeOfAKind((2,2,2,1,3,4)).remainder == [1,3,4]
    assert ThreeOfAKind((2,2,2,1,3)).remainder == [1,3]

def test_ThreeOfAKind_claim_remainder_noClaim():
    assert ThreeOfAKind((2,2,3,3,4,4)).claim == []
    assert ThreeOfAKind((2,2,3,3,4,4)).remainder == [2,2,3,3,4,4]
    assert ThreeOfAKind((2,2,3,3,4,4)).score == 0
    assert ThreeOfAKind((2,2)).claim == []
    assert ThreeOfAKind((2,2)).remainder == [2,2]
    assert ThreeOfAKind((2,2)).score == 0

def test_TwoTriplets_noRemainder():
    assert TwoTriplets((1,1,1,2,2,2)).claim == [1,1,1,2,2,2]
    assert TwoTriplets((1,1,1,2,2,2)).remainder == []
    assert TwoTriplets((1,1,1,2,2,2)).score == 2500

def test_TwoTriplets_sortsClaim():
    assert TwoTriplets((2,1,2,1,2,1)).claim == [1,1,1,2,2,2]

def test_TwoTriplets_noClaim():
    assert TwoTriplets((1,1,1,2,2,3)).claim == []
    assert TwoTriplets([1,1,1,2,2,3]).remainder == [1,1,1,2,2,3]
    assert TwoTriplets((1,1,1,2,2,3)).score == 0

def test_FourAndTwo_noRemainder():
    assert FourAndTwo((1,1,1,1,2,2)).claim == [1,1,1,1,2,2]
    assert FourAndTwo((1,1,1,1,2,2)).remainder == []
    assert FourAndTwo((1,1,1,1,2,2)).score == 1500

def test_FourAndTwo_sorts():
    assert FourAndTwo((2,1,1,1,1,2)).claim == [1,1,1,1,2,2]

def test_FourAndTwo_noClaim():
    assert FourAndTwo((1,1,1,2,2,2)).claim == []
    assert FourAndTwo([1,1,1,2,2,2]).remainder == [1,1,1,2,2,2]
    assert FourAndTwo((1,1,1,2,2,2)).score == 0

    assert FourAndTwo((1,1,2,2,3,4)).claim == []
    assert FourAndTwo([1,1,2,2,3,4]).remainder == [1,1,2,2,3,4]
    assert FourAndTwo((1,1,2,2,3,4)).score == 0

def test_Straight_noRemainder():
    assert Straight((1,2,3,4,5,6)).claim == [1,2,3,4,5,6]
    assert Straight((1,2,3,4,5,6)).remainder == []
    assert Straight((1,2,3,4,5,6)).score == 1500

def test_Straight_sorts():
    assert Straight((1,3,5,2,4,6)).claim == [1,2,3,4,5,6]

def test_Straight_noClaim():
    assert Straight((1,2,3,4,4,6)).claim == []
    assert Straight([1,2,3,4,4,6]).remainder == [1,2,3,4,4,6]
    assert Straight((1,2,3,4,4,6)).score == 0

    assert Straight((1,2,3,4,5)).claim == []
    assert Straight([1,2,3,4,5]).remainder == [1,2,3,4,5]
    assert Straight((1,2,3,4,5)).score == 0

def test_ThreePair_noRemainder():
    assert ThreePair((1,1,2,2,3,3)).claim == [1,1,2,2,3,3]
    assert ThreePair((1,1,2,2,3,3)).remainder == []
    assert ThreePair((1,1,2,2,3,3)).score == 1500

def test_ThreePair_sorts():
    assert ThreePair((1,2,3,3,2,1)).claim == [1,1,2,2,3,3]

def test_ThreePair_noClaim():
    assert ThreePair((1,1,2,2,3,4)).claim == []
    assert ThreePair([1,1,2,2,3,4]).remainder == [1,1,2,2,3,4]
    assert ThreePair((1,1,2,2,3,4)).score == 0

    assert ThreePair((1,1,2,2)).claim == []

# def test_One_matches_true():
#     points = One()
#     assert points.matches((1,1,2,2,3,3)) == True
#
# def test_One_matches_false():
#     points = One()
#     assert points.matches((2,2,3,4,5,6)) == False
#
# def test_One_score():
#     assert One().score((1,)) == 100
#     assert One().score((1,1)) == 200
#     assert One().score((1,1,1)) == 300
#
# def test_Five_matches_true():
#     points = Five()
#     assert points.matches((1,1,2,2,3,5)) == True
#
# def test_Five_matches_false():
#     points = Five()
#     assert points.matches((1,2,2,3,4,6)) == False
#
# def test_Five_score():
#     assert Five().score((5,)) == 50
#     assert Five().score((5,5)) == 100

def test_scorer_SixOfAKind():
    scorer = Scorer((2,2,2,2,2,2))
    assert scorer.claim == [2,2,2,2,2,2]
    assert scorer.remainder == []
    assert scorer.points == 3000
    assert scorer.result == 'SixOfAKind'

def test_scorer_FiveOfAKind():
    scorer = Scorer((2,2,2,2,2,3))
    assert scorer.claim == [2,2,2,2,2]
    assert scorer.remainder == [3]
    assert scorer.points == 2000
    assert scorer.result == 'FiveOfAKind'

def test_scorer_FourOfAKind():
    scorer = Scorer((2,2,2,2,3,4))
    assert scorer.claim == [2,2,2,2]
    assert scorer.remainder == [3,4]
    assert scorer.points == 1000
    assert scorer.result == 'FourOfAKind'

def test_scorer_FourAndTwo():
    scorer = Scorer((2,2,2,2,3,3))
    assert scorer.claim == [2,2,2,2,3,3]
    assert scorer.remainder == []
    assert scorer.points == 1500
    assert scorer.result == 'FourAndTwo'

def test_scorer_TwoTriplets():
    scorer = Scorer((2,2,2,3,3,3))
    assert scorer.claim == [2,2,2,3,3,3]
    assert scorer.remainder == []
    assert scorer.points == 2500
    assert scorer.result == 'TwoTriplets'

def test_scorer_ThreePair():
    scorer = Scorer((2,2,3,3,4,4))
    assert scorer.claim == [2,2,3,3,4,4]
    assert scorer.remainder == []
    assert scorer.points == 1500
    assert scorer.result == 'ThreePair'

def test_scorer_FourOfAKind():
    scorer = Scorer((2,2,2,2,3,4))
    assert scorer.claim == [2,2,2,2]
    assert scorer.remainder == [3,4]
    assert scorer.points == 1000
    assert scorer.result == 'FourOfAKind'

def test_scorer_ThreeOfAKind():
    scorer = Scorer((1,1,1,3,4,6))
    assert scorer.claim == [1,1,1]
    assert scorer.remainder == [3,4,6]
    assert scorer.points == 300
    assert scorer.result == 'ThreeOfAKind'

    scorer = Scorer((2,2,2,3,4,6))
    assert scorer.claim == [2,2,2]
    assert scorer.remainder == [3,4,6]
    assert scorer.points == 200
    assert scorer.result == 'ThreeOfAKind'

    scorer = Scorer((3,3,3,2,4,6))
    assert scorer.claim == [3,3,3]
    assert scorer.remainder == [2,4,6]
    assert scorer.points == 300
    assert scorer.result == 'ThreeOfAKind'

    scorer = Scorer((4,4,4,2,3,6))
    assert scorer.claim == [4,4,4]
    assert scorer.remainder == [2,3,6]
    assert scorer.points == 400
    assert scorer.result == 'ThreeOfAKind'

    scorer = Scorer((5,5,5,2,3,6))
    assert scorer.claim == [5,5,5]
    assert scorer.remainder == [2,3,6]
    assert scorer.points == 500
    assert scorer.result == 'ThreeOfAKind'

    scorer = Scorer((6,6,6,2,3,1))
    assert scorer.claim == [6,6,6]
    assert scorer.remainder == [1,2,3]
    assert scorer.points == 600
    assert scorer.result == 'ThreeOfAKind'

    # scorer = Scorer((1,2,2,3,4,5))
    # assert set([(1,5), (1,), (5,)]) == scorer.claim()
