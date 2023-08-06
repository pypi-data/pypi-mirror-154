from pydantic import BaseModel


class Dependent(BaseModel):
    name: str
    stars: int
    forks: int
    author: str
    url: str

    def __hash__(self):
        return hash((self.name, self.stars, self.forks, self.author, self.url))
