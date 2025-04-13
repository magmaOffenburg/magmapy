from __future__ import annotations

from magma.common.math.geometry.vector import Vector3D


class VisibleObject:
    """
    Representation of a visible object in the world.
    """

    def __init__(self,
                 name: str,
                 position: Vector3D | None = None) -> None:
        """
        Construct a new visible object.
        """

        self._name: str = name
        self._position: Vector3D = Vector3D() if position is None else position

    def get_name(self) -> str:
        """
        Retrieve the name of the visible object.
        """

        return self._name

    def get_position(self) -> Vector3D:
        """
        Retrieve the perceived position of the visible object.
        """

        return self._position


class MovableObject(VisibleObject):
    """
    Representation of a movable object in the world.
    """

    def __init__(self,
                 name: str,
                 position: Vector3D | None = None,
                 velocity: Vector3D | None = None) -> None:
        """
        Construct a new movable object.
        """

        super().__init__(name, position)

        self._velocity: Vector3D = Vector3D() if velocity is None else velocity

    def get_velocity(self) -> Vector3D:
        """
        Retrieve the perceived velocity of the object.
        """

        return self._velocity


class Landmark(VisibleObject):
    """
    Representation of a static landmark object in the world.
    """

    def __init__(self,
                 name: str,
                 l_type: str,
                 position: Vector3D | None = None) -> None:
        """
        Construct a new landmark object.
        """

        super().__init__(name, position)

        self._type: str = l_type

    def get_type(self) -> str:
        """
        Retrieve the type of landmark object.
        """

        return self._type


class PointLandmark(Landmark):
    """
    Representation of a static, punctual landmark object in the world.
    """

    def __init__(self,
                 name: str,
                 l_type: str,
                 known_position: Vector3D,
                 position: Vector3D | None = None) -> None:
        """
        Construct a new point landmark object.
        """

        super().__init__(name, l_type, position)

        self._known_position: Vector3D = known_position

    def get_known_position(self) -> Vector3D:
        """
        Retrieve the known position of this point landmark.
        """

        return self._known_position


class LineLandmark(Landmark):
    """
    Representation of a static, line segment landmark object in the world.
    """

    def __init__(self,
                 name: str,
                 l_type: str,
                 known_position1: Vector3D,
                 known_position2: Vector3D,
                 position: Vector3D | None = None) -> None:
        """
        Construct a new line segment landmark object.
        """

        super().__init__(name, l_type, position)

        self._known_position1: Vector3D = known_position1
        self._known_position2: Vector3D = known_position2

    def get_known_position1(self) -> Vector3D:
        """
        Retrieve the first known position of this line segment landmark.
        """

        return self._known_position1

    def get_known_position2(self) -> Vector3D:
        """
        Retrieve the second known position of this line segment landmark.
        """

        return self._known_position2
