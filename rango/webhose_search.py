import json
import urllib
import urllib2
import os


def read_webhose_key():
    """
     Reads the WebHose API key from a file search.key. Returns
     either None or the key as a string. Put search.key in .gitignore.
    """
    webhose_api_key = None
    # script_dir = os.path.dirname(__file__)  # absolute path to this
    # print (os.path.dirname(__file__))
    search_file = "search.key"
    if not os.path.isfile(search_file):
        search_file = "../" + search_file
    try:
        with open(search_file, "r") as f:
            webhose_api_key = f.readline().strip()
    except:
        raise IOError("search.key not found!")

    return webhose_api_key


def run_query(search_terms, size=10):
    """
    :param search_terms: query
    :param size: number of elements to display
    :return: list of results, each with title, link and summary
    """

    # get the key
    webhose_api_key = read_webhose_key()

    if not webhose_api_key:
        raise KeyError("key not found")

    # the base url for webhose API
    root_url = "http://webhose.io/search"

    # format the query string - escape special characters
    query_string = urllib.quote(search_terms)

    # construct the complete URL
    search_url = ("{root_url}?token={key}&format=json&q={query}&sort=relevancy&size={size}").format(root_url=root_url,
                                                                                                    key=webhose_api_key,
                                                                                                    query=query_string,
                                                                                                    size=size)
    # contain the search results
    results = []

    try:
        response = urllib2.urlopen(search_url).read()  # string response
        json_response = json.loads(response)  # convert it to python dict
        for post in json_response['posts']:
            results.append({'title': post['title'], 'link': post['url'], 'summary': post['text'][:200]})
    except:
        print ("Error when querying the WebHose API")

    # return the results to the calling function
    return results


def display_result():
    pass


if __name__ == '__main__':
    # get the query from user
    query_input = raw_input("Enter a query:\n")
    # get the results
    searched_results = run_query(query_input)
    for result in searched_results:
        print (result["title"] + "\n")
        print (result["summary"])
    print (os.path.dirname(__file__))
