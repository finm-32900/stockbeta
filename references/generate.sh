# This script generates the reference data for the LLM.
# It pulls documentation from various repositories and formats it into a format that can be used by the LLM.
# Make sure to first run homebrew install repomix
repomix --remote https://github.com/astral-sh/uv --include "docs/**" --style xml
mv ./repomix-output.xml ./references/uv.xml

repomix --remote https://github.com/pypa/hatch --include "docs/**" --style xml
mv ./repomix-output.xml ./references/hatch.xml
