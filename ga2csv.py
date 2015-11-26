# -*- coding: utf-8 -*-
import click
import httplib2
import csv

from termcolor import colored
from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials


@click.group()
def cli():
    pass


# ga2csv cli options
@cli.command()
@click.option('--profiles-id', help='profiles ID ex(ga:XXXX)')
@click.option('--start-date', default='today',
              help='start date. ex. 2014-04-01')
@click.option('--end-date', default='today',
              help='end date. ex. 2015-11-25')
@click.option('--key-location', default='key.p12',
              help='.p12 key file location')
@click.option('--acc-email', help='service account email')
@click.option('--metrics', default=None,
              help='ga metrics ex (ga:sessions,ga:bounces)')
@click.option('--dimensions', default=None,
              help='ga dimensions ex.(ga:userType, ga:pagePath)')
@click.option('--sort', default=None,
              help='ga dimensions ex (-ga:dateHour)')
@click.option('--filters', default=None,
              help='ga filters ex (ga:pagePath=="/how-it-works")')
@click.option('--max-results', default=10000,
              help='ga max results per page default 10000')
@click.option('--o', '--output-file', default='output.csv',
              help='output path to csv default is current path output.csv')
def export(profiles_id, start_date, end_date, filters, max_results,
           key_location, acc_email, metrics, dimensions, sort, output_file):
    ''' export ga metrics to csv '''

    ga_scope = ['https://www.googleapis.com/auth/analytics.readonly']
    start_index = 1

    '''
    Read key file and starts analytics connection
    '''
    with open(key_location, 'rb') as key:
        click.echo('loading key {} and connecting to GA'.format(
            colored(key_location, 'yellow', attrs=['bold'])))
        credentials = SignedJwtAssertionCredentials(
            acc_email, key.read(), scope=ga_scope)

        analytics = build('analytics', 'v3',
                          http=credentials.authorize(
                              httplib2.Http()))

    '''
    Open output path to csv and start write
    '''
    with open(output_file, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        ga = analytics.data().ga()

        data = ga.get(
            ids=profiles_id,
            start_date=start_date,
            end_date=end_date,
            metrics=metrics,
            max_results=max_results,
            filters=filters,
            dimensions=dimensions,
            sort=sort).execute()

        total_results = data['totalResults']
        click.echo('found total of {} results'.format(total_results))

        writer.writerow([h['name'] for h in data['columnHeaders']])
        writer.writerows(data['rows'])

        while True:
            try:
                current_index = start_index + max_results
                data = ga.get(
                    ids=profiles_id,
                    start_date=start_date,
                    end_date=end_date,
                    start_index=current_index,
                    metrics=metrics,
                    max_results=max_results,
                    filters=filters,
                    dimensions=dimensions,
                    sort=sort
                ).execute()

                if 'rows' in data.keys():
                    writer.writerows(data['rows'])
                else:
                    break
            except Exception as e:
                click.echo(e)

        click.echo('inserted all {} results into {}'.format(
            colored(total_results, 'green', attrs=['bold']),
            colored(output_file, 'yellow', attrs=['bold'])))


if __name__ == '__main__':
    cli()
