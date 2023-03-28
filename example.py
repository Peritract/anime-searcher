#!/usr/bin/env python
"""Returns the name and rating of up to n=5 anime for a given search term."""

from argparse import ArgumentParser, Namespace

import requests as req

BASE_URL = "https://api.jikan.moe/v4/anime?"


def collect_arguments() -> Namespace:
    """Returns parsed arguments from the command line."""

    desc = "Returns the name and rating of up to n=5 anime for a given search term"
    arg_parser = ArgumentParser(description=desc)
    arg_parser.add_argument("--n", default="5",
                            help="the number of results to return")
    arg_parser.add_argument("--nsfw", action="store_true",
                            help="include NSFW shows")
    arg_parser.add_argument("query",
                            help="the query to search for")

    return arg_parser.parse_args()


def create_url(args: Namespace) -> str:
    """Returns a formatted URL based on CLI arguments."""

    url = BASE_URL + f"&limit={args.n}&q={args.query}" + ("&sfw" if not args.nsfw else "")
    return url


def get_anime_data(url: str) -> dict:
    """Returns valid anime data from the Jikan API as a dict."""

    res = req.get(url, timeout=5000)
    print(res.json()["pagination"]["items"]["total"])
    shows = res.json()["data"]
    return [s for s in shows if s["rating"] and s["score"]]


def display_anime_data(anime_data: dict):
    """Displays key details about an anime from a dict."""
    title = anime_data['titles'][0]['title']
    score = anime_data['score']
    scored_by = anime_data['scored_by']
    rating = anime_data["rating"].split(" - ")[0]

    print(f"{title} ({rating}) ~ {score}/10 ({scored_by})")


if __name__ == "__main__":
    try:
        arguments = collect_arguments()
        search_url = create_url(arguments)
        print(search_url)
        data = get_anime_data(search_url)
        for show in data:
            display_anime_data(show)
    except IndexError as err:
        print("No matching anime found.")
    except TypeError as err:
        print("No matching anime found.")
