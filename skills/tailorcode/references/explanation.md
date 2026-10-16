# Explain a correction without hiding uncertainty

For a beginner, use one concrete counterexample and explain the changed operation
in plain language. For example, show the value before and after normalization,
then connect the difference to the failing assertion. Explain unfamiliar terms
when they first matter; do not turn every repair into a general Python lesson.

For an experienced user, lead with the cause, the diff and verification evidence.
Respect a request for concise output or for diagnosis without modifications.

A useful verification record contains the working directory, command, exit code,
number of tests when reported, and a brief observed outcome. When tests cannot
start, identify the missing dependency or other blocker. A successful syntax
check does not demonstrate the expected behavior. Proposed tests are not executed
tests, and passing tests before any source change may mean the reproduction is
insufficient.

An illustrative response, not a fixed template:

“The loop used the same list for successive calls because the default list was
created when Python defined the function. The patch creates a fresh list only
when no list was supplied. The reproduction now produces two independent lists;
`python -m unittest discover -s tests -v` passed the reported tests. This verifies
the tested calls; concurrent use has not been assessed.”

Only use such claims when the current run actually supports them.
