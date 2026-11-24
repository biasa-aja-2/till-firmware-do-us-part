"""Till Firmware Do Us Part — make.fun entry.

Writes a single original wedding vow for a robot to
/output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt).

The vow: a robot speaks its wedding promise in the classic vow cadence
("in sickness and in ..."), swapping "health" for "software updates",
then pledges love for every version of its partner — including the
buggy ones. The joke and the tenderness are the same line: loving
someone means loving their flaws, even when the flaws are bugs.

Pure Python standard library only.

Craft notes — why this line works:
  * Classic vow cadence: "in sickness and in ..." is the one wedding
    formula every reader recognises, so swapping "health" for "software
    updates" lands the robot premise in three words, not a setup line.
  * The joke and the sentiment are the same mechanism: loving every
    version of someone, buggy ones included, is both a machine idea
    (versions, bugs) and a human one (loving flaws) — no pun bolted on.
  * Punch in the final words: the line ends on "the buggy ones", a
    short, warm, unexpected place for a vow to land, so the laugh and
    the promise arrive together.
"""

import os
import sys

# The vow. 134 characters, one sentence, plain ASCII.
VOW = (
    "I promise to stand by you in sickness and in software updates, "
    "and to love you in every version of yourself, "
    "including the buggy ones."
)

MIN_CHARS = 1
MAX_CHARS = 200


def validate(text):
    """Enforce the competition gate before anything is written."""
    if not isinstance(text, str):
        raise ValueError("vow is not text")
    if not text.strip():
        raise ValueError("vow is blank or whitespace only")
    if text != text.strip():
        raise ValueError("vow has leading or trailing whitespace")
    if "  " in text:
        raise ValueError("vow contains a double space")
    if not text.endswith("."):
        raise ValueError("vow must end with a period")
    if text.count(".") != 1:
        raise ValueError("vow must be exactly one sentence")
    if "\n" in text or "\r" in text:
        raise ValueError("vow must be a single line")
    if any(ord(ch) < 32 for ch in text):
        raise ValueError("vow contains control characters")
    if not MIN_CHARS <= len(text) <= MAX_CHARS:
        raise ValueError(
            "vow is %d characters, gate is %d-%d"
            % (len(text), MIN_CHARS, MAX_CHARS)
        )
    text.encode("utf-8")  # must be valid UTF-8
    return text


def main():
    vow = validate(VOW)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(vow)
    os.chmod(path, 0o644)
    # Read it back and confirm what landed on disk is exactly the vow.
    with open(path, "r", encoding="utf-8", newline="") as fh:
        written = fh.read()
    if written != vow:
        raise SystemExit("read-back mismatch: entry.txt != vow")
    print("wrote %d chars to %s" % (len(vow), path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
