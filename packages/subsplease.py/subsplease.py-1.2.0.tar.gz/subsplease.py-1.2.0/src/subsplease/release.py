class Release:
    """
    Represents a SubsPlease release.
    """
    def __init__(self, title: str, link: str, guid: str, release_date: str, tags: list, file_size: float, raw: dict) -> None:
        self._title = title 
        self._link = link 
        self._guid = guid 
        self._release_date = release_date
        self._tags = tags
        self._file_size = file_size
        self._raw = raw

    def __repr__(self) -> str:
        attrs = [
            ("title", self.title),
            ("link", self.link),
            ("guid", self.guid),
            ("release_date", self.release_date),
            ("tags", self.tags),
            ("file_size", self.file_size),
            ("raw", self.raw)
        ]
        joined = " ".join("%s=%r" % t for t in attrs)
        return f"<{self.__class__.__name__} {joined}>"

    @property
    def title(self):
        return self._title
    
    @property
    def link(self):
        return self._guid
    
    @property
    def release_date(self):
        return self._release_date
    
    @property
    def tags(self):
        return self._tags
    
    @property
    def file_size(self):
        return self._file_size

    @property
    def raw(self):
        return self._raw