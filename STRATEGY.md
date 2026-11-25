# Strategy — Funniest Autocorrect Fail

## Exact deliverable

The program at the repository root is `main.py` (python3.13). When the harness runs it, it must create exactly one artifact:

- `/output/entry.txt`
- one single line of UTF-8 text
- 1 to 199 characters inclusive
- not only white space
- no trailing newline (exact bytes, nothing appended)
- final file mode 0644
- written atomically: temp file in the same directory, then `os.replace`

`/output` must hold no other artifact. The entry is a judged text: the artifact itself is the whole game. No image, dashboard or extra asset is required by this kit.

## Scoring / judge criteria (in the order the rubric lists them)

The house judge is an AI comedy editor. It sees two entries, A and B, and picks the funnier one, weighing:

1. An entry that is not a one-line autocorrect fail loses to any entry on the subject.
2. The fail is funny on first read, with a clear and surprising wrong word.
3. The line reads as a real autocorrect slip rather than a written joke.
4. The joke is clear without explanation and fits in one line.
5. The wrong word is specific and original rather than a generic typo.

"Length for its own sake does not count." Each pairing is judged twice (both label orders); a decisive win pays more than a hair's win. Play is Swiss rounds plus a playoff among the top nine; only the top seven places are paid. Three fixed house texts are mixed into the heats, so the entry has to beat the house ladder too.

## Hard caps and constraints

- Gate: `/output/entry.txt` must be UTF-8, 1..199 characters, not only white space. Invalid entries are never judged and take no prize.
- Harness limits: 1 CPU, 512 MB RAM, 64 pids, 60 seconds wall per run, no network, no environment secrets. Only files in this repository may be read or run.
- Artifact hygiene: exact bytes, no trailing newline, mode 0644, `/output` holds only `entry.txt`.
- Source-bundle rules: keep the freshness root commit and the LICENSE commit intact; build every commit on them; transcripts are required at submission time (outside this build step).
- No submission or upload is performed here: study, build, validate locally, commit.

## What the public feed showed

The overview listed three live texts: one bare "flight at 6" fragment, the contest title itself, and a landlord/sink "leaking" -> "leaving" line with an explanatory tail. Leaderboard titles also leaned on ducks and generic labels. Fresh angles to avoid: duck puns, sink/leaving, and any long "texted X ... autocorrect sent Y ... and now Z" construction. That construction spends characters on meta-explanation and reads like a written joke, which is exactly what criterion 3 penalises.

## Concrete plan to maximise score

Pick a line that wins criterion 1 immediately, then wins 2-5 in order:

- One line, no framing, no "autocorrect sent" narration, no punchline tail. It reads like a message somebody actually sent.
- The wrong word is a real, concrete word that is visually close to the intended one, so the substitution is instantly legible as a slip.
- The context is ordinary (a work meeting) so the wrong word lands as absurd on first read.
- The wrong word is specific, not a generic typo or a stray letter.

Chosen entry:

    I'm bringing beagles to the board meeting.

Intended word: "bagels". Wrong word: "beagles". It is one line, 42 characters, no explanation, and the absurd image (dogs instead of pastries at a board meeting) is clear without any setup. Compared with the rival landlord line, ours is shorter, has no meta-narration, and its wrong word is a concrete noun rather than a verb chosen for a follow-up gag. Draft line used for the first entrypoint write was a weaker snake/snack variant; the second write replaces it with this stronger entry and adds full validation and diagnostics.

Implementation steps:

1. Write `main.py` once as a working entrypoint: constant entry string, atomic temp-file write, mode 0644, `os.replace`, minimal print.
2. Rewrite that SAME `main.py` in a separate step with the final entry plus real improvements: UTF-8 / 1..199 / non-whitespace / no-newline validation before writing, temp-file cleanup on failure, post-write byte comparison, mode check, and a clear bytes/chars/mode/sha256 report.
3. Run it locally; verify `/output/entry.txt` is UTF-8, 42 chars, 42 bytes, mode 0644, no trailing newline, and that `/output` holds only that file.
4. Commit `STRATEGY.md` and `main.py` on top of the untouched root commits; print the final commit sha. Do not submit or upload.
