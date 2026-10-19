# Browser interface threat model

## Scope

The local browser console serves static assets and a small JSON API on `127.0.0.1`. It can create or
reset GitQuest-managed scenario workspaces and verify their contents.

## Primary threats

- A malicious website attempts a cross-site request against the local server.
- DNS rebinding supplies an unexpected Host header.
- Scenario text is used for script or markup injection.
- Oversized or malformed requests consume local resources.
- A route is tricked into reading or writing an arbitrary local path.
- The interface accidentally sends user activity to a third party.

## Controls

- Mutation uses POST plus the non-simple `X-GitQuest-Request` header, with no cross-origin resource
  sharing headers.
- The request adapter accepts only `127.0.0.1` and `localhost` Host values.
- A Content Security Policy limits scripts, styles, images, and connections to the same origin.
- Dynamic text is assigned with `textContent`; fetched content is never passed to `innerHTML`.
- Request bodies are capped at one KiB and ignored because current mutation routes need no input.
- Routes accept validated scenario IDs only. Workspace and report paths are derived internally.
- Static assets are bundled locally. The application includes no analytics or remote resources.

## Residual risks

- Any process running as the same local user can call the API directly.
- This development server is intentionally single-user and must not be exposed to a network.
- Browser extensions retain the access granted by the user's browser profile.
