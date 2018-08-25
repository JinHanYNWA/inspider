# inspider
A tool for downloading Instagram pictures.
You can download pictures from a post url or user's homepage.

## Usage
Open terminal in the repository floder.
- From Post:
    ```bash
    python inspider.py --mode p --url <the post link>
    ```
    *The downloded media will be saved in `<current folder>/<Images>` by default.*

- From User's Homepage:
    ```bash
    python inspider.py --mode u --url <the homepage link> --count <default 20>
    ```
    *The downloded media will be saved in `<current folder>/<username>` by default.*

*NOTE: When downloading many pictures, there maybe some failde links, which will be saved in `FailedUrls.txt`.*