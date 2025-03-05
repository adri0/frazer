import os
import sys

from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader

from frazer import __version__


def build(env: str | None) -> None:
    load_dotenv(env, override=True)
    jinja_env = Environment(loader=FileSystemLoader("frontend"))
    template = jinja_env.get_template("frazer.html")
    context = {
        "url": os.environ["SENTENCE_API_URL"],
        "version": __version__,
    }
    output_html = template.render(context)
    with open("site/frazer.html", "w", encoding="utf-8") as f:
        f.write(output_html)
    print("HTML file generated: frazer.html")


if __name__ == "__main__":
    env = sys.argv[1] if len(sys.argv) > 1 else None
    build(env)
