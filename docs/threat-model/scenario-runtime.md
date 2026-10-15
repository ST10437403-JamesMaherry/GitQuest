# Scenario runtime threat model

## Assets

- Files outside GitQuest's generated workspace root
- The player's real Git repositories and credentials
- Integrity of scenario scores and generated evidence

## Trust boundaries

Scenario manifests and fixtures cross from repository content into filesystem and Git operations.
Player-edited workspaces cross back into the verifier. Generated evidence may later be shared in a
portfolio or CI artifact.

## Controls

- Workspace names and check paths reject traversal and absolute paths.
- GitQuest deletes only direct children of its managed root carrying the expected safety marker.
- Symlink workspace roots, workspaces, and fixture entries are rejected.
- Git commands use argument arrays, a timeout, captured output, and disabled terminal prompts.
- Scenario fixtures use fake training credentials and need no network access.
- Reports contain commit IDs and normalized results, not file contents or secret values.
- Every scenario has deterministic failing and passing integration tests.

## Residual risks

- A malicious local user with write access can alter scenario manifests or session metadata.
- Regex checks prove the declared learning outcome, not complete workflow security.
- Deleting a secret in the remediation commit does not purge it from earlier Git history; the
  scenario debrief explicitly calls out rotation and history cleanup as real incident steps.
