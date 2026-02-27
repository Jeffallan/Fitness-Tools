# How To Contribute

When contributing to this repository, please discuss the change you wish to make first via issue,
[email](mailto:maverickcoders@pm.me), or any other method with the owners of this repository before making a change.

We have pull request guidelines and a code of conduct; please follow these in all your interactions with the project.

## Pull Request Guidelines

### Only Edit Relevant Files

- Focus your pull request on a single feature or issue.
- Do not change files unrelated to that specific issue or feature.

### Submit Clean Code

- Follow [PEP 8](https://peps.python.org/pep-0008/) conventions.
- Run `ruff check` before submitting.
- Run `mypy --strict fitness_tools/` to verify type safety.

### Write Tests

This project uses [pytest](https://docs.pytest.org/en/latest) for unit tests.

- If you're adding a feature, write tests to support it.
- If you're fixing a bug, add tests to reproduce it.

### Make Sure Your Tests Pass

Run the full test suite from the root directory:

```bash
python -m pytest tests/ -v
```

### Keep Commit History Short and Clean

Make one commit per feature or bug. Short histories aid in finding bugs and identifying the best fixes.

### Be Descriptive

State a convincing case why your PR should be accepted.

## Code of Conduct

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
