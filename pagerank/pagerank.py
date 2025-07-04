import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    prob_dist=dict()
    for link in corpus:
        if link in corpus[page]:
            prob_dist[link]=damping_factor/len(corpus[page])
        else:
            prob_dist[link]=(1-damping_factor)/len(corpus)
    return prob_dist
    


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_rank = dict.fromkeys(corpus, 0)
    pages = list(corpus.keys())

    # Start with a random page
    current_page = random.choice(pages)

    for _ in range(n):
        page_rank[current_page] += 1

        # Get transition model for the current page
        probabilities = transition_model(corpus, current_page, damping_factor)

        # Pick the next page based on weighted probabilities
        current_page = random.choices(
            population=list(probabilities.keys()),
            weights=list(probabilities.values()),
            k=1
        )[0]

    # Normalize to get probabilities
    for page in page_rank:
        page_rank[page] /= n

    return page_rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    N = len(corpus)
    page_rank = dict.fromkeys(corpus, 1 / N)
    convergence_threshold = 0.001

    while True:
        new_ranks = dict()
        for page in corpus:
            total = 0
            for possible_page in corpus:
                links = corpus[possible_page]
                if page in links:
                    total += page_rank[possible_page] / len(links)
                if not links:
                    # Handle dangling pages (no links)
                    total += page_rank[possible_page] / N
            new_ranks[page] = ((1 - damping_factor) / N) + (damping_factor * total)

        # Check for convergence
        diff = max(abs(new_ranks[page] - page_rank[page]) for page in corpus)
        page_rank = new_ranks
        if diff < convergence_threshold:
            break

    return page_rank
    


if __name__ == "__main__":
    main()
