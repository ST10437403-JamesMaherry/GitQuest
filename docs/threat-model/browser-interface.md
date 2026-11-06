# Browser interface threat model

## Boundary

GitQuest serves a packaged interface on `127.0.0.1`. It is a local single-player application, not a
production internet service. The current browser is read-only; future labs will mutate only marked
GitQuest workspaces through typed application operations.

## Assets to protect

- Repositories outside the GitQuest sandbox root
- User files and process environment
- Local Git configuration and credentials
- Lesson progress integrity
- Browser trust in local responses

## Primary threats and controls

| Threat | Control |
| --- | --- |
| Remote access to the local server | Bind to loopback and reject non-local Host headers |
| Browser injection | No inline code, strict CSP, DOM text APIs for lesson data |
| Framing and data leakage | Deny framing, referrers, remote assets, and unnecessary permissions |
| Arbitrary command execution | Expose typed allow-listed Git actions, never raw shell input |
| Path traversal | Resolve paths beneath a marked workspace and reject symlink escapes |
| Damage to personal repositories | Create disposable marked repositories under one managed root |
| Cross-origin mutation | Require non-simple JSON requests and a request-verification token |
| Oversized input | Bound request bodies and validate every field |

## Required review before interactive labs

Before adding browser mutation routes, document the exact action schema, allowed Git operations,
path containment checks, request-verification mechanism, failure cleanup, and integration tests for
host-header rejection, path traversal, symlink escape, malformed input, and workspace markers.
