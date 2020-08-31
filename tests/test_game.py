#!/usr/bin/env python

import pytest
import pygame
from absolutris import game
from absolutris import errors
from absolutris import testhelper


def test_raise_GuiNotImplemented() -> None:
    """
    Tests if GuiNotImplemented error is raised when user selected a not implemented or non-instantiated gui, e.g.
    $ absolutris -g missing_gui
    """
    with pytest.raises(errors.GuiNotImplemented):
        testhelper.config.cli = testhelper.Cli(gui="not_instantiated")
        game_test = game.Game(testhelper.config)


def test_raise_PlanNotImplemented() -> None:
    """
    Tests if PlanNotImplemented error is raised when user selected a not implemented or non-instantiated plan, e.g.
    $ absolutris -p missing_plan
    """
    with pytest.raises(errors.PlanNotImplemented):
        testhelper.config.cli = testhelper.Cli(plan="not_instantiated")
        game_test = game.Game(testhelper.config)


def test_game_with_gui() -> None:
    """
    Tests the instance fuinctions of game.Game()
    """
    # test the instantiation of a game for every gui instance (`gi`)
    for gi_name, gi in testhelper.find_gui_instances():
        testhelper.config.cli = testhelper.Cli(gui=gi_name)
        # test Game.__init__()
        game_instance = game.Game(testhelper.config)
        assert type(game_instance) is game.Game
        # test Game.setup_game_window()
        pygame.init()
        game_instance.setup_game_window()
        assert type(game_instance.game_window) is pygame.Surface


# Disabling test, no-gui game is used only for debugging purposes anyway
# def test_no_gui_game() -> None:
    # """
    # Tests if a game can be run without gui
    # """
    # testhelper.config.cli = testhelper.Cli(download=False, gui=None, stats=False, verbose=False)
    # assert game.run(testhelper.config) is None
