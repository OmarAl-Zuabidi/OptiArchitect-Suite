# OptiArchitect

Interactive, bilingual (English / Arabic) toolkit for teaching Operations Research.

| Part | Topic | Methods |
|---|---|---|
| 1 | Linear Programming | Standard, Dual and Two-Phase Simplex; graphical method (2 variables) |
| 2 | Transportation & Assignment | North-West Corner, Least Cost, Vogel (VAM), MODI (u-v), Hungarian |
| 3 | Single-variable non-linear optimization | Golden Section, Fibonacci, Newton-Raphson, Secant (automatic derivatives) |

Every result is verified independently (constraint residuals, grid scan, supply/demand check),
and a built-in self-test reproduces the reference results.

## Install

```bash
pip install .                 # core (numpy only)
pip install ".[all]"          # + sympy, matplotlib, Arabic shaping, Streamlit web app
```

Extras: `nlp` (sympy), `plot` (matplotlib), `arabic` (arabic-reshaper, python-bidi), `web` (Streamlit), `all`.
Requires Python >= 3.10.

## Use

```bash
optiarchitect                    # interactive console (also: python -m optiarchitect)
optiarchitect --lang ar --part 2 # Arabic, open Part 2 directly
optiarchitect --selftest         # built-in verification suite
optiarchitect --detail           # show every tableau / MODI loop / iteration
optiarchitect-web                # browser interface (Streamlit)
```

Options of the console: `--lang {en,ar}`, `--part {1,2,3}`, `--no-plot`, `--detail`, `--shape-ar`, `--selftest`, `--version`.
Web deep links: `?lang=ar&page=part2`.

As a library:

```python
from optiarchitect import solve_lp, solve_transportation, hungarian, Objective

res = solve_lp([3, 5], [[1, 0], [0, 2], [3, 2]], [4, 12, 18], ["<="] * 3, "max")
print(res.status, res.z, res.x)        # optimal 36.0 [2. 6.]
```

## Layout

```
optiarchitect/
  cli.py         interactive bilingual console (entry point `optiarchitect`)
  app.py         Streamlit web interface        (entry point `optiarchitect-web`)
  messages.py    bilingual message table (single source of every text)
  examples.py    worked examples          selftest.py   verification suite
  config.py      numerical settings, version, author, licence
  core/          lp.py  transportation.py  assignment.py  nlp.py      (pure solvers)
  utils/         parser.py (safe formulas)  plot.py  formatters.py  text_fix.py
tests/           solver, console and web-interface tests
```

## Tests

```bash
pip install -e ".[all]"
python -m unittest discover -s tests -t . -v
```

## Citation

See `CITATION.cff`. Al-Zuabidi, O. A. M. (2026). *OptiArchitect: an interactive bilingual toolkit for
teaching operations research and optimization.* [(https://doi.org/10.5281/zenodo.23231207)]

## Licence

MIT - see `LICENSE`. Copyright (c) 2026 Omar Ahmed Mohammed Al-Zuabidi.
