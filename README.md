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

## Conversion rules

```
version 1
```

becomes

```
{
    "version": 1
}
```

---

```
version 1
version 2
```

becomes

```
{
    "version": [1, 2]
}
```

---

```
connector "foo"
connector "bar" {
  port /dev/ttyUSB0
}
```

becomes

```
{
    "connector": {
        "foo": {},
        "bar": {
            "port": "/dev/ttyUSB0"
        }
    }
}
```

> [!INFO]
> New in 3.0.2.

---

```
connector "foo" port="/dev/ttyUSB0"
```

becomes

```
{
    "connector": {
        "foo": {
            "port": "/dev/ttyUSB0"
        }
    }
}
```

---

```
connector "foo" port="/dev/ttyUSB0" {
    baud_rate 24000
}
```

becomes

```
{
    "connector": {
        "foo": {
            "port": "/dev/ttyUSB0",
            "baud_rate": 24000
        }
    }
}
```

---

cuddly_dicts (as of v3) supports value converters, so you can do things like this:

```
definitely_encrypted_ssn (base64)"QUFBLUdHLVNTU1M="
```

## License

MIT or WTFPL, depending on how much of a prude you are

## Motivation

- Keep using Landtable's existing validation library (Pydantic)
- Support multiple configuration languages (TOML, JSON, YAML, whatever!)
  by making them all compile down to the same representation that can
  be validated

cuddly_dicts proved to be more useful to me in other projects, so now I
use it in most things.