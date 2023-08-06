# Monkeytale v0.2.9

> "The book is a program." - [Matthew Butterick](https://docs.racket-lang.org/pollen/big-picture.html)

Monkeytale is a markup language for documenting and composing a story world and its novels within flat files. I am building this language to meet my opinionated needs for improving insights into my own writing.

## Design Principles

As to adherence to these principles, here's a useful bit from The Zen of Python to keep in mind:

> Special cases aren't special enough to break the rules.
Although practicality beats purity.

- **Don't opine. Document.**</br>Monkeytale will try to collect all kinds of information on your writing, but will not tell you where or how to improve.
- **Story lives within the writing**</br>Monkeytale should work in the background and not demand attention. As such, file names and folder structures, while necessary and useful, should not have to reflect your story structure. Likewise, Monkeytale should require only one syntax format to be learned and no configuration.
- **Durability through simplicity**</br>Flat text files and binary media assets (JPG, MP3, etc.) are the backbone of long-lived systems, open to version control management.

## Planned Functionality
- Compose multiple narratives by (re-)using story components
- Execute from continuous integration server
- Derive story structure knowledge from story components and their content
- Provide plugin mount point for generation of documents from story structure extracted by Monkeytale
- Navigate to any named story component

## Dismissed Functionality
- Advice on how to improve or correct the writing
- Typography and formatting, other than emphasis (italics)
- Tables of content and indexing
- Project management and goal tracking (unless hard deadlines ever become a reality for me)
- Stuff other folks have done better

## Development Progress
Monkeytale is developed in spare time and uses [Semantic Versioning](https://semver.org/) and [Semantic Release](https://pypi.org/project/python-semantic-release/) to track its, equally spare, progress.

As per Semantic Versioning: "Major version zero (0.y.z) is for initial development. Anything MAY change at any time. The public API SHOULD NOT be considered stable."

Check the [change log](https://github.com/MLAOPDX/monkeytale/blob/main/CHANGELOG.md) for the latest updates.

## Decisions
- [Python 3](https://www.python.org/) will be the programming language for Monkeytale and any plugins that folks might want to build
- [Visual Studio Code](https://code.visualstudio.com/) (VSCode) will be the text editor of choice
- [GruntFuggly's ToDoTree](https://marketplace.visualstudio.com/items?itemName=Gruntfuggly.todo-tree) extension for VS Code will be used to support navigation
- [Markdown Preview Enhanced](https://marketplace.visualstudio.com/items?itemName=shd101wyy.markdown-preview-enhanced) extension for Markdown and Mermaid diagram display and conversion to docx using [PanDoc](https://pandoc.org/) and PDF using Safari.
- [Github Actions](https://github.com/features/actions) as execution platform
- Use .@ as the file extension to indicate Monkeytale files.
- Delivery system will be to fork a git repo that has a workflow defined to run Monkeytale.
