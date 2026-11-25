#!/usr/bin/env python3
"""Generate a reference image with Gemini through a local Gemini MCP server (streamable HTTP).

    python3 gemini_image.py <name> "<prompt>" [reference_image ...]

Requires an MCP server exposing `gemini_generate_image(prompt, reference_images=[abs paths])`
(default http://127.0.0.1:8772/mcp, override with GEMINI_MCP_URL) and the `mcp` Python package.
Prints the tool's JSON reply, which includes the saved image path.

The output is a REFERENCE, not a deliverable: redraw it as vectors (Illustrator), and proof every
word of text, because the model redraws rather than pastes.
"""
import asyncio, os, sys
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

URL = os.environ.get('GEMINI_MCP_URL', 'http://127.0.0.1:8772/mcp')


async def main(name, prompt, refs):
    refs = [os.path.abspath(r) for r in refs]
    async with streamablehttp_client(URL) as (r, w, _):
        async with ClientSession(r, w) as s:
            await s.initialize()
            res = await s.call_tool('gemini_generate_image', {'prompt': prompt, 'reference_images': refs})
            print(name, [c.text for c in res.content])


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    asyncio.run(main(sys.argv[1], sys.argv[2], sys.argv[3:]))
