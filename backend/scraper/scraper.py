import requests
from bs4 import BeautifulSoup
from rdflib import Graph, Literal, URIRef, Namespace
from urllib.parse import urlparse
from urllib.parse import quote
def scrape_reddit(url,subreddit):
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        g = Graph()

        ns = Namespace("http://wade-project.org/news#")

        for post in soup.find_all('shreddit-post'):
            title = post.get('post-title')
            link = post.get('content-href')
            subject = URIRef(ns + f"post/{quote(title).replace(' ', '_')}")
            g.add((subject, ns.title, Literal(title)))
            g.add((subject, ns.link, URIRef(link)))
            g.add((subject, ns.origin, Literal("reddit")))
            g.add((subject, ns.topic, Literal("subreddit")))

        return g
    else:
        print(f"Failed to retrieve data from {url}. Status code: {response.status_code}")
        return None

def scrape_mozilla(url):
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        g = Graph()

        ns = Namespace("http://wade-project.org/news#")

        for tile in soup.select('.article-tile, .news-item'):
            title_element = tile.select_one('.tile-title a')
            link_element = title_element['href'] if title_element else None

            if title_element and link_element:
                title = title_element.text.strip()
                link = "https://developer.mozilla.org"+link_element.strip()

                subject = URIRef(ns + f"post/{quote(title).replace(' ', '_')}")
                g.add((subject, ns.title, Literal(title)))
                g.add((subject, ns.link, URIRef(link)))
                g.add((subject, ns.origin, Literal("mozilla")))
                g.add((subject, ns.topic, Literal("tutorials")))

        return g
    else:
        print(f"Failed to retrieve data from {url}. Status code: {response.status_code}")
        return None

def scrape_github_topics(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        g = Graph()

        ns = Namespace("http://wade-project.org/news#")

        for repo in soup.select('.f3 a'):
            title = repo.text.strip()
            link = 'https://github.com' + repo['href'].strip()

            subject = URIRef(ns + f"post/{quote(title).replace(' ', '_')}")
            g.add((subject, ns.title, Literal(title)))
            g.add((subject, ns.link, URIRef(link)))
            g.add((subject, ns.origin, Literal("github")))
            g.add((subject, ns.topic, Literal("web development")))

        return g

    else:
        print(f"Failed to retrieve data from {url}. Status code: {response.status_code}")
        return None

def scrape_and_convert_to_rdf(urls, output_file='combined_rdf_data.rdf'):
    combined_graph = Graph()

    for url in urls:
        if 'reddit.com' in url:
            parsed_url = urlparse(url)
            subreddit = parsed_url.path.split('/')[2]
            rdf_graph = scrape_reddit(url, subreddit)
        if 'mozilla.org' in url:
            rdf_graph = scrape_mozilla(url)
        if 'github.com' in url:
            rdf_graph = scrape_github_topics(url)
        if rdf_graph:
            combined_graph += rdf_graph
            print(f"Web scraping and RDF conversion completed for {url}")

    combined_graph.serialize(destination=output_file, format='turtle')

    print(f"Combined RDF data saved to {output_file}")

urls_to_scrape = [
    'https://www.reddit.com/r/technology',
    'https://www.reddit.com/r/programming',
    'https://www.reddit.com/r/javascript',
    'https://developer.mozilla.org/en-US/',
    'https://github.com/topics/web-tutorial'
]

scrape_and_convert_to_rdf(urls_to_scrape)

