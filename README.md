# Data Science Example

This project demonstrates the setup and usage of a repo for data science projects, specifically showcasing the [DSLP](https://github.com/dslp/dslp/tree/main) branching strategy.

## Table of Contents
- [Data Science Example](#data-science-example)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Pre-Commit Hooks](#pre-commit-hooks)
  - [Contributing](#contributing)
  - [License](#license)

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/RonMallory/data-science-example.git
   cd nist-terminology-dataset
   ```

2. **Setup with Poetry**:

   Ensure you have [Poetry](https://python-poetry.org/docs/) installed:

   ```bash
   poetry install
   ```

   This command installs all the necessary dependencies specified in `pyproject.toml`.

## Pre-Commit Hooks

This project uses `pre-commit` to maintain code quality and consistency. The following hooks are in place:

```bash
pre-commit install
```

## Contributing

1. Fork the project.
2. Create a branch based on the DSLP strategy: `git checkout -b feature/new-feature`
3. Commit your changes: `git commit -am 'Add new feature'`
4. Push to the branch: `git push origin feature/new-feature`
5. Submit a pull request against the appropriate DSLP branch.

## License

This project is licensed under the MIT License.
