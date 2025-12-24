from jinja2 import Environment, FileSystemLoader
import markdown

import glob, os
import hashlib


STATIC_DIR = "static/"
OUTPUT_DIR = "docs/"
POSTS_DIR = "posts/"
TEMPLATE_DIR = "templates/"


def main() -> None:
  env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
  template = env.get_template("post.html.j2")
  md = markdown.Markdown(extensions=[
    'fenced_code',
    'codehilite',
    'extra',
    'meta'
  ])
  metadata: dict[str, str] = {}
  if hasattr(md, 'Meta'):
    metadata = {
      key: value[0] if len(value) == 1 else value
      for key, value in md.Meta.items()
    }

  # Render the posts first
  os.mkdir(os.path.join(OUTPUT_DIR, "posts"))
  for post in glob.glob(os.path.join(POSTS_DIR, "*.md")):
    with open(post) as fd_post:
      post_content = fd_post.read()
    title = hashlib.md5(post.encode())
    output = template.render(
      **{
        "title": metadata.get("title", "Unnamed"),
        "content": md.convert(post_content)
      }
    )
    with open(os.path.join(OUTPUT_DIR, "posts", title.hexdigest() + ".html"), "w") as fd_post:
      fd_post.write(output)
    

if __name__ == "__main__":
  main()