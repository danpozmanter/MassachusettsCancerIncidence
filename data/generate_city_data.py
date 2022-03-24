import json
import os
import config

"""Notes:
Generally one would want to model this data with strict typing,
but it's much more convenient to stick to dictionaries.
Sometimes the more convenient choice is valid, especially for a script.
"""


def load_city_average_data(cities):
    """Calculate averages by city, category, and sex.
    Load them into the cities dictionary as an additional "year range"."""

    def _update_average(city_average, year_range, category, sex):
        """Update the total observed, expected, SIR, and significance
        for each year range. For the final year range, calculate the average.
        If any one year range is not significant, mark the average
        as not significant. Only calculate the average SIR if all year ranges
        are significant.
        """
        if sex not in city_average[category]:
            city_average[category][sex] = {
                "observed": 0, "expected": 0, "sir": None,
                "significant": True
            }
        avg = city_average[category][sex]
        avg["observed"] += data[category][sex]["observed"]
        avg["expected"] += data[category][sex]["expected"]
        avg["significant"] *= data[category][sex]["significant"]
        if year_range == "11-15":
            avg["observed"] /= len(config.year_ranges)
            avg["expected"] /= len(config.year_ranges)
            if avg["significant"]:
                avg["sir"] = (
                    avg["observed"] /
                    avg["expected"]
                ) * 100

    for city in cities:
        print(f"================{city}===============")
        city_average = {}
        for year_range in config.year_ranges:
            print(f"    {year_range}")
            data = cities[city][year_range]
            for category in data:
                if category not in city_average:
                    city_average[category] = {}
                for sex in ("male", "female", "combined"):
                    _update_average(city_average, year_range, category, sex)
        cities[city]["Average"] = city_average


def load_city_data_from_json():
    """Pull in the data from the parsed city_json."""
    cities = {}
    print("Loading City Data...")
    for year_range in config.year_ranges:
        path = f"city_json/{year_range}"
        city_files = os.listdir(path)
        for city_file in city_files:
            city = os.path.splitext(city_file)[0]
            if year_range == "08-12":
                # Previously vetted, city names don't change year to year.
                # But they could - so one might want to account for that.
                cities[city] = {}
            cities[city][year_range] = {}
            with open(f"{path}/{city_file}") as f:
                data = json.loads(f.read())
                cities[city][year_range] = data
    return cities


def rank_cities(cities):
    """Rank cities across year ranges by category and sex."""

    def _rank(cities, year_range, category, sex):
        """Rank the cities by the provided year range, category, and sex.
        Use SIR as the standard. Account for null SIR values."""
        def _sort_by(city):
            sir = cities[city][year_range][category][sex]["sir"]
            if sir is None:
                return 0
            return sir
        city_names = list(cities.keys())
        city_names.sort(key=_sort_by)
        return city_names

    rankings = {}
    for city in cities:
        cities[city]["Rank"] = {}
    cat = "All Sites / Types"
    for year_range in config.processed_year_ranges:
        rankings[year_range] = {}
        for sex in ("male", "female", "combined"):
            rankings[year_range][sex] = {}
            rankings[year_range][sex] = _rank(
                cities,
                year_range=year_range,
                category=cat,
                sex=sex)
            for city in cities:
                if year_range not in cities[city]["Rank"]:
                    cities[city]["Rank"][year_range] = {cat: {
                        "male": {},
                        "female": {},
                        "combined": {}
                    }}
                rank = rankings[year_range][sex].index(city) + 1
                cities[city]["Rank"][year_range][cat][sex] = rank
    return rankings


def create_city_names_json(city_names):
    with open(f"../site/city_list.js", "w") as f:
        city_names = sorted(city_names)
        f.write("const cities = " + json.dumps(city_names))


def create_ranked_city_json(city, city_data, rankings):
    print(f"Creating ranked city json for {city}...")
    with open(f"../site/data/{city}.json", "w") as f:
        f.write(json.dumps(city_data))


# Load the parsed city json created by "process_raw".
cities = load_city_data_from_json()

# Export city names to json for the static site.
create_city_names_json(cities.keys())

# Calculate averages by city, category, and sex.
load_city_average_data(cities)

# Calculate the rankings by city, category, and sex.
rankings = rank_cities(cities)

# Write out the full data city by city for use by the static site.
for city in cities:
    create_ranked_city_json(city, cities[city], rankings)
