from cuddly_dicts import kdl_source_to_dict

TO_PARSE = """
landtable {
    // Configuration version
    version 1
    
    // Minimum compatible Landtable version
    ensure_landtable_version "0.0.1"
    
    provisioning {
        // Whether to allow runtime provisioning
        // (whether you can add/remove fields via the API or the web)
        allow_runtime_provisioning true
        
        // A provisioning strategy defines how a new database can be
        // created.
        strategy "Nest Postgres" {
            primary {
                using "postgres_provisioning_plugin"
                hostname "hackclub.app"
                
                authentication "userpass" {
                    username "sarah"
                    password "i_l0ve_hC!"
                }
                
                // or:
                
                authentication "vault-pg" {
                    path "database/creds/landtable"
                }
            }
        }
    }
}
"""

EXPECTED_RESULT = {
    "landtable": {
        "version": 1.0,
        "ensure_landtable_version": "0.0.1",
        "provisioning": {
            "allow_runtime_provisioning": True,
            "strategy": {
                "Nest Postgres": {
                    "primary": {
                        "using": "postgres_provisioning_plugin",
                        "hostname": "hackclub.app",
                        "authentication": {
                            "userpass": {"username": "sarah", "password": "i_l0ve_hC!"},
                            "vault-pg": {"path": "database/creds/landtable"},
                        },
                    }
                }
            },
        },
    }
}


def test_parse():
    parsed = kdl_source_to_dict(TO_PARSE)
    assert parsed == EXPECTED_RESULT, f"expected {EXPECTED_RESULT}, got {parsed}"
