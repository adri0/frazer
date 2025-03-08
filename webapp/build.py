import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader

from frazer import __version__


def build(env: str | None) -> None:
    load_dotenv(env, override=True)
    jinja_env = Environment(loader=FileSystemLoader("webapp"))
    template = jinja_env.get_template("frazer.html")
    context = {
        "url": os.environ["SENTENCE_API_URL"],
        "version": __version__,
    }
    output_html = template.render(context)
    output_path = Path("site/frazer.html")
    os.makedirs(output_path.parent, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        f.write(output_html)
    print("HTML file generated: frazer.html")


if __name__ == "__main__":
    env = sys.argv[1] if len(sys.argv) > 1 else None
    build(env)
