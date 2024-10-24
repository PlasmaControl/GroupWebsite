from material.plugins.blog.structure import Archive, Category


def on_page_markdown(markdown, *, page, config, files):  # NOQA: ARG001
    if isinstance(page, Archive | Category):
        page.meta["hide"] = ["toc"]

    if "hide" in page.meta:
        page.meta["hide"].append("navigation")
    else:
        page.meta["hide"] = ["navigation"]
