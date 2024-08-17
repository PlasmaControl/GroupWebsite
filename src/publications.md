---
hide:
 - navigation
disable_comments: true
toc_depth: 1
---

# Publications

{% for publication in publications() %}
## {{ publication.year }}

    {% for category_title, papers_and_presentations in publication.categories.items() %}

### {{ category_title }}

        {% for type, publications in papers_and_presentations.items() %}
#### {{ type }}
            {% for publication in publications %}
- "{{ publication.title }}," {{ publication.author_list }}, {{ publication.context }}, {{ publication.beautiful_date }} ([link]({{ publication.pdf_url }}))
            {% endfor %}
        {% endfor %}


    {% endfor %}

{% endfor %}

