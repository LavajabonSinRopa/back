import unittest
import pytest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from entities.cards.figure_cards import print_figure, normalize_card, rotate_card, figure_exists, figure_card_types_hard, figure_card_types_easy

def test_find_figures_that_exist():
    for card in figure_card_types_hard:
        for rotation in range(4):
            card = rotate_card(card)
            assert figure_exists(card)
    for card in figure_card_types_easy:
        for rotation in range(4):
            card = rotate_card(card)
            assert figure_exists(card)

def test_find_figures_that_dont_exist():
    card = [[0,0]]*4
    assert not figure_exists(card)
    card = [[0,0]]*3
    assert not figure_exists(card)
    card = [[0,0]]*6
    assert not figure_exists(card)
    card = [[0,0]]*0
    assert not figure_exists(card)
    card = [[0,0],[0,2],[0,4],[0,6]]
    assert not figure_exists(card)

#test medio a ojo por ahora. no sé como definir la rotación sin usar la misma cuenta que usa el rotate_card()
def test_rotate_card():
    figura = [[0,0],[0,1],[0,2],[1,1],[1,-1]]
    n = len(figura)
    exists = figure_exists(figura)
    for rotation in range(4):
        figura = rotate_card(figura)
        assert len(figura) == n
        assert figure_exists(figura) == exists
        print_figure(figura)

def test_normalize_card():
    figura = [[-3,0],[0,1],[0,2],[1,1],[1,-1]]
    assert len(normalize_card(figura))==len(figura)
    assert normalize_card(figura)[0] == [0,0]
    figura = [[0,0],[0,1],[0,2],[1,-1],[1,1]]
    assert normalize_card(figura) == figura

if __name__ == "__main__":
    unittest.main()