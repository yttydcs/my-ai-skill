# Codex Visualization Preview Limitations

## Summary

Official Codex visualization fragments may validate correctly while the standalone render-helper preview behaves differently from the final inline host. In particular, browser automation may focus a native button without dispatching synthetic Enter / Space activation inside the sandboxed iframe, and preview infrastructure may emit console errors from code that is absent from the fragment.

## Lookup Hints

- Keywords: `$visualize:visualize`, `::codex-inline-vis`, sandboxed iframe, synthetic keyboard activation, `MutationObserver.observe`, preview host, `window.openai.sendFollowUpMessage`.
- Quick checks: search the fragment for the reported API, inspect native semantics and focus, click the primary interaction, capture its payload, compare viewport and scroll widths, and perform a final inline-host smoke check.

## Symptoms

- `locator.press("Enter")` or `locator.press("Space")` focuses a native button but does not trigger its click handler in the preview iframe.
- The preview logs `Failed to execute 'observe' on 'MutationObserver'` even though the fragment contains no `MutationObserver`.
- Mouse activation, local state updates, Lucide icons, layout, and follow-up payload capture still work.

## Impact

- A preview-only automation limitation can be mistaken for a product accessibility defect.
- A host-injected console error can send investigation toward fragment code that does not contain the failing API.
- Treating either signal as a silent pass would also be unsafe; independent evidence is required.

## Trigger Conditions

- The official render helper wraps a fragment in a sandboxed iframe.
- Browser automation targets the wrapper rather than the final Codex inline host.
- A test bridge simulates `window.openai.sendFollowUpMessage` for payload inspection.
- Preview or browser infrastructure injects observers or utilities around the fragment.

## Root Cause

- The preview wrapper and final inline host are different execution surfaces.
- Keyboard-event synthesis and host-injected scripts may not cross the sandbox boundary exactly like user input in the final conversation surface.
- Console entries may originate from preview infrastructure rather than the fragment.

## Investigation Trail

1. Confirmed four labeled native buttons and four Lucide icons in the accessibility snapshot.
2. Confirmed synthetic keyboard operations acquired focus but did not activate the target inside the preview sandbox.
3. Confirmed normal click activation changed `aria-pressed` and detail content.
4. Captured the exact follow-up payload through a test bridge attached to the preview iframe.
5. Measured exact 736px and 320px inner widths with no horizontal overflow.
6. Searched the source fragment and confirmed it did not contain `MutationObserver`, network calls, or direct repository actions.

## Resolution

- Keep native semantic controls, native tab order, and visible focus styles.
- Validate local selection and primary action through direct operation and exact state or payload evidence.
- Attribute preview errors only after verifying that the fragment does not contain the reported API.
- Record the automation gap as residual risk and use the final inline result as the host-level smoke check.

## Prevention / Guardrails

- Do not add custom keyboard handlers to native buttons solely to satisfy a preview automation quirk; this can create duplicate activation in the real host.
- Do not ignore missing interaction evidence; triangulate semantics, focus, state changes, payload capture, screenshots, and source review.
- Keep the complete Markdown result and manual next command available outside the interactive fragment.
- Re-run the official skill instructions when plugin behavior changes instead of copying version-specific preview assumptions into repository contracts.

## Related Docs

- [Interactive skill outputs change](../change/2026-07-15_interactive-skill-outputs.md)
- [Visual output intake](../intake/2026-07-15_visual-output-components.md)
- [m-autoflow feature](../features/m-autoflow-workflow.md)
- [m-autoflow requirements](../requirements/m-autoflow-skill.md)
- [m-autoflow spec](../specs/m-autoflow-skill.md)
