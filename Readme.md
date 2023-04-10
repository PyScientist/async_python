## Asynchronous Python version 1.0 by PyScientist

The repository demonstrates the work of asynchronous Python (asyncio) with http asynchronous requesting (aiohttp) and asynchronous writing files (aiofiles).

The hard thing that asynchronous actions need to be launched from console.
For this purpose I have been used "run_in_executor"

The console application can be asked for help by help keyword.

For testing purpose used resource https://jsonplaceholder.typicode.com/
which provided the simple api for post fetching.

## In addition.... 

In files "pep8_download_syn.py"
and "pep8_download_asyn.py"

Provided the simple examples of synchronous and asynchronous version for
making requests to url. These are the slightly changed examples from:

Hands-on Intro to aiohttp (PyCon tutorial) by Mariatta Wijaya, Andrew Svetlov May 18, 2021

It is interesting that in "pep8_download_asyn.py" in the very end of performing the traceback appeared
that "loop.closed", I suppose incorrectly. but i cannot understand why. probably i wil resolve this issue in the future. I'm sure that I will fi it, or find out the reason.

There is one more interesting file with example of an organising tasks "hands_on.py" its from my code only.

Hope you find it interesting, and it will be useful for you!
