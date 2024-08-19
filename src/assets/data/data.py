from datetime import date as Date
import functools
import pathlib
import ruamel.yaml
from typing import Literal, get_args, Optional

import pydantic

# ======================================================================================
# Read the publications.yaml file and create a list of YearOfResearch objects
# ======================================================================================

available_categories = Literal[
    "Controls and Optimization",
    "Liquid Metals",
    "Machine Learning",
    "Special Topics",
]

available_types = Literal["Papers", "Presentations"]


class Publication(pydantic.BaseModel):
    """This class defines the schema for a publication."""

    title: str
    type: available_types
    category: available_categories
    authors: list[str]
    date: str
    context: Optional[str] = None
    pdf_url: pydantic.HttpUrl

    @functools.cached_property
    def date_object(self) -> Date:
        """Convert the date string to a date object."""
        return Date.fromisoformat(self.date)

    @functools.cached_property
    def beautiful_date(self) -> str:
        """Return the date in the format "Month Year"."""
        return self.date_object.strftime("%B %Y")

    @functools.cached_property
    def author_list(self) -> str:
        """Return a string with the authors separated by commas and the last two
        authors connected with "and"."""
        authors = [author for author in self.authors]
        # Connect all the authors with commas, except the last two, which are connected
        # with "and"
        if len(authors) > 1:
            authors[-1] = "and " + authors[-1]
            return ", ".join(authors)
        else:
            return authors[0]

    @functools.cached_property
    def year(self) -> int:
        """Return the year of the publication."""
        return self.date_object.year

    @pydantic.field_validator("date")
    @classmethod
    def validate_date(cls, date: str) -> str:
        """Validate that the date is in the format YYYY-MM-DD."""
        try:
            Date.fromisoformat(date)
        except ValueError:
            raise ValueError("The date must be in the format YYYY-MM-DD!")

        return date


class Publications(pydantic.BaseModel):
    """This class defines the schema for the publications.yaml file."""

    publications: list[Publication]

    @pydantic.field_validator("publications")
    @classmethod
    def sort_publications_by_date(cls, publications) -> list[Publication]:
        """Sort the publications by date in descending order."""
        return sorted(
            publications, key=lambda publication: publication.date, reverse=True
        )


class YearOfResearch(pydantic.BaseModel):
    """This class defines the schema for a year of research, which will be used in
    the `publications.md` file."""

    year: int
    publications: dict[str, dict[str, list[Publication]]]


def group_publications(
    publications: list[Publication],
    grouping_key: Literal["type", "category"],
) -> dict[str, list[Publication]]:
    """Group the publications by a key."""
    grouped_publications = {}
    for publication in publications:
        key = getattr(publication, grouping_key)
        if key not in grouped_publications:
            grouped_publications[key] = []
        grouped_publications[key].append(publication)
    return grouped_publications


def group_publications_by_type(
    publications: list[Publication],
) -> dict[str, list[Publication]]:
    """Group the publications by type."""
    return group_publications(publications, "type")


def group_publications_by_category(
    publications: list[Publication],
) -> dict[str, list[Publication]]:
    """Group the publications by category."""
    return group_publications(publications, "category")


def group_publications_by_year(
    publications: list[Publication],
) -> dict[int, list[Publication]]:
    """Group the publications by year."""
    return group_publications(publications, "year")


def define_env(env):

    @env.macro
    def year_of_research_objects():
        publications_file_path = (
            pathlib.Path(__file__).parent / "publications" / "publications.yaml"
        )

        if not publications_file_path.exists():
            raise FileNotFoundError("The file publications.yaml does not exist!")

        publications_file_contents = publications_file_path.read_text(encoding="utf-8")
        publications_as_dictionary = ruamel.yaml.YAML().load(publications_file_contents)
        publications = Publications(**publications_as_dictionary).publications

        # Find the maximum and minimum years of publication
        max_year = Date.today().year
        min_year = max_year
        for publication in publications:
            year = publication.date_object.year
            if year < min_year:
                min_year = year
            if year > max_year:
                max_year = year

        # Create YearOfResearch objects for each year
        year_of_research_objects = []
        publications_for_each_year = group_publications_by_year(publications)
        for year, publications in publications_for_each_year.items():
            publications_by_category = group_publications_by_category(publications)
            for (
                category,
                publications,
            ) in publications_by_category.items():
                publications_by_category[category] = group_publications_by_type(
                    publications
                )
            year_of_research_objects.append(
                YearOfResearch(
                    year=year,
                    publications=publications_by_category,
                )
            )

        return year_of_research_objects


# ======================================================================================
# ======================================================================================
# ======================================================================================
