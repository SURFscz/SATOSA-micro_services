# SATOSA-micro_services
[![Build Status](https://travis-ci.com/SURFscz/SATOSA-micro_services.svg)](https://travis-ci.com/SURFscz/SATOSA-micro_services)
[![codecov.io](https://codecov.io/github/SURFscz/SATOSA-micro_services/coverage.svg)](https://codecov.io/github/SURFscz/SATOSA-micro_services)
Separate micro_services repository for SATOSA

## Active
#### attribute_check.py
Check if attributes have changed. Requires mysqlclient.
#### attribute_filter.py
Remove attributes from internal representation based on source IdP, Destination SP, attribute name and content.
#### custom_alias.py
Add simple static html endpoints. Handy for metadata serving and error pages.
#### custom_uid.py
Creates a custom unique identifier, used for COManage provisioning.
#### sbs_attribute_store.py
Retrieves COManage attributes from SBS. Requires requests.

#### r_and_s_acl.py

## Development
```
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r ./test_requirements.txt
```
## Testing
```
python -m pytest --cov=src --cov-report html:htmlcov src/test
open htmlcov/index.html 
```

