import asyncio

from marimo import MarimoIslandGenerator

generator = MarimoIslandGenerator.from_file("src/data-files/tem-stem-reciprocity.py")
app = asyncio.run(generator.build())
body = generator.render_body()
print(body)
