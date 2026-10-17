import pytest
from django.urls import reverse
from django.utils.translation import override
from playwright.sync_api import Page, expect

from blog.tests.factories import PostFactory, TagFactory


@pytest.mark.parametrize("width", [375, 640, 641, 767, 768, 769, 1024, 1440])
@pytest.mark.parametrize("embedded", [False, True])
def test_related_layout_and_pagination(page: Page, live_server, width, embedded):
    tag = TagFactory.create()
    source = PostFactory.create(tags=[tag])
    for index in range(9):
        PostFactory.create(tags=[tag], title=f"Related {index} " + "LongTitle" * 20)

    with override("en"):
        route = (
            reverse("post_detail", kwargs={"slug": source.slug})
            if embedded
            else reverse("related_posts", kwargs={"post_id": source.pk})
        )
    page.set_viewport_size({"width": width, "height": 900})
    page.goto(f"{live_server.url}{route}")
    cards = page.locator(".related-card")
    expect(cards).to_have_count(4)
    expect(page.locator("#content h1")).to_have_count(1)
    expect(page.locator("#related-post-container")).to_have_count(1)

    dimensions = page.locator(".related-posts").evaluate(
        "element => ({related: element.getBoundingClientRect().width, "
        "outer: element.closest('.page-layout').getBoundingClientRect().width})"
    )
    assert abs(dimensions["related"] - dimensions["outer"]) <= 1
    assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 1")
    title_size = page.locator(".related-card__title").first.evaluate("element => getComputedStyle(element).fontSize")
    assert title_size == "20px"

    pager = page.get_by_role("navigation", name="Related posts pagination")
    expect(pager.get_by_role("link", name="Previous")).to_have_count(0)
    pager.get_by_role("link", name="Next").click()
    expect(pager.get_by_role("link", name="Previous")).to_be_visible()
    expect(cards).to_have_count(4)
    pager.get_by_role("link", name="Next").click()
    expect(cards).to_have_count(1)
    expect(pager.get_by_role("link", name="Next")).to_have_count(0)
    pager.get_by_role("link", name="Previous").click()
    expect(cards).to_have_count(4)
    expect(page.locator("#content h1")).to_have_count(1)
