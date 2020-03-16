Github repository to get info from the covid-19 in Spain and Germany, comparing the active cases with the ones existing in Italy.

In order to run the script in the background, use the following command:

```
python -u  covid.py > log  2>&1 &
```

You have to consider 3 environment variables in order to send the email with the image:

- GMAIL_PASS (password)
- GMAIL_USER (sender)
- GMAIL_DEST (destiny)
