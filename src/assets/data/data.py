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
    title: str = pydantic.Field(default="")
    description: str = pydantic.Field(default="", max_length=900)
    emails: list[pydantic.EmailStr] = []
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
        else:
            return f"https://github.com/PlasmaControl/GroupWebsite/blob/main/src/assets/data/members/photos/person?raw=true"

    @functools.cached_property
    def cv_html_url(self) -> Optional[str]:
        """Return the URL of the CV file."""
        if self.cv_file_name is not None:
            return (
                f'<a href="https://github.com/PlasmaControl/GroupWebsite/blob/main/src/assets/data/members/cvs/{self.cv_file_name}?raw=true">CV</a>'
            )

    @functools.cached_property
    def github_html_url(self) -> Optional[str]:
        """Return the URL of the GitHub profile."""
        if self.github_username is not None:
            return (
                f'<a href="https://github.com/{self.github_username}"><span'
                ' class="twemoji"><svg xmlns="http://www.w3.org/2000/svg" viewbox="0 0'
                ' 496 512"><!--! Font Awesome Free 6.5.2 by @fontawesome -'
                " https://fontawesome.com License -"
                " https://fontawesome.com/license/free (Icons: CC BY 4.0, Fonts: SIL"
                " OFL 1.1, Code: MIT License) Copyright 2024 Fonticons, Inc.--><path"
                ' d="M165.9 397.4c0 2-2.3 3.6-5.2 3.6-3.3.3-5.6-1.3-5.6-3.6 0-2'
                " 2.3-3.6 5.2-3.6 3-.3 5.6 1.3 5.6 3.6zm-31.1-4.5c-.7 2 1.3 4.3 4.3"
                " 4.9 2.6 1 5.6 0 6.2-2s-1.3-4.3-4.3-5.2c-2.6-.7-5.5.3-6.2"
                " 2.3zm44.2-1.7c-2.9.7-4.9 2.6-4.6 4.9.3 2 2.9 3.3 5.9 2.6 2.9-.7"
                " 4.9-2.6 4.6-4.6-.3-1.9-3-3.2-5.9-2.9zM244.8 8C106.1 8 0 113.3 0"
                " 252c0 110.9 69.8 205.8 169.5 239.2 12.8 2.3 17.3-5.6 17.3-12.1"
                " 0-6.2-.3-40.4-.3-61.4 0 0-70 15-84.7-29.8 0 0-11.4-29.1-27.8-36.6 0"
                " 0-22.9-15.7 1.6-15.4 0 0 24.9 2 38.6 25.8 21.9 38.6 58.6 27.5 72.9"
                " 20.9 2.3-16 8.8-27.1 16-33.7-55.9-6.2-112.3-14.3-112.3-110.5 0-27.5"
                " 7.6-41.3 23.6-58.9-2.6-6.5-11.1-33.3 2.6-67.9 20.9-6.5 69 27 69 27"
                " 20-5.6 41.5-8.5 62.8-8.5s42.8 2.9 62.8 8.5c0 0 48.1-33.6 69-27 13.7"
                " 34.7 5.2 61.4 2.6 67.9 16 17.7 25.8 31.5 25.8 58.9 0 96.5-58.9"
                " 104.2-114.8 110.5 9.2 7.9 17 22.9 17 46.4 0 33.7-.3 75.4-.3 83.6 0"
                " 6.5 4.6 14.4 17.3 12.1C428.2 457.8 496 362.9 496 252 496 113.3 383.5"
                " 8 244.8 8zM97.2 352.9c-1.3 1-1 3.3.7 5.2 1.6 1.6 3.9 2.3 5.2 1 1.3-1"
                " 1-3.3-.7-5.2-1.6-1.6-3.9-2.3-5.2-1zm-10.8-8.1c-.7 1.3.3 2.9 2.3 3.9"
                " 1.6 1 3.6.7 4.3-.7.7-1.3-.3-2.9-2.3-3.9-2-.6-3.6-.3-4.3.7zm32.4"
                " 35.6c-1.6 1.3-1 4.3 1.3 6.2 2.3 2.3 5.2 2.6 6.5 1"
                " 1.3-1.3.7-4.3-1.3-6.2-2.2-2.3-5.2-2.6-6.5-1zm-11.4-14.7c-1.6 1-1.6"
                " 3.6 0 5.9 1.6 2.3 4.3 3.3 5.6 2.3 1.6-1.3 1.6-3.9"
                ' 0-6.2-1.4-2.3-4-3.3-5.6-2z"></path></svg></span></a>'
            )

    @functools.cached_property
    def google_scholar_html_url(self) -> Optional[str]:
        """Return the URL of the Google Scholar profile."""
        if self.google_scholar_url is not None:
            return f'<a href="{self.google_scholar_url}">Google Scholar</a>'

    @functools.cached_property
    def orcid_html_url(self) -> Optional[str]:
        """Return the URL of the ORCID profile."""
        if self.orcid_id is not None:
            return (
                f'<a href="https://orcid.org/{self.orcid_id}"><span'
                ' class="twemoji"><svg xmlns="http://www.w3.org/2000/svg" viewbox="0 0'
                ' 512 512"><!--! Font Awesome Free 6.5.2 by @fontawesome -'
                " https://fontawesome.com License -"
                " https://fontawesome.com/license/free (Icons: CC BY 4.0, Fonts: SIL"
                " OFL 1.1, Code: MIT License) Copyright 2024 Fonticons, Inc.--><path"
                ' d="M294.75 188.19h-45.92V342h47.47c67.62 0 83.12-51.34 83.12-76.91'
                " 0-41.64-26.54-76.9-84.67-76.9zM256 8C119 8 8 119 8 256s111 248 248"
                " 248 248-111 248-248S393 8 256 8zm-80.79"
                " 360.76h-29.84v-207.5h29.84zm-14.92-231.14a19.57 19.57 0 1 1"
                " 19.57-19.57 19.64 19.64 0 0 1-19.57 19.57zM300"
                " 369h-81V161.26h80.6c76.73 0 110.44 54.83 110.44 103.85C410 318.39"
                ' 368.38 369 300 369z"></path></svg></span></a>'
            )

    @functools.cached_property
    def emails_html_urls(self) -> str:
        """Return a string with the emails separated by commas."""
        email_links = [f"<a href='mailto:{email}'>{email}</a>" for email in self.emails]
        return ", ".join(email_links)

    @functools.cached_property
    def links(self) -> str:
        """Return a string with the links separated by commas."""
        links = [
            link
            for link in [
                self.orcid_html_url,
                self.github_html_url,
                self.google_scholar_html_url,
                self.cv_html_url,
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


class GraduateStudentMember(Member):
    title: Literal[
        "1st Year Graduate Student",
        "2nd Year Graduate Student",
        "3rd Year Graduate Student",
        "4th Year Graduate Student",
        "5th Year Graduate Student",
    ]


class GroupMembers(BaseModel):
    """This class defines the schema for the members.yaml file."""

    principal_investigator: list[Member]
    research_staff: list[Member]
    graduate_students: list[GraduateStudentMember]
    undergraduate_students: list[Member]
    visiting_scholars: list[Member]
    past_members: list[Member]

    @pydantic.field_validator(
        "principal_investigator",
        "research_staff",
        "undergraduate_students",
        "visiting_scholars",
        "past_members",
    )
    @classmethod
    def sort_members_alphabetically(cls, members) -> list[Member]:
        """Sort the publications by date in descending order."""
        return sorted(members, key=lambda member: member.name)

    @pydantic.field_validator(
        "graduate_students",
    )
    @classmethod
    def sort_graduate_students(cls, members) -> list[Member]:
        """Sort the publications by date in descending order."""
        alphabetical = sorted(members, key=lambda member: member.name)
        by_year = sorted(alphabetical, key=lambda member: member.title, reverse=True)
        return by_year


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

        group_members = {
            "Principal Investigator": group_members.principal_investigator,
            "Research Staff": group_members.research_staff,
            "Graduate Students": group_members.graduate_students,
            "Undergraduate Students": group_members.undergraduate_students,
            "Visiting Scholars": group_members.visiting_scholars,
            "Past Members": group_members.past_members,
        }

        return group_members
