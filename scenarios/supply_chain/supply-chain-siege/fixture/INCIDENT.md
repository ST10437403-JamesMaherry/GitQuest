# Incident brief: Supply Chain Siege

The release pipeline was stopped after a credential was committed and an unreviewed network
installer appeared in the workflow. Treat every value in this repository as training data—never
place a real credential in a GitQuest workspace.

Your approved remediation is to:

1. remove `.env` from the worktree and Git index;
2. add `.env` to `.gitignore`;
3. replace the mutable checkout tag with this reviewed training pin:
   `actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683`;
4. replace the remote pipe-to-shell command with `bash ./scripts/install-tool.sh`;
5. commit every remediation change.

Run `gitquest scenario verify supply-chain-siege` from this directory or any other directory when
you are ready for assessment.
