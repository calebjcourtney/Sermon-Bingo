from unittest.mock import MagicMock
from unittest.mock import patch
import pytest

from src.sermon_bingo.__main__ import _dedupe_words_with_same_stems
from src.sermon_bingo.__main__ import _arrange_into_sublists
from src.sermon_bingo.__main__ import _replace_common_words_with_blanks
from src.sermon_bingo.__main__ import _parse_words
from src.sermon_bingo.__main__ import main


@pytest.fixture
def response():
    return """
    <p>To be, or not to be, that is the question:</p>
    <p>Whether 'tis nobler in the mind to suffer</p>
    <p>The slings and arrows of outrageous fortune,</p>
    <p>Or to take arms against a sea of troubles</p>
    <p>And by opposing end them. To die—to sleep,</p>
    <p>No more; and by a sleep to say we end</p>
    <p>The heart-ache and the thousand natural shocks</p>
    <p>That flesh is heir to: 'tis a consummation</p>
    <p>Devoutly to be wish'd. To die, to sleep;</p>
    <p>To sleep, perchance to dream—ay, there's the rub:</p>
    <p>For in that sleep of death what dreams may come,</p>
    <p>When we have shuffled off this mortal coil,</p>
    <p>Must give us pause—there's the respect</p>
    <p>That makes calamity of so long life.</p>
    <p>For who would bear the whips and scorns of time,</p>
    <p>Th'oppressor's wrong, the proud man's contumely,</p>
    <p>The pangs of dispriz'd love, the law's delay,</p>
    <p>The insolence of office, and the spurns</p>
    <p>That patient merit of th'unworthy takes,</p>
    <p>When he himself might his quietus make</p>
    <p>With a bare bodkin? Who would fardels bear,</p>
    <p>To grunt and sweat under a weary life,</p>
    <p>But that the dread of something after death,</p>
    <p>The undiscovere'd country, from whose bourn</p>
    <p>No traveller returns, puzzles the will,</p>
    <p>And makes us rather bear those ills we have</p>
    <p>Than fly to others that we know not of?</p>
    <p>Thus conscience doth make cowards of us all,</p>
    <p>And thus the native hue of resolution</p>
    <p>Is sicklied o'er with the pale cast of thought,</p>
    <p>And enterprises of great pith and moment</p>
    <p>With this regard their currents turn awry</p>
    <p>And lose the name of action.</p>
    """


@pytest.mark.parametrize(
    "words, expected",
    [
        (["hello", "world", "hello", "world"], {"hello": 2, "world": 2}),
        (["hello", "world", "world", "world"], {"hello": 1, "world": 3}),
    ],
)
def test_dedupe_words_with_same_stems(words, expected):
    assert _dedupe_words_with_same_stems(words) == expected


@pytest.mark.parametrize(
    "words, count, expected",
    [
        (
            ["hello", "world", "hello", "world"],
            2,
            [["hello", "world"], ["hello", "world"]],
        ),
        (
            ["hello", "world", "hello", "world"],
            3,
            [["hello", "world", "hello"], ["world"]],
        ),
    ],
)
def test_arrange_into_sublists(words, count, expected):
    assert _arrange_into_sublists(words, count) == expected


@pytest.mark.parametrize(
    "words, limit, expected",
    [
        (
            ["a", "the", "hello", "world"],
            None,
            ["a", "the", "hello", "world"],
        ),  # default behavior
        (["a", "the", "hello", "world"], 1, ["a", "", "hello", "world"]),
        (["a", "the", "hello", "world"], 2, ["", "", "hello", "world"]),
        (["a", "the", "hello", "world"], 3, ["", "", "hello", ""]),
        (["a", "the", "hello", "world"], 4, ["", "", "", ""]),
    ],
)
def test_replace_common_words_with_blanks(words, limit, expected):
    assert _replace_common_words_with_blanks(words, limit) == expected


def test_parse_words(response):
    grouped_words = _parse_words(response, 3)
    flattened = set()
    for words in grouped_words:
        flattened |= set(words)

    assert flattened == {
        "fortune",
        "say",
        "sleep",
        "",
        "arrows",
        "opposing",
        "suffer",
        "end",
        "nobler",
        "bear",
        "slings",
        "arms",
        "sea",
        "troubles",
        "outrageous",
        "Thus",
        "death",
        "dieto",
        "mind",
        "tis",
        "makes",
        "question",
        "Whether",
    }


def test_main(response):
    mock_args = MagicMock()
    mock_args.url = "https://google.com"
    mock_args.empty_boxes = 3
    with (
        patch(
            "src.sermon_bingo.__main__._parse_args", return_value=mock_args
        ) as mock_parse_args,
        patch(
            "src.sermon_bingo.__main__._download_sermon", return_value=response
        ) as mock_download_sermon,
        patch("src.sermon_bingo.__main__._save_to_pdf") as mock_save_to_pdf,
    ):
        main()

    mock_parse_args.assert_called_once()
    mock_download_sermon.assert_called_once_with(mock_args.url)
    mock_save_to_pdf.assert_called_once()
