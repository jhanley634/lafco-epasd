
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
Wrote 3664 rows to /tmp/2024-05-21_qry_EPASD_APNs_Landowner_Protests_with_phone_email.csv
```
The resulting CSV has a "phone" and an "email" column tacked on.

We began with 4273 landowner protest rows,
and reduced that to 3664 rows by discarding duplicates and rows with missing address.
That gives us 3251 unique owners, and also makes APNs unique.

The other CSV sometimes lists several voters residing at the same street address.
Each voter optionally gives a phone number,
and optionally gives an email address.
We take the first phone and first email that appears for each address.
If both are available, they won't necessarily correspond to the same voter.

In the end we wind up with 2175 unique phone numbers
and 1933 unique emails.
Focusing on addresses with a `mail_city` of MENLO PARK,
typically owner-occupied,
we see 176 unique phone numbers and 169 unique emails.
