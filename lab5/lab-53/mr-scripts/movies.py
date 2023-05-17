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

        user = None
        movie = None
        rating = None
        genre = None
        date = None

        try:
            user = int(row[0])
            movie = int(row[1])
            rating = int(row[2])
            genre = row[3]
            date = parse(row[4])
        except:
            pass
        else:
            yield (f"user-nummovies-score-{user}", rating)
            yield (f"movie-numusers-score-{movie}", rating)
            yield (f"minmax-daymovies", row[4])
            yield (f"extreme-score-day", (row[4], rating))
            yield (f"extreme-score-genre", (genre, rating))

    def reducer(self, key, values):
        if key.startswith("user-nummovies-score-"):
            n = 0
            acc_rating = 0

            for v in values:
                n += 1
                acc_rating += v

            yield (key, (n, acc_rating / n))
        if key.startswith("movie-numusers-score-"):
            n = 0
            acc_rating = 0

            for v in values:
                n += 1
                acc_rating += v

            yield (key, (n, acc_rating / n))
        if key.startswith("minmax-daymovies"):
            days = {}

            for v in values:
                if v in days:
                    days[v] += 1
                else:
                    days[v] = 1

            days = [(v, k) for k, v in days.items()]
            days.sort(reverse=True)

            if len(days) > 0:
                yield ("max-daymovies", days[0][1])
                yield ("min-daymovies", days[-1][1])
        if key.startswith("extreme-score-day"):
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
                yield ("worst-score-day", days[0])
                yield ("best-score-day", days[-1])
        if key.startswith("extreme-score-genre"):
            genres = {}
            for v in values:
                if v[0] in genres:
                    s = genres[v[0]]
                    genres[v[0]] = (s[0] + v[1], s[1] + 1)
                else:
                    genres[v[0]] = (v[1], 1)

            genres = [(v[0] / v[1], k) for k, v in genres.items()]
            genres.sort()

            if len(genres) > 0:
                yield ("worst-score-genre", genres[0])
                yield ("best-score-genre", genres[-1])


if __name__ == "__main__":
    Shares.run()
