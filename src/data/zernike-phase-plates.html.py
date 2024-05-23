import asyncio

from marimo import MarimoIslandGenerator

generator = MarimoIslandGenerator.from_file("src/data-files/zernike-phase-plates.py")
app = asyncio.run(generator.build())
body = generator.render_body()
print(body)
