import csv
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import NamedTuple

import click

from frazer.analyser import AnalysedSentence, analyse_sentence


class InputRecord(NamedTuple):
    id: int
    sentence: str


class AnalysedSentenceRecord(NamedTuple):
    id: int
    analysed_sentence: AnalysedSentence


def read_input_sentences(input_path: Path) -> list[InputRecord]:
    """
    Reads input sentences from a CSV file and returns a list of InputRecord objects.

    Args:
        input_path (Path): The path to the input CSV file. The file is expected to have
            columns "id" (integer) and "sentence" (string).

    Returns:
        list[InputRecord]: A list of InputRecord objects, each containing an "id" and a "sentence".
    """
    input_records = []
    with input_path.open("r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            input_record = InputRecord(id=int(row["id"]), sentence=row["sentence"])
            input_records.append(input_record)
    return input_records


def analyse_input_records(
    input_records: list[InputRecord],
) -> list[AnalysedSentenceRecord]:
    """
    Batch analyse a list of input records by processing their sentences in parallel.

    Args:
        input_records (list[InputRecord]): A list of input records.

    Returns:
        list[AnalysedSentenceRecord]: A list of analysed sentence records.
    """

    def analyse_sentence_wrapper(
        input_record: InputRecord,
    ) -> AnalysedSentenceRecord | None:
        try:
            return AnalysedSentenceRecord(
                id=input_record.id,
                analysed_sentence=analyse_sentence(input_record.sentence),
            )
        except Exception as e:
            click.echo(f"Error analyzing input sentence '{input_record.sentence}': {e}")
            return None

    # Run analyses in parallel
    with ThreadPoolExecutor(max_workers=4) as executor:
        analyzed_sentences = list(
            filter(None, executor.map(analyse_sentence_wrapper, input_records))
        )

    return analyzed_sentences


def save_analysed_sentences(
    analysed_records: list[AnalysedSentenceRecord], output_file: Path
) -> None:
    """
    Save a list of analysed sentences in a CSV file.

    Args:
        analyzed_records (list[AnalysedSentenceRecord]): List of analyzed sentences.
        output_file (Path): Path to the output CSV file.
    """
    header = [
        "sentence_id",
        "word_original_value",
        "word_root",
        "word_original_value_translation",
        "word_syntactic_category",
        "word_aspect",
        "word_conjugation",
        "word_object",
        "word_declension_case",
        "word_verb_causing_declension",
    ]

    with open(output_file, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()

        for sentence_id, analysed_sentence in analysed_records:
            for word in analysed_sentence.words:
                writer.writerow(
                    {
                        "sentence_id": sentence_id,
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
                    }
                )


def batch_analyse(input: Path, output: Path) -> None:
    """
    Analyze sentences from an input CSV file and save results to an output CSV file.

    Args:
        input (Path): Path to the input CSV file.
        output (Path): Path to the output CSV file.
    """
    input_records = read_input_sentences(input_path=input)
    analysed_records = analyse_input_records(input_records=input_records)
    save_analysed_sentences(analysed_records=analysed_records, output_file=output)


@click.command()
@click.option(
    "--input",
    type=click.Path(exists=True, path_type=Path),
    default="input_sentences.csv",
    help="Input CSV file containing sentences with headers.",
)
@click.option(
    "--output",
    type=click.Path(path_type=Path),
    required=True,
    help="Path to the output CSV file.",
)
def main(input: Path, output: Path) -> None:
    """
    Analyze sentences from an input CSV file and save results to an output CSV file.
    """
    batch_analyse(input=input, output=output)


if __name__ == "__main__":
    main()
