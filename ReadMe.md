
This repo supports data analyses related to LAFCo's proposed EPASD action.

Download some PyPI packages to begin:
```bash
make install
```

Activate the virtual environment, and JOIN a pair of relations on street address:
```bash
source ~/.venv/lafco-epasd/bin/activate
voter/join_emails.py
```
which produces this output:
```bash
Wrote 8504 rows to /tmp/2024-05-21_qry_EPASD_APNs_Landowner_Protests_with_phone_email.csv
```
The resulting CSV has a "phone" and an "email" column tacked on.
