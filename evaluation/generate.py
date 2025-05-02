import csv
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import click

from frazer.analyser import AnalysedSentence, analyse_sentence


def save_sentences_to_csv(
    analyzed_sentences: list[AnalysedSentence], output_file: Path
):
    """
    Analyzes a list of sentences and saves the results in a CSV file.

    Args:
        analyzed_sentences (list[Sentence]): List of analyzed sentences.
        output_file (str): Path to the output CSV file.
    """
    header = [
        "sentence_text",
        "word_original_value",
        "word_root",
        "word_original_value_translation",
        "word_syntactic_category",
        "word_aspect",
        "word_conjugation",
        "word_object",
        "word_declension_case",
        "word_verb_causing_declension",
        "sentence_remarks",
    ]

    with open(output_file, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()

        for analyzed_sentence in analyzed_sentences:
            # Write each word in the sentence to the CSV
            for word in analyzed_sentence.words:
                writer.writerow(
                    {
                        "sentence_text": analyzed_sentence.text,
                        "word_original_value": word.original_value,
                        "word_root": word.root,
                        "word_original_value_translation": word.original_value_translation,
                        "word_syntactic_category": word.syntatic_category,
                        "word_aspect": getattr(word, "aspect", None),
                        "word_conjugation": getattr(word, "conjugation", None),
                        "word_object": getattr(word, "object", None),
                        "word_declension_case": getattr(word, "declension_case", None),
                        "word_verb_causing_declension": getattr(
                            word, "verb_causing_declension", None
                        ),
                        "sentence_remarks": analyzed_sentence.remarks,
                    }
                )


@click.command()
@click.option(
    "--input",
    type=click.Path(exists=True, path_type=Path),
    default="input.txt",
    help="Input file containing sentences on each line.",
)
@click.option(
    "--output",
    type=click.Path(path_type=Path),
    required=True,
    help="Path to the output CSV file.",
)
def main(input: Path, output: Path) -> None:
    """
    Command-line interface for analyzing sentences from a specified input file and saving results to a CSV file.

    Args:
        input_file (Path): Path to the input text file.
        output_file (Path): Path to the output CSV file.
    """
    with input.open("r", encoding="utf-8") as file:
        sentences = [line.strip() for line in file if line.strip()]

    def analyze_sentence_wrapper(sentence: str) -> AnalysedSentence | None:
        try:
            return analyse_sentence(sentence)
        except Exception as e:
            print(f"Error analyzing sentence '{sentence}': {e}")
            return None

    with ThreadPoolExecutor(max_workers=4) as executor:
        analyzed_sentences = list(
            filter(None, executor.map(analyze_sentence_wrapper, sentences))
        )

    save_sentences_to_csv(analyzed_sentences, output)


if __name__ == "__main__":
    main()
