# Frazer

Frazer is an LLM-powered application for performing syntactical analysis of sentences in the Polish language. Sentences are categorized word by word, providing their syntatic function and additional linguistic details.

## Features

- **Word-by-Word Analysis**: Each word in the sentence is categorized into syntactic categories such as nouns, verbs, adjectives, pronouns, etc.
- **Translation**: Provides an English translation of the input Polish sentence.
- **Linguistic Details**:
  - For verbs: Identifies the aspect (perfective or imperfective) and conjugation, and specifies the object it acts upon.
  - For nouns, numerals, and adjectives: Specifies the declension case and the verb causing the declension.
  - For other syntactic functions: Labels the word as "other" and provides its syntactic function.
- **Remarks**: Highlights any potential spelling or grammatical mistakes in the sentence.

## Installation

To install the module and its dependencies, use the following command:

```bash
pip install .
```

## Usage

### Command-Line Interface

Frazer provides a CLI tool to analyze sentences. Run the following command:

```bash
python -m frazer "Kocham piękne kwiaty."
```

The output will include a YAML-formatted analysis of the sentence, with keys and values colorized for better readability.

### Programmatic Usage

You can also use Frazer programmatically in your Python code:

```python
from frazer.analyser import analyse_sentence

sentence = "Kocham piękne kwiaty."
result = analyse_sentence(sentence)
print(result.model_dump())
```
