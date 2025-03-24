---
toc_depth: 2
disable_comments: true
---

# Members

![](assets/images/group_photo_2.png){ #group-photo }

{% for people_category, people in members().items() %}
{% if people_category not in ["Past Members"] %}
## {{ people_category }}

{% for person in people %}

<div class="member-wrapper">
    <h3 id="{{ person.h3_id }}">
        {{ person.name }} {% if people_category not in ["Principal Investigator"] %}({{ person.title }}) {% endif %}
        <a class="headerlink" href="#{{ person.h3_id }}" title="Permanent link">¶</a>
    </h3>

    <div class="member-container">
        <div class="member-photo">
            <img src="../{{ person.photo_url }}">

            {% if person.links %}<p>{{ person.links }}</p>{% endif %}
        </div>

        <div class="member-description" markdown="span">
    <p>{{ person.description }}</p>

    {% if person.emails != [] %}
    <p><strong>Contact: </strong>{{ person.emails_html_urls }}</p>
    {% endif %}
        </div>
    </div>
</div>
{% endfor %}

{% endif %}
{% endfor %}

## Past Members

<div class="past-member-grid grid" markdown>
{% for person in members()["Past Members"] %}
-  **{{ person.name }}**

    ---
    ![]({{ person.photo_url }})

{% endfor %}
</div>
