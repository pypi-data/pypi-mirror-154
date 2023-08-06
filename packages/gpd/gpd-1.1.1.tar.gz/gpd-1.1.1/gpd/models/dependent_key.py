from pydantic import BaseModel


class DependentKey(BaseModel):
    owner: str
    project: str
    max_page: int
