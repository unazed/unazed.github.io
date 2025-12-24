from jinja2 import Environment, FileSystemLoader
import markdown

import glob, os
import hashlib
import re


STATIC_DIR = "static/"
OUTPUT_DIR = "docs/"
POSTS_DIR = "posts/"
TEMPLATE_DIR = "templates/"
IMG_DIR = "img/"


def preprocess_obsidian_images(text: str) -> str:
  def repl(match):
    full = match.group(1).strip()
    parts = [p.strip() for p in full.split('|')]
    filename = parts[0]
    align = parts[1] if len(parts) > 1 else ''
    style = ' style="display:block;margin:0 auto;"' if align.lower() == 'center' else ''
    src = f"{IMG_DIR}/{filename}"
    return f'<img src="{src}"{style} />'
  return re.sub(r'!\[\[(.*?)\]\]', repl, text)


def main() -> None:
  env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
  post_template = env.get_template("post.html.j2")
  index_template = env.get_template("index.html.j2")

  md = markdown.Markdown(extensions=[
    'fenced_code',
    'codehilite',
    'extra',
    'meta',
    'mdx_math'
  ])

  post_dict: dict[str, list] = {
    "technical": [],
    "writing": []
  }

  for post_file in glob.glob(os.path.join(POSTS_DIR, "**/*.md"), recursive=True):
    with open(post_file, 'r', encoding='utf-8', errors='replace') as fd_post:
      post_content = fd_post.read()
      post_content = post_content.replace('\xa0', ' ').replace('\u00a0', ' ')
      post_content = preprocess_obsidian_images(post_content)

    title_hash = hashlib.md5(post_file.encode()).hexdigest()

    content = md.convert(post_content)
    metadata: dict[str, str] = {}
    if hasattr(md, 'Meta'):
      metadata = {
        key: value[0] if len(value) == 1 else value
        for key, value in md.Meta.items()
      }

    group = os.path.basename(os.path.dirname(os.path.dirname(post_file)))
    if group not in post_dict:
      group = os.path.basename(os.path.dirname(post_file))
    fallback_title = os.path.splitext(os.path.basename(post_file))[0]
    post_info = {
        "title": metadata.get("title", fallback_title),
        "filename": title_hash + ".html",
        "hash": title_hash
    }
    post_dict[group].append(post_info)

    output = post_template.render(
      title=post_info["title"],
      content=content,
    )

    with open(os.path.join(OUTPUT_DIR, post_info["filename"]), "w", encoding="utf-8") as fd_out:
      fd_out.write(output)

    md.reset()

  output = index_template.render(
    category="technical",
    posts=post_dict['technical']
  )
  with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as fd_index:
    fd_index.write(output)

  output = index_template.render(
    category="writing",
    posts=post_dict['writing'],
  )
  with open(os.path.join(OUTPUT_DIR, "writing.html"), "w", encoding="utf-8") as fd_index:
    fd_index.write(output)


if __name__ == "__main__":
  main()
