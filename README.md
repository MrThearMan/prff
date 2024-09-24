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

## Note about triggering other workflows

Due to the way GitHub works, pushed created using github actions bots 
[do not trigger additional workflows], even if the the workflow would 
otherwise be triggered. This applies to this fast-forward action as well.

To trigger additional workflows, you can use the `repository_dispatch` event.
Add the following step to your workflow after `uses: MrThearMan/prff@v1`:

```yaml
- name: Trigger tests
  run: |
    curl -L \
      -X POST \
      -H "Accept: application/vnd.github+json" \
      -H "Authorization: Bearer ${{ secrets.GITHUB_TOKEN }}" \
      -H "X-GitHub-Api-Version: 2022-11-28" \
      -H "User-Agent: ${{ github.repository }}" \
      https://api.github.com/repos/${{ github.repository }}/dispatches \
      -d '{"event_type":"fast-forward"}'
```

You also need to add the following trigger to the workflow(s) you want to trigger:

```yaml
on:
  repository_dispatch:
    types:
      - fast-forward
```

> Note: The `event_type` in the curl command matches the `types` in the workflow trigger.

> Note: If fast-forwarding a pull request fails, the additional workflow will not be triggered,
> since its part of the same job. If desired, you can use the [continue-on-error] option on the
> fast-forward action to run the additional workflow even if the fast-forwarding fails.

[do not trigger additional workflows]: https://docs.github.com/en/actions/security-for-github-actions/security-guides/automatic-token-authentication#using-the-github_token-in-a-workflow
[continue-on-error]: https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#jobsjob_idstepscontinue-on-error
