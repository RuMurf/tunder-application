from os import makedirs

directories = [
    "edata/client_hashes",
    "edata/db_hashes"
    "edata/statistics"
]

for dir in directories:
    makedirs(dir, exist_ok=True)
