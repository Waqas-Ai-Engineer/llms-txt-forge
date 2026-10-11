# llms-txt-forge

> Generate and validate `llms.txt` for any website in one command - make your site readable by ChatGPT, Claude, Perplexity and other AI search tools. Zero dependencies.

![python](https://img.shields.io/badge/python-3.8%2B-blue) ![license](https://img.shields.io/badge/license-MIT-green) ![deps](https://img.shields.io/badge/dependencies-0-brightgreen) ![tests](https://img.shields.io/badge/tests-7%20passing-brightgreen)

## Quickstart (under 2 minutes, works offline)

```bash
git clone https://github.com/Waqas-Ai-Engineer/llms-txt-forge
cd llms-txt-forge
python -m llmstxt generate examples/site --name "BrightSmile Dental Clinic" --base-url https://brightsmile.example
python -m llmstxt validate llms.txt
```

Live site (same-origin, sitemap-first, polite delay):

```bash
python -m llmstxt generate https://yoursite.com --name "Your Business" --max-pages 40 --full
```

## Problem

AI assistants increasingly answer questions by reading websites. The [llms.txt](https://llmstxt.org) convention gives them a clean, curated map of your site, but writing one by hand for every client site is tedious and easy to get wrong.

## Solution

`llms-txt-forge` crawls a site (or a local HTML export), extracts title and description per page, groups pages into sections, skips `noindex` pages, and writes a spec-shaped `llms.txt`. A validator checks any existing file.

## Features

- Live crawl (stdlib only, same-origin, sitemap-first, rate limited) or offline folder mode
- Sections inferred from URL paths (Services, Pricing, Docs...); blog/case studies go under `## Optional`
- Respects `<meta name="robots" content="noindex">`
- Optional `llms-full.txt` with page text for LLM ingestion
- `validate` command with CI exit codes (H1, summary, sections, link format, duplicates)
- Great for agencies: run it per client site and ship the file

## Example output

```
# BrightSmile Dental Clinic

> Family dental clinic in Austin offering checkups, whitening and same-day emergency appointments.

## Main

- [BrightSmile Dental Clinic](https://brightsmile.example/): Family dental clinic in Austin offering checkups, whitening and same-day emergency appointments.

## Pricing

- [Pricing](https://brightsmile.example/pricing): Transparent prices for common treatments.

## Services

- [Emergency Dentist](https://brightsmile.example/services/emergency): Toothache or broken tooth? We offer same-day emergency appointments Monday to Saturday.
- [Teeth Whitening](https://brightsmile.example/services/whitening): Professional in-chair whitening in about 60 minutes.

## Optional

- [How Often Should You Floss?](https://brightsmile.example/blog/how-often-should-you-floss): A short guide to flossing habits.
```

## Architecture

```
site URL or folder -> crawl.py -> extract.py (title/description/links) -> build.py (sections) -> llms.txt
                                                                      \-> validate.py
```

## Use with n8n

Execute Command node: `python -m llmstxt generate https://client.com --name "Client"`, then upload `llms.txt` to the client's web root via SFTP/FTP node.

## Project structure

```
llmstxt/   crawl.py extract.py build.py validate.py cli.py
tests/     unittest suite (offline)
examples/  sample dental-clinic site
```

## Honesty note

llms.txt is an emerging convention; support among AI providers varies and no ranking or traffic gains are claimed. Example site is fictional.

## Future improvements

JS-rendered pages, hreflang/multilingual output, auto-generated per-section summaries via an optional LLM.

## Hire me / Need this built?

Need AI-search visibility, lead capture or business automation built for your company? I'm **Muhammad Waqas - AI Agents & Business Automation**. Reach me via my [GitHub profile](https://github.com/Waqas-Ai-Engineer).

## License

MIT
