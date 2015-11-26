# ga2csv
python cli to query into google analytics metrics/dimensions and generate a csv with results


# install

```
git clone git@github.com:devton/ga2csv.git
cd ga2csv
pip install -r requirements.txt
```

# how to use

getting total of sessions and pageviews from today

```
$ python ga2csv.py export --key-location=client_secret.p12 \
    --acc-email=account-X@appname.iam.googleserEXAMPLE \
    --profiles-id=ga:XXXXX \
    --metrics=ga:sessions,ga:pageviews 
```

getting total of session and pageviews using dimensions to get request page path

```
$ python ga2csv.py export --key-location=client_secret.p12 \
    --acc-email=account-X@appname.iam.googleserEXAMPLE \
    --profiles-id=ga:XXXXX \
    --metrics=ga:sessions,ga:pageviews \
    --dimensions=ga:pagePath
```

filtering by /hello request path

```
$ python ga2csv.py export --key-location=client_secret.p12 \
    --acc-email=account-X@appname.iam.googleserEXAMPLE \
    --profiles-id=ga:XXXXX \
    --metrics=ga:sessions,ga:pageviews \
    --filters=ga:pagePath==/hello
```
#### all avaiable options:

```--key-location``` api p12 server to server communication keys

```--acc-email``` api account email to server to server communication

```--profiles-id``` profiles id to extract, ex --profiles-id=ga:XXXX,ga:XXXX

```--metrics``` metrics to collect ex. --metrics=ga:sessions,ga:pageviews,ga:bounces

```--dimensions``` dimensions to collect ex. --dimensions=ga:userType,ga:pagePath,ga:city,ga:country

```--filters``` filters to filter collected data ex. --filters=ga:pagePath==/hello

```--start-date``` start date filter format YYYY-MM-DD

```--end-date``` start date filter format YYYY-MM-DD

```--max-results``` max results per page, default 10k

```--sort``` sorting results ex. --sort=-ga:dateHour (- for descending)

```--o``` or ```--output-file``` output csv file path default is current path output.csv
