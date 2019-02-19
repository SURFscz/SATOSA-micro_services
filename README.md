# SATOSA-micro_services
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
#### db_attribute_store.py
Retrieves COManage attributes from shared databaes. Requires mysqlclient.

#### r_and_s_acl.py

## Abandoned
These were used earlier in development but are currently not used in SCZ-Deploy.
#### attributes_acl.py
Deny access based on absence of attributes. This is superceded by r_and_s_acl.py.
#### comanage.py
Micro service to directly query COManage API. This is superceded by db_attribute_store.py.
#### db_acl.py
Deny access if user is not present in database. Not used anymore.


## Development
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r ./test_requirements.txt


