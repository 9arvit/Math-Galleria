# Math Galleria — Pretty Math Graphs (Flask + Plotly)

A pretty, detailed Flask web app that lets users:
- Enter equations (Cartesian `y=f(x)`, Parametric `(x(t), y(t))`, Polar `r(θ)`)
- Or pick **presets** (Lissajous, Rose, Hypotrochoid, Harmanograph)
- Toggle theme, line width, markers, and sample size
- See **math trivia** for each plot
<img width="1470" height="804" alt="Screenshot 2025-08-22 at 7 10 19 PM" src="https://github.com/user-attachments/assets/a1099edd-5f0e-4ef3-9fe5-d7b4a099a677" />
<img width="1464" height="805" alt="Screenshot 2025-08-22 at 7 11 12 PM" src="https://github.com/user-attachments/assets/422336b7-4cdc-4b27-a8dc-fcda46a191b6" />



## Quickstart

```bash
# 1) Create venv (optional)
python -m venv .venv && source .venv/bin/activate  # (Windows: .venv\Scripts\activate)

# 2) Install deps
pip install -r requirements.txt

# 3) Run
python app.py
```

Open http://127.0.0.1:5050 and play!

## Usage Tips

- **Cartesian**: enter any SymPy-friendly expression in terms of `x`, e.g. `sin(x) + cos(2*x)`
- **Parametric**: use `t` in `x(t)` and `y(t)`, e.g. `sin(3*t+pi/2)`, `sin(5*t)`
- **Polar**: use `theta`, e.g. `cos(5*theta)`
- **Presets** are instant art + trivia.
- Errors are shown below the graph if your expression can't be parsed.

## File Structure

```
MathGalleria/
├── app.py
├── requirements.txt
├── README.md
├── templates/
│   └── index.html
└── static/
    ├── app.js
    └── style.css
```
