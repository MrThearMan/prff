# Fast-forward merge for pull requests

This action adds the ability to fast-forward merge pull requests by
commenting a predefined comment on the pull request.

Example:

```yaml
name: Fast-forward

on:
  issue_comment:
    types:
      - created
      - edited

jobs:
  fast-forward:

    name: Fast-forward
    runs-on: ubuntu-latest

    permissions:
      contents: write  # Allows merging the PR.
      pull-requests: write  # Writing comments on PRs.
      issues: write  # Also required for posting comments on PRs.

    # Only run if the comment is one of the defined keywords.
    if: >-
      ${{
        github.event.issue.pull_request
        && contains(fromJSON('["/fast-forward", "/ff"]'), github.event.comment.body)
      }}

    steps:
      - name: Fast-forward
        uses: MrThearMan/prff@v1
```

With this, by commenting either `/ff` or `/fast-forward` on the pull request, the action
will run to check if the fast forward merge is possible, and that the commenter has
the requird permissions to make that merge, and then make the merge if those checks pass.

If this operation is unsuccessful, a comment will be added to the pull request
with the error. A detailed report is also written to the actions summary.
