from typing import Final

from magmapy.common.math.geometry.angle import ANGLE_ZERO
from magmapy.soccer_agent.model.strategy.roles import DummyRole
from magmapy.soccer_agent.model.strategy.strategy import TeamStrategy

# fmt: off
DEFAULT_11_VS_11_STRATEGY: Final[TeamStrategy] = TeamStrategy(
    name='default-11-vs-11',
    goalie_role=DummyRole(-0.95, 0, ANGLE_ZERO, 'dummy-goalie', 0.0),  # no: 1
    dynamic_roles=[
        DummyRole(-0.75,  0.6, None, 'dummy-defender-1',   0.0),  # no:  2
        DummyRole(-0.75,  0.2, None, 'dummy-defender-2',   0.0),  # no:  3
        DummyRole(-0.75, -0.2, None, 'dummy-defender-3',   0.0),  # no:  4
        DummyRole(-0.75, -0.6, None, 'dummy-defender-4',   0.0),  # no:  5
        DummyRole(-0.5,   0.4, None, 'dummy-midfielder-1', 0.0),  # no:  6
        DummyRole(-0.5,   0  , None, 'dummy-midfielder-2', 0.0),  # no:  7
        DummyRole(-0.5,  -0.4, None, 'dummy-midfielder-3', 0.0),  # no:  8
        DummyRole(-0.25,  0.3, None, 'dummy-wing-1',       0.0),  # no:  9
        DummyRole(-0.25, -0.3, None, 'dummy-wing-2',       0.0),  # no: 10
    ],
    active_player_role=DummyRole(-0.15, 0, ANGLE_ZERO, 'dummy-striker', 0.0),  # no: 11
)
# fmt: on
"""The default 11 vs 11 team strategy."""
