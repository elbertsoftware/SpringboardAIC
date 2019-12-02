import luigi
import os


class PrintWordTask(luigi.Task):
    path = luigi.Parameter()
    word = luigi.Parameter()

    def run(self):
        with open(self.path, 'w') as out_file:
            out_file.write(self.word)
            out_file.close()

    def output(self):
        return luigi.LocalTarget(self.path)

    def requires(self):
        return [
            MakeDirectory(path=os.path.dirname(self.path)),
        ]


class HelloWorldTask(luigi.Task):
    id = luigi.Parameter(default='test')

    def run(self):
        with open(self.input()[0].path, 'r') as hello_file:
            hello = hello_file.read()
        with open(self.input()[1].path, 'r') as world_file:
            world = world_file.read()
        with open(self.output().path, 'w') as output_file:
            content = '{} {}!'.format(hello, world)
            output_file.write(content)
            output_file.close()

    def requires(self):
        return [
            PrintWordTask(
                path='results/{}/hello.txt'.format(self.id),
                word='Hello',
            ),
            PrintWordTask(
                path='results/{}/world.txt'.format(self.id),
                word='World',
            ),
        ]

    def output(self):
        path = 'results/{}/hello_world.txt'.format(self.id)
        return luigi.LocalTarget(path)


class MakeDirectory(luigi.Task):
    path = luigi.Parameter()

    def output(self):
        return luigi.LocalTarget(self.path)

    def run(self):
        os.makedirs(self.path)


if __name__ == '__main__':
   luigi.run()