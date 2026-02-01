class InsufficientCapacityException(Exception):
    """Exception raised when a payload exceeds the payload capacity of a cover image."""

    def __init__(
        self, payload_size: int, cover_image_capacity: int, message: str = None
    ):
        """
        Creates an instance of the InsufficientCapacityException class.
        :param payload_size: Size of the payload in bytes.
        :param cover_image_capacity: Maximum payload capacity of the cover image.
        :param message: Optional custom exception message.
        """
        self.payload_size = payload_size
        self.capacity = cover_image_capacity

        if message is None:
            message = f"payload of {self.payload_size} bytes exceeds cover image capacity of {self.capacity} bytes"
        super().__init__(message)


class UnsupportedColorSpaceError(Exception):
    """Exception raised when the image color space is not supported."""

    def __init__(self, message: str = "unsupported color space"):
        """
        Creates an instance of the UnsupportedColorSpaceError class.
        :param message: The default error message.
        """
        super().__init__(message)
