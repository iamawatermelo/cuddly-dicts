from cuddly_dicts import kdl_source_to_dict

TO_PARSE = """
alias "High Seas"
alias "hs"
alias "highseas"
alias "high_seas"
"""

EXPECTED_RESULT = {
    "alias": ["High Seas", "hs", "highseas", "high_seas"]
}


def test_parse():
    parsed = kdl_source_to_dict(TO_PARSE)
    assert parsed == EXPECTED_RESULT, f"expected {EXPECTED_RESULT}, got {parsed}"
