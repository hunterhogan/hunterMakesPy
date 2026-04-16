# Software development issues and wishlist

## `[dependency-groups]`

I don't know how VS Code/Python Environments handles `[dependency-groups]`. I'm 95% sure it is `uv` under the hood, so I can probably get this to work without much effort.

### Testing

I currently define `testing` as an "extra" in many packages, but it's not really an extra.

1. Migrate away from using `project.optional-dependencies, testing = ...`
2. Use `[dependency-groups]`.
3. Change "pythonTests.yml" away from `run: pip install -e .[testing]`.
4. When trying to build wheels with `cibuildwheel` in "pypiRelease.yml", running the tests was an obstacle. `[dependency-groups]` could help a little.

### Development or "dev"

I sometimes define `development` as an "extra" in packages, but it's not really an extra.

1. Migrate away from using `project.optional-dependencies, development = ...`
2. Use `[dependency-groups]`.
3. `uv` uses "dev" as a special group name, but I dislike diminutives.
4. If I use `uv`, then I will probably want to use their [Default groups feature](https://docs.astral.sh/uv/concepts/projects/dependencies/#default-groups).

## Default files for repos

<https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file>

## Documentation

- Context7 clearly treats the README as the primary documentation source.
- Would a README in humpy_cytoolz, for example, add value for humans and for AI assistants?
- More explicitly describe context7/AI assistants as an audience for documentation?

## dependabot

- Learn more about it.

## "Packaging" and/or make it easier for people who clone the repo to set up the environment

- AI instructions
- Font selection: code-workspace
- From hunterMakesPy.PackageSettings: the variables I wish were fixed during packaging and installation.
- How to intelligently include the tests?
- Switch to uv?

## A Python formatter that formats my style

There seem to be some tools for creating formats that aren't "Black" or "PEP 8", but they all seem to be a huge pain in the ass.

## An easier way to type CJK

I use code snippets to enter ideograms, which is limiting and annoying. I haven't been able to get alt-codes to work. Installing font with package?

## Simple sorting of functions

I can easily sort lines. But I want a fast way to alpha sort functions.

## Ruff

In general, I love it. But I need to have different "levels" of strictness for different files. When I am developing a file or
function, I don't want diagnostics about commented out code or print or a bunch of other things.

## Tools to integrate into VS Code or consider using

- grepWin UI
- grepWin CLI? It is in PATH.
- nirSoft searchMyFiles
- ss64.com
- Everything Search
- pyflakes
