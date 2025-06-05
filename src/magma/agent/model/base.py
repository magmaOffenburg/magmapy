from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from magma.agent.communication.perception import Perception


@runtime_checkable
class PMutableModel(Protocol):
    """Protocol for mutable models."""

    def update(self, perception: Perception) -> None:
        """Update the state of the model from the given perceptions.

        Parameter
        ---------
        perception : Perception
            The collection of perceived sensor information.
        """
