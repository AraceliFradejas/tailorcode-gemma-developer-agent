# Running the visual lab locally

The Streamlit app has three everyday examples: a zero price, shared shopping
baskets and an excluded final day. The price uses a recorded Codex correction;
the other two use handwritten reference corrections. No screen generates new
model responses.

## Start and stop

From the repository root:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m streamlit run app.py --server.address 127.0.0.1
```

Open the address printed by Streamlit, usually http://127.0.0.1:8501. Press Ctrl+C
in the server terminal to stop it. The public version is
https://tailorcode-corrige-y-aprende.streamlit.app/.

## Walkthrough

Choose one of the three visible options in the highlighted panel. Read the rule
and expected result before looking at the original/corrected behavior. The
“Understand the example” tab explains the cause and offers a small question.
“Check the correction” runs real acceptance tests; code and technical output
are optional details.

- **Price:** choose a free product, a nonzero recorded price, or a missing price.
  Only the missing value should select the fallback. The button runs three tests.
- **Baskets:** Ana and Luis start new lists. The original shares items, while the
  correction keeps them independent and preserves a supplied list. Three tests run.
- **Calendar:** water on even days within an inclusive period. Days 1 through 4
  should select 2 and 4. A single-day and an odd-final-day scenario clarify the
  boundary. Four original tests run.

The demo does not accept arbitrary Python to execute. Only known repository
examples run in temporary folders. This is a local test mechanism, not a secure
execution sandbox for visitor-supplied code.

## Downloads and authorship

Both skill ZIPs are built in memory from an explicit set of files. Codex includes
its interface metadata; Claude Code receives the portable instructions/reference.
Extract the `tailorcode` folder into `.agents/skills/` or `.claude/skills/` inside
the target project. The sidebar explains how to start a fresh conversation.
A shared footer identifies Araceli Fradejas Muñoz and links to her social profiles.

## Checks and operational issue

At release, 37 local tests passed. Streamlit AppTest exercised the three screens,
scenario changes, questions and actual acceptance-check buttons. Dependencies
passed `pip check`. Public checks and screenshots are recorded separately in
[the deployment report](publicacion-streamlit.md).

A live server started before a structural change held the old imported engine
and could not import `basket_trace`, although fresh-process checks passed.
Restarting Streamlit loaded the updated module. Restart the server after changes
to module structure; reloading the browser alone may not refresh imported modules.

## Language revision

The first walkthrough was too technical, so the design was changed to everyday
situations with optional code details. The public interface was subsequently
translated into English at the author's request. Original evidence records may
quote the earlier interface or prompts; those observations are not retroactively
translated into new experiments.
