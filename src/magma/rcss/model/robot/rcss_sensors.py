from magma.agent.communication.perception import Perception
from magma.agent.model.robot.sensors import Sensor
from magma.common.math.geometry.vector import Vector3D
from magma.rcss.communication.rcss_perception import ForceResistancePerceptor


class ForceResistance(Sensor):
    """
    Force resistance sensor representation.
    """

    def __init__(self, name: str, frame_id: str, perceptor_name: str) -> None:
        """
        Construct a new force resistance sensor.
        """

        super().__init__(name, frame_id, perceptor_name)

        self._force: Vector3D = Vector3D()
        self._origin: Vector3D = Vector3D()

    def update(self, perception: Perception) -> None:
        perceptor = perception.get_perceptor(self._perceptor_name, ForceResistancePerceptor)

        if perceptor is not None:
            self._time = perception.get_time()
            self._force = perceptor.force
            self._origin = perceptor.origin
