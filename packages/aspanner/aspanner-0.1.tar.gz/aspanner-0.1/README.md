# aspanner
Asyncio Google Cloud Spanner Client, wrapped google-cloud-spanner to support aio calls, provide easy-to-use methods.
This project exists because Spanner have no easy-to-use asyncio interface.


References:

https://github.com/googleapis/python-spanner
https://googleapis.dev/python/spanner/latest/index.html
https://cloud.google.com/spanner/docs/samples


## Quick Start

Get the credentials JSON file from Google Cloud - IAM - Service Account - KEYS,
or run directly from the permission granted VM.

``` bash
pip install aspanner

# if use credentials file
export GOOGLE_APPLICATION_CREDENTIALS="/home/user/Working/project-server-324812-880880d2766e.json"

python3 test.py
```
