from cuddly_dicts import kdl_source_to_dict

TO_PARSE = """
connector 5 {}

connector "rc-connector-dummy" {
    polling_interval 1
}

connector "my-other-connector" {}
"""

EXPECTED_RESULT = {
    "connector": {
        "rc-connector-dummy": {
            "polling_interval": 1
        },
        5: {},
        "my-other-connector": {}
    }
}


def test_parse():
    parsed = kdl_source_to_dict(TO_PARSE)
    assert parsed == EXPECTED_RESULT, f"expected {EXPECTED_RESULT}, got {parsed}"
