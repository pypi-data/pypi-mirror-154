# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['web2preview', 'web2preview.tests']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.0,<5.0', 'requests>=2.0,<3.0']

entry_points = \
{'console_scripts': ['web2preview = web2preview.cli:main']}

setup_kwargs = {
    'name': 'web2preview',
    'version': '1.1.3',
    'description': 'Extracts OpenGraph, TwitterCard and Schema properties from a webpage.',
    'long_description': '# web2preview\n\nFor a given URL `web2preview` extracts its **title**, **description**, and **image url** using\n[Open Graph](http://ogp.me/), [Twitter Card](https://dev.twitter.com/cards/overview), or\n[Schema](http://schema.org/) meta tags, or, as an alternative, parses it as a generic webpage.\n\n<p>\n    <a href="https://pypi.org/project/web2preview/"><img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/web2preview"></a>\n    <a href="https://pypi.org/project/web2preview/"><img alt="PyPI" src="https://img.shields.io/pypi/v/web2preview?logo=pypi&color=blue"></a>\n    <a href="https://github.com/vduseev/web2preview/actions?query=workflow%3Atest"><img alt="Build status" src="https://img.shields.io/github/workflow/status/vduseev/web2preview/test?label=build&logo=github"></a>\n    <a href="https://codecov.io/gh/vduseev/web2preview"><img alt="Code coverage report" src="https://img.shields.io/codecov/c/github/vduseev/web2preview?logo=codecov"></a>\n</p>\n\nThis is a **fork** of an excellent [webpreview] library and it maintains **complete and absolute**\ncompatibility with the original while fixing several bugs, enhancing parsing, and adding a new\nconvenient APIs.\n\n*Main differences between `web2preview` and `webpreview`*:\n\n* Enhanced parsing for generic web pages\n* No unnecessary `GET` request is ever made if `content` of the page is supplied\n* Complete fallback mechanism which continues to parse until all methods are exhausted\n* Python Typings are added across the entire library (**better syntax highlighting**)\n* New dict-like `WebPreview` result object makes it easier to read parsing results\n* Command-line utility to extract title, description, and image from URL\n\n## Installation\n\n```shell\npip install web2preview\n```\n\n## Usage\n\nUse the generic `web2preview` method to parse the page independent of its nature.\nIt tries to extract the values from Open Graph properties, then it falls back to\nTwitter Card format, then Schema. If none of them can extract all three of the title,\ndescription, and preview image, then webpage\'s content is parsed using a generic\nextractor.\n\n```python\n>>> from web2preview import web2preview\n\n>>> p = web2preview("https://en.wikipedia.org/wiki/Enrico_Fermi")\n>>> p.title\n\'Enrico Fermi - Wikipedia\'\n>>> p.description\n\'Italian-American physicist (1901–1954)\'\n>>> p.image\n\'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Enrico_Fermi_1943-49.jpg/1200px-Enrico_Fermi_1943-49.jpg\'\n\n# Access the parsed fields both as attributes and items\n>>> p["url"] == p.url\nTrue\n\n# Check if all three of the title, description, and image are in the parsing result\n>>> p.is_complete()\nTrue\n\n# Provide page content from somewhere else\n>>> content = """\n<html>\n    <head>\n        <title>The Dormouse\'s story</title>\n        <meta property="og:description" content="A Mad Tea-Party story" />\n    </head>\n    <body>\n        <p class="title"><b>The Dormouse\'s story</b></p>\n        <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>\n    </body>\n</html>\n"""\n\n# This function call won\'t make any external calls,\n# only relying on the supplied content, unlike the example above\n>>> web2preview("aa.com", content=content)\nWebPreview(url="http://aa.com", title="The Dormouse\'s story", description="A Mad Tea-Party story")\n```\n\n### Using the command line\n\nWhen `web2preview` is installed via `pip` the accompanying command-line tool is intalled alongside.\n\n```shell\n$ web2preview https://en.wikipedia.org/wiki/Enrico_Fermi\ntitle: Enrico Fermi - Wikipedia\ndescription: Italian-American physicist (1901–1954)\nimage: https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Enrico_Fermi_1943-49.jpg/1200px-Enrico_Fermi_1943-49.jpg\n\n$ web2preview https://github.com/ --absolute-url\ntitle: GitHub: Where the world builds software\ndescription: GitHub is where over 83 million developers shape the future of software, together.\nimage: https://github.githubassets.com/images/modules/site/social-cards/github-social.png\n```\n\n*Note*: For the Original [webpreview] API please check the [official docs][webpreview].\n\n## Run with Docker\n\nThe docker image can be built and ran similarly to the command line.\nThe default entry point is the `web2preview` command-line function.\n\n```shell\n$ docker build -t web2preview .\n$ docker run -it --rm web2preview "https://en.m.wikipedia.org/wiki/Enrico_Fermi"\ntitle: Enrico Fermi - Wikipedia\ndescription: Enrico Fermi (Italian: [enˈriːko ˈfermi]; 29 September 1901 – 28 November 1954) was an Italian (later naturalized American) physicist and the creator of the world\'s first nuclear reactor, the Chicago Pile-1. He has been called the "architect of the nuclear age"[1] and the "architect of the atomic bomb".\nimage: https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Enrico_Fermi_1943-49.jpg/1200px-Enrico_Fermi_1943-49.jpg\n```\n\n*Note*: built docker image weighs around 210MB.\n\n[webpreview]: https://github.com/ludbek/webpreview\n\n## Testing\n\n```shell\n# Execute the tests\npoetry run pytest web2preview\n\n# OR execute until the first failed test\npoetry run pytest web2preview -x\n```\n\n## Setting up development environment\n\n```shell\n# Install a correct minimal supported version of python\npyenv install 3.7.13\n\n# Create a virtual environment\n# By default, the project already contains a .python-version file that points\n# to 3.7.13.\npython -m venv .venv\n\n# Install dependencies\n# Poetry will automatically install them into the local .venv\npoetry install\n\n# If you have errors likes this:\nERROR: Can not execute `setup.py` since setuptools is not available in the build environment.\n\n# Then do this:\n.venv/bin/pip install --upgrade setuptools\n```',
    'author': 'vduseev',
    'author_email': 'vagiz@duseev.com',
    'maintainer': 'vduseev',
    'maintainer_email': 'vagiz@duseev.com',
    'url': 'https://github.com/vduseev/web2preview',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
