#!/usr/bin/python3
"""
   recursive function that queries the Reddit API
"""

import requests


def recurse(subreddit, hot_list=[], after=None):
    # Set up the Reddit API URL
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"

    # Set a custom User-Agent to avoid Too Many Requests errors
    headers = {'User-Agent': 'my_bot/1.0'}

    # Set parameters for the API request
    params = {'limit': 100, 'after': after}

    # Make the API request
    response = requests.get(url, headers=headers, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        posts = data['data']['children']

        # Check if there are any posts
        if len(posts) == 0:
            return hot_list
        else:
            # Extract titles from the posts and extend the hot_list
            hot_list.extend([post['data']['title'] for post in posts])

            # Recursively call the function with the 'after'
            next_page = data['data']['after']
            if next_page is not None:
                return recurse(subreddit, hot_list, after=next_page)
            else:
                return hot_list
    else:
        return None  # Invalid subreddit or other error


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Please pass an argument for the subreddit to search.")
    else:
        subreddit = sys.argv[1]
        result = recurse(subreddit)
        if result is not None:
            print(len(result))
        else:
            print("None")
