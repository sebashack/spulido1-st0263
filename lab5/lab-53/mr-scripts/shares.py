from mrjob.job import MRJob
from mrjob.step import MRStep
from dateutil.parser import parse


def non_decreasing(ls):
    return all(x <= y for x, y in zip(ls, ls[1:]))


class Shares(MRJob):
    def steps(self):
        return [
            MRStep(mapper=self.mapper, reducer=self.reducer),
        ]

    def mapper(self, _, line):
        row = line.replace(" ", "").split(",")

        company = None
        price = None
        date = None

        try:
            company = row[0]
            price = float(row[1])
            date = parse(row[2])
        except:
            pass
        else:
            yield (f"minmax-day-{company}", (row[2], price))
            yield (f"stable-{company}", (row[2], price))
            yield (f"black-day", (row[2], price))

    def reducer(self, key, values):
        if key.startswith("minmax-day-"):
            min_price = ("", float("inf"))
            max_price = ("", float("-inf"))

            for v in values:
                if v[1] > max_price[1]:
                    max_price = v

                if v[1] < min_price[1]:
                    min_price = v

            yield (key, (min_price[0], max_price[0]))
        elif key.startswith("stable-"):
            prices_with_dates = []
            for v in values:
                date = parse(v[0])
                prices_with_dates.append((date, v[1]))

            prices_with_dates.sort()
            prices = list(map(lambda t: t[1], prices_with_dates))

            if non_decreasing(prices):
                yield (key, prices)
        elif key.startswith("black-day"):
            days = {}
            for v in values:
                if v[0] in days:
                    s = days[v[0]]
                    days[v[0]] = (s[0] + v[1], s[1] + 1)
                else:
                    days[v[0]] = (v[1], 1)

            days = [(v[0] / v[1], k) for k, v in days.items()]
            days.sort()

            if len(days) > 0:
                yield (key, days[0])


if __name__ == "__main__":
    Shares.run()
