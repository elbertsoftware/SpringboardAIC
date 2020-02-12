# How to run the program:
# Start Luigi Daemon: luigid --background --port 8082 --logdir ./log
# Execute Task: python hello_world_ky.py HelloWorldTask --workers=2 --id='2019-09-02'

import luigi
from pathlib import Path
from time import sleep


class Cassandra(luigi.Config):
    host = luigi.Parameter()


class RawDataStoreTask(luigi.Target):
    def output(self):
        return luigi.contrib.mongodb.MongoTarget(host=f'{Cassandra().host}')


class DirectoryTask(luigi.Task):
    path = luigi.Parameter()

    def run(self):
        directory = Path(self.path)
        directory.mkdir(parents=True)

    def output(self):
        return luigi.LocalTarget(self.path)


class WordTask(luigi.Task):
    path = luigi.Parameter()
    word = luigi.Parameter()

    def requires(self):
        return [
            DirectoryTask(
                path=str(Path(self.path).parent)
            )
        ]

    def run(self):
        sleep(30)
        Path(self.path).write_text(self.word)

    def output(self):
        return luigi.LocalTarget(self.path)


class HelloWorldTask(luigi.Task):
    id = luigi.Parameter(default='test')

    def requires(self):
        return [
            WordTask(
                path=f'result/{self.id}/hello.txt',
                word='Hello'
            ),
            WordTask(
                path=f'result/{self.id}/world.txt',
                word='World!'
            )
        ]

    def run(self):
        sleep(30)
        hello = Path(self.input()[0].path).read_text()
        world = Path(self.input()[1].path).read_text()
        Path(self.output().path).write_text(f'{hello} {world}')

    def output(self):
        return luigi.LocalTarget(f'result/{self.id}/hello_world.txt')


if __name__ == '__main__':
    luigi.run()
