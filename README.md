Alfred Workflows
---

> This repo contains a collection of [Alfred](http://www.alfredapp.com/) workflow scripts written in python.

> _Note: This requires Alfred Powerpack_

## Workflows
- [Open GitHub Repo](#open-github-repo)

**To use these workflows, fork and clone this repo. Then when setting up a workflow you can point to the python scripts
in your repo and update the data files for your usage.**

## Open GitHub Repo
This workflow parses the query, matches the search terms (whitespace delimited) against a list of GitHub repos and a
list of GitHub users, and returns the matching results to Alfred. Selecting one of the results will open that repo
in the browser.

### Demo
![open github repo workflow demo](http://recordit.co/2Nq346nean.gif)

### Setup
1. Open Alfred > Workflows
1. Add a new workflow
1. Add a "Script Filter" input
  ![open github repo script filter configuration](images/open-github-repo/script-filter-config.png)
1. _Be sure to drag the GitHub icon from the icons/ directory to this script filter input_
1. Add a "Run Script" action
  ![open github repo run script action configuration](images/open-github-repo/run-script-config.png)
1. Link the input to the action
  ![open github repo workflow](images/open-github-repo/link-workflow.png)
1. Update the JSON data files ([data/git_repos.json](data/git_repos.json), [data/git_users.json](data/git_users.json))
for your use

## Thanks
Shout out to the following people and tools:

- [Alfred](http://www.alfredapp.com/)
- Jan Müller's [alfred-python](https://github.com/nikipore/alfred-python)