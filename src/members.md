---
toc_depth: 2
hide:
 - navigation
disable_comments: true
---

# Members

{% for people_category, people in members().items() %}
{% if people_category != "Past Members" %}
## {{ people_category }}

{% for person in people %}

### {{ person.name }}

<div class="member-container">
    <div class="member-photo">
        <img src="{{ person.photo_url }}">

        <p>{{ person.links }}</p>
    </div>

    <div class="member-description" markdown="span">
<p>{{ person.description }}</p>

{% if person.emails != [] %}
<p><strong>Contact: </strong>{{ person.emails_html_urls }}</p>
{% endif %}
    </div>
</div>

{% endfor %}

{% endif %}
{% endfor %}

## Past Members

<div class="grid cards" markdown>
{% for person in members()["Past Members"] %}
-  **{{ person.name }}**

    ---

    ![]({{ person.photo_url }})

{% endfor %}
</div>
