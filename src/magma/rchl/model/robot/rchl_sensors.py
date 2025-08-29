from collections.abc import Sequence

from magma.agent.communication.perception import Perception
from magma.agent.model.robot.sensors import Sensor
from magma.rchl.communication.rchl_mitecom import RCHLTeamMessage
from magma.rchl.communication.rchl_perception import RCHLTeamComPerceptor


class RCHLTeamComSensor(Sensor):
    """Sensor implementation for receiving team communication."""

    def __init__(self, name: str, frame_id: str, perceptor_name: str) -> None:
        """Construct a new team communication sensor.

        Parameter
        ---------
        name : str
            The unique name of the sensor.

        frame_id : str
            The name of the body the sensor is attached to.

        perceptor_name : str
            The name of the perceptor associated with the sensor.
        """

        super().__init__(name, frame_id, perceptor_name)

        self._messages: Sequence[RCHLTeamMessage]
        """The collection of received team communication messages."""

    def get_messages(self) -> Sequence[RCHLTeamMessage]:
        """Return the collection of most recent team messages."""

        return self._messages

    def _update(self, perception: Perception) -> None:
        perceptor = perception.get_perceptor(self.perceptor_name, RCHLTeamComPerceptor)

        if perceptor is not None:
            self.set_time(perception.get_time())
            self._messages = perceptor.messages
