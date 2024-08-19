from datetime import date as Date
import functools
import pathlib
import ruamel.yaml
from typing import Literal, get_args, Optional

import pydantic


class BaseModel(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(extra="forbid")


# ======================================================================================
# Utilities for reading the publications.yaml file:
# ======================================================================================

available_categories = Literal[
    "Controls and Optimization",
    "Liquid Metals",
    "Machine Learning",
    "Special Topics",
]

available_types = Literal["Papers", "Presentations"]


class Publication(BaseModel):
    """This class defines the schema for a publication."""

    title: str
    type: available_types
    category: available_categories
    authors: list[str]
    date: str
    context: Optional[str] = None
    pdf_file_name: str

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

    @functools.cached_property
    def pdf_url(self) -> str:
        """Return the URL of the PDF file."""
        return f"https://github.com/PlasmaControl/GroupWebsite/blob/main/src/assets/data/publications/pdfs/{self.pdf_file_name}?raw=true"

    @pydantic.field_validator("date")
    @classmethod
    def validate_date(cls, date: str) -> str:
        """Validate that the date is in the format YYYY-MM-DD."""
        try:
            Date.fromisoformat(date)
        except ValueError:
            raise ValueError("The date must be in the format YYYY-MM-DD!")

        return date

    @pydantic.field_validator("pdf_file_name")
    @classmethod
    def validate_pdf_exists(cls, pdf_file_name: str) -> str:
        """Validate that the PDF file exists."""
        pdf_file_path = (
            pathlib.Path(__file__).parent / "publications" / "pdfs" / pdf_file_name
        )
        if not pdf_file_path.exists():
            raise FileNotFoundError(f"The file {pdf_file_name} does not exist!")

        return pdf_file_name


class Publications(BaseModel):
    """This class defines the schema for the publications.yaml file."""

    publications: list[Publication]

    @pydantic.field_validator("publications")
    @classmethod
    def sort_publications_by_date(cls, publications) -> list[Publication]:
        """Sort the publications by date in descending order."""
        return sorted(
            publications, key=lambda publication: publication.date, reverse=True
        )


class YearOfResearch(BaseModel):
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


# ======================================================================================
# ======================================================================================
# ======================================================================================


# ======================================================================================
# Utilities for reading the members.yaml file:
# ======================================================================================


class Member(BaseModel):
    """This class defines the schema for a member of the research group."""

    name: str
    title: str
    description: Optional[str] = pydantic.Field(default=None, max_length=900)
    emails: list[pydantic.EmailStr]
    photo_file_name: Optional[str] = None
    cv_file_name: Optional[str] = None
    google_scholar_url: Optional[str] = None
    orcid_id: Optional[str] = None
    github_username: Optional[str] = None

    @functools.cached_property
    def photo_url(self) -> Optional[str]:
        """Return the URL of the photo file."""
        if self.photo_file_name is not None:
            return f"https://github.com/PlasmaControl/GroupWebsite/blob/main/src/assets/data/members/photos/{self.photo_file_name}?raw=true"

        return None

    @functools.cached_property
    def cv_markdown_url(self) -> Optional[str]:
        """Return the URL of the CV file."""
        if self.cv_file_name is not None:
            return f"[CV](https://github.com/PlasmaControl/GroupWebsite/blob/main/src/assets/data/members/cvs/{self.cv_file_name}?raw=true)"

        return None

    @functools.cached_property
    def github_markdown_url(self) -> Optional[str]:
        """Return the URL of the GitHub profile."""
        if self.github_username is not None:
            return f"[:fontawesome-brands-github:](https://github.com/{self.github_username})"
        else:
            return ""

    @functools.cached_property
    def google_scholar_markdown_url(self) -> Optional[str]:
        """Return the URL of the Google Scholar profile."""
        if self.google_scholar_url is not None:
            return (
                "[Google"
                f" Scholar](https://scholar.google.com/citations?user={self.google_scholar_url})"
            )
        else:
            return ""

    @functools.cached_property
    def orcid_markdown_url(self) -> Optional[str]:
        """Return the URL of the ORCID profile."""
        if self.orcid_id is not None:
            return f"[:fontawesome-brands-orcid:](https://orcid.org/{self.orcid_id})"
        else:
            return ""

    @functools.cached_property
    def emails_markdown_urls(self) -> str:
        """Return a string with the emails separated by commas."""
        email_links = [f"[{email}](mailto:{email})" for email in self.emails]
        return ", ".join(email_links)

    @functools.cached_property
    def links(self) -> str:
        """Return a string with the links separated by commas."""
        links = [
            link
            for link in [
                self.orcid_markdown_url,
                self.google_scholar_markdown_url,
                self.cv_markdown_url,
                self.github_markdown_url,
            ]
            if link
        ]
        return ", ".join(links)

    @pydantic.field_validator("cv_file_name")
    @classmethod
    def validate_cv_exists(cls, cv_file_name: Optional[str]) -> Optional[str]:
        """Validate that the CV file exists."""
        if cv_file_name is not None:
            cv_file_path = (
                pathlib.Path(__file__).parent / "members" / "cvs" / cv_file_name
            )
            if not cv_file_path.exists():
                raise FileNotFoundError(f"The file {cv_file_name} does not exist!")

        return cv_file_name

    @pydantic.field_validator("photo_file_name")
    @classmethod
    def validate_photo_exists(cls, photo_file_name: Optional[str]) -> Optional[str]:
        """Validate that the photo file exists."""
        if photo_file_name is not None:
            photo_file_path = (
                pathlib.Path(__file__).parent / "members" / "photos" / photo_file_name
            )
            if not photo_file_path.exists():
                raise FileNotFoundError(f"The file {photo_file_name} does not exist!")

        return photo_file_name


class GroupMembers(BaseModel):
    """This class defines the schema for the members.yaml file."""

    principal_investigator: Member
    research_staff: list[Member]
    graduate_students: list[Member]
    undergraduate_students: list[Member]
    visiting_scholars: list[Member]
    past_members: list[Member]


# ======================================================================================
# ======================================================================================
# ======================================================================================


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

    @env.macro
    def members():
        members_file_path = pathlib.Path(__file__).parent / "members" / "members.yaml"

        if not members_file_path.exists():
            raise FileNotFoundError("The file members.yaml does not exist!")

        members_file_contents = members_file_path.read_text(encoding="utf-8")
        members_as_dictionary = ruamel.yaml.YAML().load(members_file_contents)
        group_members = GroupMembers(**members_as_dictionary)

        return group_members
