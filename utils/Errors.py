class PythonVersionError(ValueError):
    REQUIRED_VERSION = (3, 9)

    def __init__(self) -> None:
        super().__init__(f"This Project requires Python >= {self.REQUIRED_VERSION[0]}.{self.REQUIRED_VERSION[1]}")

    @staticmethod
    def validate_python() -> None:
        from sys import version_info
        if version_info < PythonVersionError.REQUIRED_VERSION:
            raise PythonVersionError()
