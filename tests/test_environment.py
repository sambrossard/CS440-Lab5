"""Tests for the vacuum grid environment."""

import pytest

from vacuum.environment import WALL, make_vacuum_mdp, to_cell, to_xy


@pytest.fixture
def mdp():
    """The default vacuum grid."""
    return make_vacuum_mdp(living_reward=-0.04, gamma=0.9)


def test_fifteen_reachable_states(mdp):
    assert len(mdp.states) == 15


def test_wall_is_not_a_state(mdp):
    assert to_xy(WALL) not in mdp.states


def test_start_is_top_left(mdp):
    assert to_cell(mdp.init) == (0, 0)


def test_terminals_and_rewards(mdp):
    assert {to_cell(s) for s in mdp.terminals} == {(3, 1), (3, 3)}
    assert mdp.R(to_xy((3, 1))) == -1
    assert mdp.R(to_xy((3, 3))) == 10
    assert mdp.R(to_xy((2, 2))) == -0.04


def test_coordinate_round_trip():
    for row in range(4):
        for col in range(4):
            assert to_cell(to_xy((row, col))) == (row, col)


def test_moving_into_wall_stays_put(mdp):
    # From (1,0), moving right (+x) would enter the wall at (1,1).
    assert mdp.go(to_xy((1, 0)), (1, 0)) == to_xy((1, 0))


def test_moving_off_grid_stays_put(mdp):
    assert mdp.go(to_xy((0, 0)), (0, 1)) == to_xy((0, 0))


def test_zero_living_reward_rejected():
    with pytest.raises(ValueError):
        make_vacuum_mdp(living_reward=0)
