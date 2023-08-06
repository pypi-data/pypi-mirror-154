# arXiv Renamer

This package has a utility called `arxiv-renamer` that can be used to rename `pdf` files downloaded from [arXiv](https://arxiv.org).
It creates a slug of the form `<id>-<authors>-<title>` and renames the original file to that slug.

Another utility called `arxiv-watcher` can be used to watch for new (or moved) files in a directory and rename them.

## Usage

```
python arxiv-renamer.py <path>
```

```
python arxiv-watcher.py <watch dir>
```
