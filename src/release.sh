#!/bin/bash
# usage: [EP_EXPECT=key,...] [EP_SAVE=NAME] src/release.sh [REFERENCE]
#   Generates the tier tokens (lib/gen_tokens.py), builds every blueprint and the four templates from the sources in src/ (page definitions, layouts, macros, tokens,
#   shared parts), runs every check, and only when they all pass writes them to ../blueprints and ../custom_templates.
#   REFERENCE (optional, e.g. v1): also compare every render with src/baseline/REFERENCE; any difference stops the release,
#     except in the layouts EP_EXPECT names (the ones a change is meant to alter: listed, not failed).
#   EP_SAVE=NAME: after every check passed, keep this release's renders and blueprints as the reference NAME
#     (src/baseline/NAME and the golden data), without rendering them again.
#   The blueprints and templates are output only: change the sources and run this again.
set -eo pipefail
SRC="$(cd "$(dirname "$0")" && pwd)"; cd "$SRC"
unset EP_KEYS                                     # a release checks every layout, whatever the shell was left with
REF=$1; OUT="$SRC/build"; TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT                         # the second build, the previous build and the kept renders
T0=$SECONDS; TL=$SECONDS
lap() { echo "[$1: $((SECONDS - TL)) s, total $((SECONDS - T0)) s]"; TL=$SECONDS; }   # how long each step takes
KEYS=$(python3 lib/layouts.py)   # every layout, from the page definitions
build() {   # build DIR: the whole package, from the sources
  python3 lib/build.py "$1" "$KEYS"           # templates, blueprints, input scheme, shared parts, vocabulary, set id
}
[ -e "$OUT" ] && mv "$OUT" "$TMP/previous-build"
python3 lib/vocab_apply.py code >/dev/null
python3 lib/gen_tokens.py "$KEYS"                # the tier tokens: derived from the panel facts, measured ones fitted
lap tokens
build "$OUT"
build "$TMP/second"                              # the package is what the sources make: a second build must be identical
diff -r "$OUT" "$TMP/second" >/dev/null || { echo "build is not reproducible"; exit 1; }
lap builds
python3 lib/shared.py --lint "$OUT"
python3 lib/inputs_std.py --lint "$OUT"
python3 lib/unread.py "$OUT"                     # no input, text key or data key that nothing reads
python3 lib/coverage.py                          # every layout has a case for every kind of state (or a listed gap)
python3 lib/registry.py check                    # the registry: every reference, page and screen it names exists
# the checks print what fails (cases, state differences) and the comparison every differing render, then their totals
lap lints
export EP_RENDERS="$TMP/renders"                 # check.py keeps its renders; the comparison reuses them (one render per case)
EP_CT="$OUT/custom_templates" python3 check.py "$OUT" | { grep -v '^ok   ' || true; }
lap check
if [ -n "$REF" ]; then python3 lib/baseline.py cmp "$OUT" "$REF"; lap compare; fi
# the document's generated tables and values follow this build; then the document, the code comments and the package are linted
python3 lib/registry.py write ../docs/design-system.md "$OUT"
python3 lib/registry.py lint ../docs/design-system.md "$OUT"
python3 lib/rules.py lint ../docs/design-system.md   # the code cites rules the document has, and none of them changed unconfirmed
lap document
mkdir -p ../blueprints ../custom_templates
rm -f ../blueprints/epaper-blueprint-*.yaml     # generated output only: a renamed blueprint must not leave its old file behind
cp "$OUT"/epaper-blueprint-*.yaml ../blueprints/
cp "$OUT"/custom_templates/ep_*.jinja ../custom_templates/
python3 lib/pictures.py "$EP_RENDERS"            # the README's reference pictures: each blueprint's ordinary check case
echo "released to ../blueprints and ../custom_templates"
if [ -n "$EP_SAVE" ]; then python3 lib/baseline.py save "$OUT" "$EP_SAVE"; python3 lib/golden.py save "$OUT" "$EP_SAVE"; fi
