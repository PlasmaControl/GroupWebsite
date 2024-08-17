from datetime import date as Date
import functools
import pathlib
import ruamel.yaml
from typing import Literal, get_args, Optional

import pydantic


available_categories = Literal[
    "Controls and Optimization",
    "Liquid Metals",
    "Machine Learning",
    "Special Topics",
]

available_types = Literal["Papers", "Presentations"]


class Publication(pydantic.BaseModel):
    title: str
    type: available_types
    category: available_categories
    authors: list[str]
    date: str
    context: Optional[str] = None
    pdf_url: pydantic.HttpUrl

    @functools.cached_property
    def date_object(self) -> Date:
        return Date.fromisoformat(self.date)

    @functools.cached_property
    def beautiful_date(self) -> str:
        return self.date_object.strftime("%B %Y")

    @functools.cached_property
    def author_list(self) -> str:
        authors = [author for author in self.authors]
        # Connect all the authors with commas, except the last two, which are connected
        # with "and"
        if len(authors) > 1:
            authors[-1] = "and " + authors[-1]
            return ", ".join(authors)
        else:
            return authors[0]

    @pydantic.field_validator("date")
    @classmethod
    def validate_date(cls, date: str) -> str:
        try:
            date_object = Date.fromisoformat(date)
        except ValueError:
            raise ValueError("The date must be in the format YYYY-MM-DD!")

        return date


class Publications(pydantic.BaseModel):
    publications: list[Publication]

    @pydantic.field_validator("publications")
    @classmethod
    def sort_publications_by_date(cls, publications) -> list[Publication]:
        return sorted(
            publications, key=lambda publication: publication.date, reverse=True
        )


class YearOfResearch(pydantic.BaseModel):
    year: int
    categories: dict[str, dict[str, list[Publication]]]


def define_env(env):

    @env.macro
    def publications():
        publications_file_path = pathlib.Path(__file__).parent / "publications.yaml"

        if not publications_file_path.exists():
            raise FileNotFoundError("The file publications.yaml does not exist!")

        publications_file_contents = publications_file_path.read_text(encoding="utf-8")
        publications_as_dictionary = ruamel.yaml.YAML().load(publications_file_contents)
        publications = Publications(**publications_as_dictionary)

        # Find the maximum and minimum years of publication
        max_year = Date.today().year
        min_year = max_year
        for publication in publications.publications:
            year = publication.date_object.year
            if year < min_year:
                min_year = year
            if year > max_year:
                max_year = year

        # Create YearOfResearch objects for each year
        years_of_research = []
        categories = get_args(available_categories)
        for year in range(min_year, max_year + 1):
            publications_for_each_category = {}
            for category in categories:
                publications_in_category = [
                    publication
                    for publication in publications.publications
                    if publication.category == category
                    and publication.date_object.year == year
                ]
                if publications_in_category:
                    publications_for_each_category[category] = {}
                    for publication in publications_in_category:
                        types = get_args(available_types)
                        for type in types:
                            publications_in_type = [
                                publication
                                for publication in publications_in_category
                                if publication.type == type
                            ]
                            if publications_in_type:
                                publications_for_each_category[category][
                                    type
                                ] = publications_in_type

            if publications_for_each_category:
                years_of_research.append(
                    YearOfResearch(year=year, categories=publications_for_each_category)
                )

        return years_of_research
