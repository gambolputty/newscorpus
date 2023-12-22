from pathlib import Path

from pydantic import BaseModel, RootModel, model_validator

# Type definition of sources.json
# [
#     {
#         "id": "tagesschau",
#         "name": "Tagesschau",
#         "url": "https://www.tagesschau.de/xml/rss2"
#     },
#     ...
# ]

DEFAULT_SOURCES_PATH = Path(__file__).parent.resolve().joinpath("sources.json")


class Source(BaseModel):
    id: int
    name: str
    url: str


class SourceCollection(RootModel):
    root: list[Source]

    # validate: each Source item must have a unique id
    @model_validator(mode="after")
    def validate_unique_id(self):
        ids = [item.id for item in self.root]
        if len(ids) != len(set(ids)):
            raise ValueError("Source id must be unique")
        return self

    @classmethod
    def from_file(
        cls,
        path: Path | str | None = None,
    ) -> "SourceCollection":
        """Load sources.json and return a list of Source objects"""

        with open(path or DEFAULT_SOURCES_PATH, encoding="utf-8") as f:
            return cls.model_validate_json(f.read())
