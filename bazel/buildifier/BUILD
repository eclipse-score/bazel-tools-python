load("@buildifier_prebuilt//:rules.bzl", "buildifier")

BUILDIFIER_EXCLUDE_PATTERNS = [
    "./.git/*",
    "./.tox/*",
]

buildifier(
    name = "check",
    exclude_patterns = BUILDIFIER_EXCLUDE_PATTERNS,
    lint_mode = "warn",
    lint_warnings = ["all"],
    mode = "diff",
)

buildifier(
    name = "fix",
    exclude_patterns = BUILDIFIER_EXCLUDE_PATTERNS,
    lint_mode = "fix",
    lint_warnings = ["all"],
    mode = "fix",
)
