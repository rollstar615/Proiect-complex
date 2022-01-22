from domain.jucator import Jucator


def test_car():

    c1 = Jucator(1, 231, 'p', 3)
    assert c1.id_jucator == 1
    assert c1.nume == 231
    assert c1.sex == 'p'
    assert c1.ranking == 3


test_car()



