# cuddly_dicts

Turn a KDL document like this:

```kdl
landtable version=1 {
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
```

Into a dict like this:

```py
{
    "landtable": {
        "version": 1,
        "ensure_landtable_version": "0.0.1",
        "provisioning": {
            "allow_runtime_provisioning": True,
            "strategy": {
                "Nest Postgres": {
                    "primary": {
                        "using": "postgres_provisioning_plugin",
                        "hostname": "hackclub.app",
                        "authentication": {
                            "userpass": {
                                "username": "sarah",
                                "password": "i_l0ve_hC!"
                            }
                        }
                    }
                }
            }
        }
    }
}
```

## Motivation

- Keep using Landtable's existing validation library (Pydantic)
- Support multiple configuration languages (TOML, JSON, YAML, whatever!)
  by making them all compile down to the same representation that can
  be validated

## Conversion rules

- KDL node -> dict result
- `landtable {}` -> `{"landtable": {}}`.
  - Repeated `landtable` nodes will create a list.
- `version 1` -> `{"version": 1}`
  - Repeated `version` nodes will create a list.
    ```
    alias "High Seas"
    alias "hs"
    ```
    Will turn into `{"alias": ["High Seas", "hs"]}`
- `landtable version=1 {}` -> `{"landtable": {"version": 1}}`
- `strategy "Nest Postgres" {}` -> `{"strategy": {"Nest Postgres": {}}}`
  - Repeated `strategy` nodes will add another entry to the dict.

cuddly_dicts (as of v3) supports value converters, so you can do things like this:

- `definitely_encrypted_ssn (base64)"QUFBLUdHLVNTU1M="`

## License

MIT or WTFPL, depending on how much of a prude you are