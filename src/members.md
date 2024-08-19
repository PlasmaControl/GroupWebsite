---
toc_depth: 2
hide:
 - navigation
disable_comments: true
---

# Members

## Principal Investigator

### {{ members().principal_investigator.name }} ({{ members().principal_investigator.links }})

![]({{ members().principal_investigator.photo_url }})

{{ members().principal_investigator.description }}

**Contact**: {{ members().principal_investigator.emails_markdown_urls }}

## Research Staff

{% for member in members().research_staff %}
### {{ member.name }}

![]({{ member.photo_url }})

{{ member.description }}
{% endfor %}

## Graduate Students

{% for member in members().graduate_students %}
### {{ member.name }}

![]({{ member.photo_url }})

{{ member.description }}
{% endfor %}

## Undergraduate Students

{% for member in members().undergraduate_students %}

### {{ member.name }}

![]({{ member.photo_url }})

{{ member.description }}
{% endfor %}

## Visiting Scholars

{% for member in members().visiting_scholars %}
### {{ member.name }}

![]({{ member.photo_url }})

{{ member.description }}
{% endfor %}
