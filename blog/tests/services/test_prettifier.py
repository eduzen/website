from blog.services.parsers import json_to_pretty_html


def test_json_to_pretty_html():
    data = {"key": "coooool"}
    output = json_to_pretty_html(data)
    # This is a very basic check. You might want to verify specific parts of the output.
    assert "<style>" in output
    assert "coooool" in output


def test_no_json_to_pretty_html():
    data = {}
    output = json_to_pretty_html(data)
    # This is a very basic check. You might want to verify specific parts of the output.
    assert "No data" == output
