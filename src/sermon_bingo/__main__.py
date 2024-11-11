"""
The main entrypoint for the program.
"""

from argparse import ArgumentParser
from collections import Counter
from collections import defaultdict
import random

import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# plotting the data
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


CUSTOM_WORDS = set(
    [
        "",
        "v",
        "was",
        "us",
        "this",
        "said",
    ]
)

STOPWORDS = set(stopwords.words("english")) | CUSTOM_WORDS


def _download_sermon(url: str) -> str:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/130.0.0.0 Safari/537.36"
        )
    }
    response = requests.request("GET", url, headers=headers, timeout=30)
    return response.text


def _dedupe_words_with_same_stems(words: list[str]) -> dict[str, int]:
    stemmer = PorterStemmer()
    stem_dict = defaultdict(list)

    words = [word for word in words if word.lower() not in STOPWORDS]

    # Group words by their stems
    for word in words:
        stem = stemmer.stem(word)
        stem_dict[stem].append(word)

    output = Counter()
    for _, similar_words in stem_dict.items():
        c = Counter(similar_words)
        output[c.most_common(1)[0][0]] = len(similar_words)

    return output


def _arrange_into_sublists(lst, n):
    """Arranges a list into sublists of size n."""
    return [lst[i : i + n] for i in range(0, len(lst), n)]


def _replace_common_words_with_blanks(words, limit=3):
    if not limit:
        return words

    counter = Counter()
    word_frequencies = {}
    with open("data/count_1w.txt", mode="r", encoding="utf-8") as in_file:
        for line in in_file:
            word, count = line.split()
            word_frequencies[word] = int(count)

    counter = Counter({word: word_frequencies.get(word, 0) for word in words})

    n_common = [word for word, _ in counter.most_common(limit)]

    output = [word if word not in n_common else "" for word in words]

    return output


def _parse_words(text: str, limit: int) -> list[list[str]]:
    soup = BeautifulSoup(text, "html.parser")

    words = "\n".join(x.get_text() for x in soup.find_all("p")).split()
    words = ["".join(char for char in word if char.isalpha()) for word in words]

    counter = _dedupe_words_with_same_stems(words)

    common_sermon_words = [word for word, _ in counter.most_common(25)]
    random.shuffle(common_sermon_words)
    common_sermon_words = _replace_common_words_with_blanks(common_sermon_words, limit)
    grouped_words = _arrange_into_sublists(common_sermon_words, 5)

    return grouped_words


def _save_to_pdf(data):
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.axis("off")
    # Create the table
    the_table = ax.table(cellText=data, loc="center", cellLoc="center")

    # Set row and column sizes to fill the figure area
    n_rows = len(data)
    n_cols = len(data[0])

    # Increase cell height and width to fill the page more
    for i in range(n_rows):
        for j in range(n_cols):
            cell = the_table[i, j]
            cell.set_height(1.0 / n_rows)  # Adjust height proportionally
            cell.set_width(1.0 / n_cols)  # Adjust width proportionally

    # Save the table to a PDF file
    pp = PdfPages("data/example_output.pdf")
    pp.savefig(fig, bbox_inches="tight")  # Use bbox_inches to remove extra white space
    pp.close()


def _parse_args():
    argument_parser = ArgumentParser()
    argument_parser.add_argument("url")
    argument_parser.add_argument("--empty-boxes", type=int, default=3)
    args = argument_parser.parse_args()

    return args


def _main():
    args = _parse_args()
    text = _download_sermon(args.url)
    grouped_words = _parse_words(text, args.empty_boxes)
    _save_to_pdf(grouped_words)


if __name__ == "__main__":
    _main()
