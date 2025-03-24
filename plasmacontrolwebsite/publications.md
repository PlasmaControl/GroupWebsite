---
disable_comments: true
toc_depth: 1
---

# Publications

[Find the publications on Google Scholar as well](https://scholar.google.com/citations?hl=en&user=-GHcoUYAAAAJ)

{% for year_of_research in year_of_research_objects() %}
## {{ year_of_research.year }}

    {% for category_title, publications in year_of_research.publications.items() %}

### {{ category_title }}

        {% for type, publications in publications.items() %}
#### {{ type }}

            {% for publication in publications %}
- "{{ publication.title }}," {{ publication.author_list }}{% if publication.context %}, {{ publication.context }}{% endif %}, {{ publication.beautiful_date }}{% if publication.pdf_url %}, [:fontawesome-regular-file-pdf:]({{ publication.pdf_url }}){% endif %}
            {% endfor %}
        {% endfor %}


    {% endfor %}

{% endfor %}