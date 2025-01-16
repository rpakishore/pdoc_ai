<!--- Heading --->
<div align="center">
  <h1>pdoc_ai</h1>
  <p>
    Automated Python documentation generator
  </p>
  <a href="https://rpakishore.github.io/pdoc_ai/pdoc_ai.html"> Documentation</a>
</div>
<br />

![GitHub commit activity](https://img.shields.io/github/commit-activity/m/rpakishore/pdoc_ai)
![GitHub last commit](https://img.shields.io/github/last-commit/rpakishore/pdoc_ai)
<!-- Table of Contents -->
<h2>Table of Contents</h2>

- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
- [Usage](#usage)
- [Roadmap](#roadmap)
- [License](#license)
- [Contact](#contact)

<!-- Features -->
## Features

- CLI commands to document packages and files
- Automatic docstring generation in Google format
- Support for excluding specific files or patterns
- Integration with LLM for enhanced documentation

<!-- Getting Started -->
## Getting Started

<!-- Prerequisites -->
### Prerequisites

Python 3.12 or above

<!-- Usage -->
## Usage

To use pdoc_ai, install the package and run the CLI commands. For example:

```bash
# Document an entire package
python -m pdoc_ai.cli_app package /path/to/your/package

# Document a specific file
python -m pdoc_ai.cli_app file /path/to/your/package your_file.py

# Clean up generated files
python -m pdoc_ai.cli_app clean /path/to/your/package
```

<!-- Roadmap -->
## Roadmap

- [x] Set up a skeletal framework
- [ ] Todo 2

<!-- License -->
## License

See [LICENSE](/LICENSE) for more information.

<!-- Contact -->
## Contact

Arun Kishore - [@rpakishore](mailto:pypi@rpakishore.co.in)

Project Link: [https://github.com/rpakishore/pdoc_ai](https://github.com/rpakishore/pdoc_ai)
