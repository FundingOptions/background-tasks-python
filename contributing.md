# Contributing to Funding Options' Background Tasks

Contributions are welcome, and they are greatly appreciated! Every little bit helps,
and credit will always be given.

## Types of Contributions

### Report Bugs

Report bugs on the [Github Repo][issues].

If you are reporting a bug, please include:
- The version you are running
- Any details about your local setup that might be helpful
- Reproduction steps

### Fix Bugs

Look through the [Github issues][bugs] for bugs. Anything tagged with "bug" or "help wanted" is
open to whoever wants to implement it.

### Implementing Features

Look through the [GitHub issues][features] for features. Anything tagged with "enhancement" and
"help wanted" is open to whoever wants to implement it.

### Write Documentation

We could always use more documentation, whether as part of the official
docs, in docstrings, or even on the web in blog posts, articles, and such.

### Submit Feedback

The best way to send feedback is to file an [issue][issues] on Github.

If you are proposing a feature:
- Explain in detail how it would work
- Keep the scope as narrow as possible, to make it easier to implement
- Try to give an example of what you're looking for

## Get Started

Ready to contribute? Here's how to get setup:

1. Fork the repo on Github
2. Clone your fork locally
3. Setup a virtual environment
   This repository uses [poetry][poetry] for this, which can be easily installed
   following the [installation instructions][poetry-installation].
5. Install the development dependencies
   You can use `make install` for this.
6. Checkout a new branch (`git checkout -b branch-name`)
   Now you can make your changes locally
7. Once you're done, make sure [Linting][linting] and [Testing][testing] passes

## Validating Changes

### Linting

3 Linters have been set up to adhere to our style guidelines:

- isort
- black
- autoflake

You can check your changes by running `make lint` to get a report.

To fix any linting issues, run:

```
make fixlint
```

### Testing

Testing is as simple as running:

```
make test
```

This will run the pytest suite. Note that there are 2 important plugins loaded as part of this:

- [pytest-cov][pytest-cov] Generates a coverage report of the tests
- [pytest-randomly][pytest-randomly] Ensures that tests don't always run in the same order
  (prevents order dependent tests)


[issues]: https://github.com/FundingOptions/background-tasks-python/issues
[bugs]: https://github.com/FundingOptions/background-tasks-python/issues?q=is:issue+label:bug
[features]: https://github.com/FundingOptions/background-tasks-python/issues?q=is:issue+label:enhancement
[poetry]: https://github.com/python-poetry/poetry
[poetry-installation]: https://github.com/python-poetry/poetry#installation
[pytest-cov]: https://github.com/pytest-dev/pytest-cov
[pytest-randomly]: https://github.com/pytest-dev/pytest-randomly
[linting]: #Linting
[testing]: #Testing
