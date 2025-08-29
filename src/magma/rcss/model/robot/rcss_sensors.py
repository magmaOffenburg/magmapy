from magma.agent.communication.perception import Perception
from magma.agent.model.robot.sensors import Sensor
from magma.common.math.geometry.vector import V3D_ZERO, Vector3D
from magma.rcss.communication.rcss_perception import ForceResistancePerceptor


class ForceResistance(Sensor):
    """Force resistance sensor representation."""

    def __init__(self, name: str, frame_id: str, perceptor_name: str) -> None:
        """Construct a new force resistance sensor.

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

        self._force: Vector3D = V3D_ZERO
        """The sensed force vector."""

        self._origin: Vector3D = V3D_ZERO
        """The sensed force origin."""

    def _update(self, perception: Perception) -> None:
        perceptor = perception.get_perceptor(self.perceptor_name, ForceResistancePerceptor)

        if perceptor is not None:
            self.set_time(perception.get_time())
            self._force = perceptor.force
            self._origin = perceptor.origin
