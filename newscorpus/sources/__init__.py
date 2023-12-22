from pathlib import Path

from pydantic import BaseModel, RootModel

# Type definition of sources.json
# [
#     {
#         "id": "tagesschau",
#         "name": "Tagesschau",
#         "url": "https://www.tagesschau.de/xml/rss2"
#     },
#     ...
# ]


class Source(BaseModel):
    id: int
    name: str
    url: str


class SourceCollection(RootModel):
    root: list[Source]

    @classmethod
    def from_file(cls) -> "SourceCollection":
        """Load sources.json and return a list of Source objects"""
        path = Path(__file__).parent.resolve().joinpath("sources.json")

        with open(path, encoding="utf-8") as f:
            return cls.model_validate_json(f.read())
