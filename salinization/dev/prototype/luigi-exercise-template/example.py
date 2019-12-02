# Link to the git repo: https://github.com/iamaaronknight/luigi-exercise-template
# Link to the video tutorial: https://www.youtube.com/watch?v=jpkZGXrhZJ8&feature=player_embedded

# How to run the program:
# python example.py WriteUserUpdatesToSQL --id=1

import csv
import os

import luigi
import luigi.contrib.postgres
import luigi.contrib.s3


# Configuration classes
class postgresTable(luigi.Config):
    host = luigi.Parameter()
    database = luigi.Parameter()
    user = luigi.Parameter()
    password = luigi.Parameter()


class s3Bucket(luigi.Config):
    key = luigi.Parameter()
    secret = luigi.Parameter()


# Tasks
class GetUserUpdateFromS3(luigi.Task):
    id = luigi.Parameter()

    extension = '.csv'
    s3_directory = 's3://pycon-2017-luigi-presentation-data/UserUpdates/'
    local_directory = './downloads/UserUpdates/'

    def get_local_file_name(self, s3_file_name):
        return s3_file_name.replace(self.s3_directory, f'{self.local_directory}{self.id}_')

    @property
    def client(self):
        key = s3Bucket().key
        secret = s3Bucket().secret

        return luigi.contrib.s3.S3Client(aws_access_key_id=key, aws_secret_access_key=secret)

    @property
    def s3_files(self):
        return [s3_file for s3_file in self.client.listdir(self.s3_directory) if s3_file.endsWith(self.extension)]

    @property
    def local_files(self):
        return [self.get_local_file_name(file) for file in self.s3_files]

    def run(self):
        for s3_file in self.s3_files:
            self.client.get(s3_file, self.get_local_file_name(s3_file))

    def output(self):
        return [luigi.LocalTarget(file) for file in self.local_files]


class ConcatenateUserUpdates(luigi.Task):
    id = luigi.Parameter()

    def requires(self):
        return [GetUserUpdateFromS3(id=self.id)]

    def run(self):
        os.system(f'cat ./downloads/UserUpdates/{self.id}_*.csv >> generated_files/{self.id}_user_updates.csv')

    def output(self):
        return luigi.LocalTarget(f'generated_files/{self.id}_user_updates.csv')


class WriteUserUpdatesToSQL(luigi.contrib.postgres.CopyToTable):
    id = luigi.Parameter()

    host = postgresTable().host
    database = postgresTable().database
    user = postgresTable().user
    password = postgresTable().password

    table = 'user_updates'
    columns = [
        ('ts', 'timestamp'),
        ('user_id', 'int'),
        ('email', 'text'),
        ('name', 'text'),
        ('environment', 'text')
    ]

    def rows(self):
        with open(self.source_csv, 'r') as csv_file:
            reader = csv.reader(csv_file)
            return [row for row in reader if len(row) == len(self.columns)]

    @property
    def update_id(self):
        return f'{self.table}_{self.id}'

    @property
    def source_csv(self):
        return f'generated_files/{self.id}_user_updates.csv'

    def requires(self):
        return [ConcatenateUserUpdates(id=self.id)]


if __name__ == '__main__':
    luigi.run()
