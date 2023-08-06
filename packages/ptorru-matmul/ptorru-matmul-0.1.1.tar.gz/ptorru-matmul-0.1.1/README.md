# ptorru-matmul

Learning about pipy, distributing a simple matrix multiply example

# Dependencies

[Poetry](https://python-poetry.org), [installation instructions](https://python-poetry.org/docs/).

# After clonning

```bash
cd ptorru-matmul
poetry init
```

# Running tests

```bash
poetry run pytest tests/
```

# Publishing

## Setup PyPI token

```bash
poetry config pypi-token.pypi <TOKEN>
```

## Build and Publish

```bash
poetry build
poetry publish
```

# References

Consulted these resources:

- [Utpal Kumar, The easiest way to publish a python package on PyPI using Poetry](https://www.earthinversion.com/utilities/easiest-way-to-publish-a-python-package-using-poetry/)
