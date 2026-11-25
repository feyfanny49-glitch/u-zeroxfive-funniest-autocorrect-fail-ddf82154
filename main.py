#!/usr/bin/env python3
"""Write the single judged text artifact for the autocorrect-fail contest.

Harness: python3.13, no network, no secrets, 60 s wall budget.
Deliverable: /output/entry.txt, UTF-8, 1..199 chars, one line, no trailing
newline, mode 0644, created atomically. Nothing else may remain in /output.
"""

import hashlib
import os
import tempfile

OUTPUT_DIR = "/output"
TARGET = "entry.txt"

# One natural line, no narration, no punchline tail. Intended "bagels";
# the autocorrect slip is "beagles". Concrete, surprising, instantly clear.
ENTRY = "I'm bringing beagles to the board meeting."


def validate(text: str) -> bytes:
    """Return the exact bytes to write, or raise before touching /output."""
    if not isinstance(text, str):
        raise TypeError("entry must be a string")
    if not (1 <= len(text) <= 199):
        raise ValueError(f"entry length {len(text)} outside 1..199")
    if text.strip() != text:
        raise ValueError("entry must not have leading or trailing whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be exactly one line")
    data = text.encode("utf-8")
    # Decode again so a bad encoding cannot slip through the gate.
    if data.decode("utf-8") != text:
        raise ValueError("entry is not clean UTF-8")
    return data


def prune_output(output_dir: str) -> None:
    """Keep only the required artifact in /output (files and symlinks)."""
    with os.scandir(output_dir) as it:
        for item in it:
            if item.name == TARGET:
                continue
            if item.is_file() or item.is_symlink():
                os.unlink(item.path)


def main() -> None:
    data = validate(ENTRY)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    target = os.path.join(OUTPUT_DIR, TARGET)

    fd, tmp = tempfile.mkstemp(prefix=".entry-", suffix=".tmp", dir=OUTPUT_DIR)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        # mkstemp creates 0600; the grader refuses that. Fix before the swap.
        os.chmod(tmp, 0o644)
        os.replace(tmp, target)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise

    prune_output(OUTPUT_DIR)

    # Verify the artifact as the grader will see it.
    with open(target, "rb") as f:
        written = f.read()
    if written != data:
        raise RuntimeError("artifact bytes differ from the intended entry")
    mode = os.stat(target).st_mode & 0o777
    if mode != 0o644:
        raise RuntimeError(f"artifact mode is {mode:04o}, expected 0644")
    if len(written.decode("utf-8")) != len(ENTRY):
        raise RuntimeError("artifact is not valid UTF-8 of the expected size")

    digest = hashlib.sha256(written).hexdigest()
    print(
        f"entry.txt: {len(written)} bytes, {len(ENTRY)} chars, "
        f"mode {mode:04o}, sha256 {digest}"
    )


if __name__ == "__main__":
    main()
