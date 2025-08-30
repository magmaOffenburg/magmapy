from collections.abc import Sequence

from magmapy.agent.communication.perception import Perception
from magmapy.agent.model.robot.sensors import VisionSensor
from magmapy.rcss.communication.rcss_perception import RCSSLineDetection, RCSSPlayerDetection, RCSSVisionPerceptor


class RCSSVisionSensor(VisionSensor):
    """Soccer simulation specific vision pipeline sensor representation."""

    def __init__(self, name: str, frame_id: str, perceptor_name: str, h_fov: float, v_fov: float) -> None:
        """Construct a new vision pipeline sensor.

        Parameter
        ---------
        name : str
            The unique name of the sensor.

        frame_id : str
            The name of the body the sensor is attached to.

        perceptor_name : str
            The name of the perceptor associated with the sensor.

        h_fov : float
            The horizontal field of view.

        v_fov : float
            The vertical field of view.
        """

        super().__init__(name, frame_id, perceptor_name, h_fov, v_fov)

        self._lines: Sequence[RCSSLineDetection] = []
        """The collection of line detections."""

        self._players: Sequence[RCSSPlayerDetection] = []
        """The collection of player detections."""

    def get_line_detections(self) -> Sequence[RCSSLineDetection]:
        """Return the collection of most recent line detections."""

        return self._lines

    def get_player_detections(self) -> Sequence[RCSSPlayerDetection]:
        """Return the collection of most recent player detections."""

        return self._players

    def _update(self, perception: Perception) -> None:
        perceptor = perception.get_perceptor(self.perceptor_name, RCSSVisionPerceptor)

        if perceptor is not None:
            self.set_time(perception.get_time())
            self._objects = perceptor.objects
            self._lines = perceptor.lines
            self._players = perceptor.players
