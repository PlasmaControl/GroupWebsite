# GroupWebsite

This repository contains the source code of the [Plasma Control Group's website](http://control.princeton.edu/).

# How it works?

It uses [MkDocs](https://github.com/mkdocs/mkdocs) with the [MkDocs-Material](https://github.com/squidfunk/mkdocs-material) theme. MkDocs is a Python package. It takes the website's content ([`src`](https://github.com/PlasmaControl/GroupWebsite/tree/main/src)) and returns it as HTML, CSS, and JavaScript files, which are then deployed to Princeton University's servers.

Whenever something is pushed to the `main` branch, the website is rebuilt (i.e., HTML, CSS, and JavaScript files are generated using MkDocs) and deployed to Princeton Univerisity's servers with the workflow recipe defined in [`.github/workflows/deploy.yaml`](https://github.com/PlasmaControl/GroupWebsite/blob/main/.github/workflows/deploy.yaml).

The content is written with [Markdown](https://www.markdownguide.org/cheat-sheet/#basic-syntax) syntax, and on top of that, it supports various features such as

-   References with BibteX
-   Auto-numbered $\LaTeX$ equations
-   Diagrams written with [Mermaid](https://mermaid.js.org/syntax/flowchart.html)
-   Cross-referencing
-   Figures with captions
-   Many more.

Therefore, updating the content of the website is very easy.

# Updating the website

There are two ways of updating the website:

-   Creating a pull request
-   Using the [backend app](https://sa9942.mycpanel.princeton.edu/) ([source code](https://github.com/PlasmaControl/GroupWebsiteBackend) of the backend app). It is only for updating the "Members" and "Publications" pages.

## Creating a pull request

To get started, follow the steps below:

1.  Ensure that you have Python version 3.12 or higher.
2.  Fork the repository and clone it with the following command.
    ```
    git clone https://github.com/YOURUSERNAME/GroupWebsite.git
    ```
3.  Go to the `GroupWebsite` directory.
    ```
    cd GroupWebsite
    ```
4.  Create a virtual environment.
    ```
    python -m venv .venv
    ```
5.  Activate the virtual environment.
    -  Windows
        ```
        .venv\Scripts\activate
        ```
    -  MacOS and Linux
        ```
        source .venv/bin/activate
        ```
7.  Install the requirements to the virtual environment with the following command.
    ```
    pip install -r requirements.txt
    ```
9.  Run the following command.
    ```
    mkdocs serve
    ```
10. Then, go to [http://127.0.0.1:8000](http://127.0.0.1:8000/) and see your changes in real time. You can now start working on the website.

### Adding or editing a new page

All the files with `md` extensions are the pages. Create new ones or edit the existing ones. To add a new page to the navigation, see the [`mkdocs.yaml`](https://github.com/PlasmaControl/GroupWebsite/blob/main/mkdocs.yaml) file.

#### Features

To use inline $\LaTeX$ equations:

```markdown
This is an inline equation $\frac{3}{4}$.
```

To use block $\LaTeX$ equations:

```markdown
$$
\int_1^2 x^2 dx=\frac{x^3}{3}\Big|_{x=1}^{x=2}
$$
```

To auto-number the equations:

```markdown
$$
\begin{equation}
\int_1^2 x^2 dx=\frac{x^3}{3}\Big|_{x=1}^{x=2}
\end{equation}
$$
```

To cross-reference the equations:

```markdown
See [Equation 1](#eq:my_label).

$$
\begin{equation}
\int_1^2 x^2 dx=\frac{x^3}{3}\Big|_{x=1}^{x=2}
\end{equation}
$$
{ #eq:my_label }
```

To see all the available $\LaTeX$ commands, see [here](https://katex.org/docs/supported).


To add a figure without a caption:

```markdown
![](assets/images/group_photo.jpg){ #group-photo }
```

To add a figure with a caption:

```markdown
![This is the caption.](assets/images/group_photo.jpg)
```

To cross-reference the figures:

```markdown
See [](#fig:my_label).

![This is the caption.](assets/images/group_photo.jpg){ #fig:my_label }
```

To use Mermaid diagrams:

``````markdown
```mermaid
graph TD;
    A-->B;
    A-->C;
    B-->D;
    C-->D;
```
``````

To cite a reference:

```markdown
See [@my_reference].
```

and add the reference to the [`references.bib`](https://github.com/PlasmaControl/GroupWebsite/blob/main/src/assets/data/bibliography.bib) file.


### Updating the "Members" page

The "Members" page is created automatically from the [`members.yaml`](https://github.com/PlasmaControl/GroupWebsite/blob/main/src/assets/data/members/members.yaml) file. CVs and photos are stored in the [`cvs`](https://github.com/PlasmaControl/GroupWebsite/tree/main/src/assets/data/members/cvs) and [`photos`](https://github.com/PlasmaControl/GroupWebsite/tree/main/src/assets/data/members/photos) folders next to the `members.yaml` file.

### Updating the "Publications" page

The "Publications" page is created automatically from the [`publications.yaml`](https://github.com/PlasmaControl/GroupWebsite/blob/main/src/assets/data/publications/publications.yaml) file. All the PDFs are stored in the [`pdfs`](https://github.com/PlasmaControl/GroupWebsite/tree/main/src/assets/data/publications/pdfs)folder next to the `publications.yaml` file.
