---
disable_comments: true
---

# Members

{% for publication in publications() -%}
- **{{ publication.title }}** [:fontawesome-regular-file-pdf:]({{ publication.pdf_url }}) 

    published in *{{ publication.journal }}* ({{ publication.date }})

    {{ publication.author_list }}

    DOI: [{{ publication.doi }}]({{ publication.doi_url }})


{% endfor %}

