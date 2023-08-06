class PathIsEmpty(Exception):
    " Error If Path Is Not Specified "
    def __init__(self,*args: object) -> None:
        super().__init__("File Path Not Found")

class LogicError(Exception):
    " Logic throws an error when a mistake is made "
    def __init__(self, *args: object) -> None:
        super().__init__("Logic Error")

class VersionFileNotFound(Exception):
    " Error when version file does not exist "
    def __init__(self, *args: object) -> None:
        super().__init__("Create version.json first!")