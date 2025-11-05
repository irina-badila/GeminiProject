# --- File Handling ---

# Defines the maximum number of characters to read from any single file.
# This prevents accidentally loading very large files into memory.
MAX_CHARS=10000

# --- Security & Workspace ---

# Defines the root directory for all file operations (read, write, list, run).
# This is a crucial security boundary that "jails" the AI agent,
# preventing it from accessing files outside this specific folder.
WORKING_DIR = "./calculator"

# --- Agent Control ---

# Sets the maximum number of back-and-forth cycles (model response -> function call)
# the agent can perform for a single prompt.
# This acts as a safety stop to prevent infinite loops.
MAX_ITERATIONS = 20