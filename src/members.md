---
toc_depth: 2
hide:
 - navigation
disable_comments: true
---

# Members

{% for people_category, people in members().items() %}

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

<p><strong>Contact: </strong>{{ person.emails_html_urls }}</p>
    </div>
</div>

{% endfor %}

{% endfor %}

