from mrjob.job import MRJob
from mrjob.step import MRStep


class Salary(MRJob):
    def steps(self):
        return [
            MRStep(mapper=self.mapper, reducer=self.count_reducer),
        ]

    def mapper(self, _, line):
        row = line.replace(" ", "").split(",")

        idemp = None
        sector = None
        salary = None
        year = None

        try:
            idemp = int(row[0])
            sector = int(row[1])
            salary = float(row[2])
            year = int(row[3])
        except:
            pass
        else:
            yield (f"sector-{sector}-avg: ", salary)
            yield (f"employee-{idemp}-avg: ", salary)
            yield (f"employee-count-{idemp}", sector)

    def count_reducer(self, key, values):
        if key.startswith("employee-count-"):
            count = 0
            previous_sectors = set()

            for v in values:
                if v not in previous_sectors:
                    previous_sectors.add(v)
                    count += 1

            yield (key, count)
        else:
            salary = 0
            n = 0

            for s in values:
                salary += s
                n += 1

            if n > 0:
                yield (key, salary / n)
            else:
                yield (key, salary)


if __name__ == "__main__":
    Salary.run()
