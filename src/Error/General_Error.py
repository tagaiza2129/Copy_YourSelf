class ExtensionsNotFoundError(Exception):
    def __init__(self,Extension:str):
        self.Extension=Extension
    def __str__(self) -> str:
        return repr(f"{self.Extension}が見つかりませんでした")