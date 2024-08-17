from datetime import date as Date
import functools
import pathlib
import ruamel.yaml

import pydantic


class Author(pydantic.BaseModel):
    name: str
    orcid_id: str

    @functools.cached_property
    def orcid_url(self) -> pydantic.HttpUrl:
        return f"https://orcid.org/{self.orcid_id}"


class Publication(pydantic.BaseModel):
    title: str
    authors: list[Author]
    date: str
    doi: str
    journal: str
    pdf_url: pydantic.HttpUrl

    @functools.cached_property
    def doi_url(self) -> str:
        return f"https://doi.org/{self.doi}"

    @functools.cached_property
    def author_list(self) -> str:
        authors = [author.name for author in self.authors]
        return ", ".join(authors)

    @pydantic.field_validator("date")
    @classmethod
    def validate_date(cls, date: str) -> str:
        try:
            date_object = Date.fromisoformat(date)
            return date_object.strftime("%B %Y")
        except ValueError:
            raise ValueError("The date must be in the format YYYY-MM-DD!")


class Publications(pydantic.BaseModel):
    publications: list[Publication]

    @pydantic.field_validator("publications")
    @classmethod
    def sort_publications_by_date(cls, publications) -> list[Publication]:
        return sorted(
            publications, key=lambda publication: publication.date, reverse=True
        )


def define_env(env):

    @env.macro
    def publications():
        publications_file_path = pathlib.Path(__file__).parent / "publications.yaml"

        if not publications_file_path.exists():
            raise FileNotFoundError("The file publications.yaml does not exist!")

        publications_file_contents = publications_file_path.read_text(encoding="utf-8")
        publications_as_dictionary = ruamel.yaml.YAML().load(publications_file_contents)
        publications = Publications(**publications_as_dictionary)

        return publications.publications
