import json
import os
from functools import lru_cache
from pathlib import Path

import pandas as pd
from tqdm import tqdm

DATA_PATH = os.path.join(Path(__file__).parent.parent.resolve(), "data")


country_mapping = {
    "uk": "united kingdom",
    "england": "united kingdom",
    "scotland": "united kingdom",
    "us": "united states",
    "usa": "united states",
    "the netherlands": "netherlands",
}

hard_coded = {
    "NYC": "New York, New York",
    "New York City": "New York, New York",
    "Philly": "Philadelphia, PA",
    "LA": "Los Angeles, CA",
}


def load_friends_data():
    # Load some friends JSON data
    base = os.path.join(DATA_PATH, "twitter_friends")
    print(base)
    friends = []
    for filename in os.listdir(base):
        fp = os.path.join(base, filename)
        with open(fp) as f:
            some_friends = json.load(f)
        friends += some_friends
    # extract relevant info
    data = [(f["screen_name"], f["location"]) for f in friends]
    return data


@lru_cache
def load_city_data():
    df_cities = pd.read_csv(os.path.join(DATA_PATH, "geocode", "worldcities.csv"))
    df_cities = df_cities.sort_values(by="population", ascending=False)
    for key in ["city", "city_ascii", "country", "iso2", "iso3", "admin_name"]:
        df_cities[key] = df_cities[key].str.lower()
    return df_cities


@lru_cache
def load_state_data():
    states_df = pd.read_csv(os.path.join(DATA_PATH, "geocode", "states.csv"))
    abbrvs = states_df["abbreviation"]
    states = states_df["state"]
    state_lookup = {
        abbrvs.lower(): states.lower() for abbrvs, states in zip(abbrvs, states)
    }
    return state_lookup


@lru_cache(maxsize=10000)
def geocode_simplemaps(location):
    df_cities = load_city_data()
    state_lookup = load_state_data()

    # ----- easy stuff -----
    if not location:
        return None

    # ----- pre-processing -----
    if hard_coded.get(location):
        location = hard_coded.get(location)
    location = location.split("via")[0].strip()

    # ----- main -----
    parts = [x.strip().lower() for x in location.split(",")]

    # treat first part as a city
    city = parts[0]
    city = city.replace("st ", "st. ")
    lookup_res = df_cities[df_cities["city"] == city]

    # if just one result, take it
    if len(lookup_res) == 1:
        row = lookup_res.iloc[0]
        return row.name

    # if just one part, take first result
    if len(parts) == 1 and len(lookup_res) > 0:
        row = lookup_res.iloc[0]
        return row.name

    # consider second part
    if len(parts) > 1:
        place = parts[1]

        # check if second part is a state
        state = state_lookup.get(place)
        if not state:
            state = place
        lookup_res_state = lookup_res[lookup_res["admin_name"] == state]
        if len(lookup_res_state) == 1:
            row = lookup_res_state.iloc[0]
            return row.name

        # check if second part is a country
        country = country_mapping.get(place)
        if not country:
            country = place
        lookup_res_country = lookup_res[lookup_res["country"] == country]
        if len(lookup_res_country) == 1:
            row = lookup_res_country.iloc[0]
            return row.name

    return None


def lookup_index(i):
    df_cities = load_city_data()
    try:
        row = df_cities.loc[i]
        return row["city"], row["country"]
    except KeyError:
        return None, None


def pre_process(df):
    new_df = df.copy()

    # lowercase location
    new_df["location"] = new_df["location"].str.lower()

    # ignore some confusing values
    ignore = ["earth", "planet earth", "home"]
    for item in ignore:
        new_df[new_df["location"] == item] = ""

    # remove empty
    new_df = new_df[new_df["location"] != ""]
    return new_df


def main():
    data = load_friends_data()
    data_coded = []
    for screen_name, location in tqdm(data):
        res = geocode_simplemaps(location)
        city, country = lookup_index(res)  # could return (None, None)
        data_coded.append(
            dict(screen_name=screen_name, location=location, city=city, country=country)
        )
    return pd.DataFrame(data_coded)


def test(location):
    res = geocode_simplemaps(location)
    city, country = lookup_index(res)

    print(location)
    print(res, city, country)


if __name__ == "__main__":
    test("Colorado, USA")
    # print(main())
