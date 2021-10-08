class NotFoundError(Exception):
    """To be raised when an element is not found on the repository."""
    pass

class KpiNotFoundError(NotFoundError):
    """To be raised when a kpi is not found on the repository."""
    def __init__(self) -> None:
        super().__init__(
            1001,
            "Resource not found",
            "Kpi doesn`t exist"
        )

class KpiGroupNotFoundError(NotFoundError):
    """To be raised when a kpi group is not found on the repository."""
    def __init__(self) -> None:
        super().__init__(
            1002,
            "Resource not found",
            "Kpi Group doesn`t exist"
        )

class PlaceNotFoundError(NotFoundError):
    """To be raised when a place is not found on the repository."""
    def __init__(self) -> None:
        super().__init__(
            1003,
            "Resource not found",
            "Place doesn`t exist"
        )
