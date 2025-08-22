from flask import Flask, render_template, request, jsonify
import numpy as np
from math import gcd, pi
from fractions import Fraction
import sympy as sp

app = Flask(__name__)

# ---------- Helpers ----------
def safe_lambdify(vars_symbols, expr_str):
    """
    Convert a user expression string to a numpy-callable function safely.
    Allowed names: x, t, theta, sin, cos, tan, exp, log, sqrt, abs, asin, acos, atan,
    sinh, cosh, tanh, pi, E, GoldenRatio, sign, floor, ceiling, Mod, factorial, gamma.
    """
    allowed = {
        'sin': sp.sin, 'cos': sp.cos, 'tan': sp.tan,
        'exp': sp.exp, 'log': sp.log, 'sqrt': sp.sqrt, 'abs': sp.Abs,
        'asin': sp.asin, 'acos': sp.acos, 'atan': sp.atan,
        'sinh': sp.sinh, 'cosh': sp.cosh, 'tanh': sp.tanh,
        'pi': sp.pi, 'E': sp.E, 'GoldenRatio': sp.GoldenRatio,
        'sign': sp.sign, 'floor': sp.floor, 'ceiling': sp.ceiling,
        'Mod': sp.Mod, 'factorial': sp.factorial, 'gamma': sp.gamma
    }
    try:
        expr = sp.sympify(expr_str, locals=allowed)
    except Exception as e:
        raise ValueError(f"Could not parse expression: {e}")
    f = sp.lambdify(vars_symbols, expr, modules=[{'sqrt': np.sqrt, 'abs': np.abs}, 'numpy'])
    return f, expr

def lcm(a, b):
    return abs(a*b) // gcd(int(a), int(b)) if a and b else 0

# Trivia builders
def trivia_lissajous(a, b):
    try:
        frac = Fraction(a, b).limit_denominator()
        p, q = abs(frac.numerator), abs(frac.denominator)
        closed = "closes after one full path" if (isinstance(a, (int, np.integer)) and isinstance(b, (int, np.integer))) else "often appears quasi-periodic unless a/b is rational"
        lobes = f"Horizontal lobes: {q}, Vertical lobes: {p} (for δ=π/2)" if p>0 and q>0 else ""
        return f"Lissajous with frequency ratio a:b = {a}:{b} ≈ {p}:{q}. The curve {closed}. {lobes}."
    except Exception:
        return f"Lissajous with frequency ratio a:b = {a}:{b}."
    
def trivia_rose(k):
    petals = None
    try:
        frac = Fraction(k).limit_denominator()
        num, den = abs(frac.numerator), abs(frac.denominator)
        kk = num/den
        if den == 1:  # integer
            petals = num if num % 2 == 1 else 2*num
        else:
            # For rational k = p/q, rose closes with q* (p if p odd else 2p) petals (informal)
            petals = None
    except Exception:
        pass
    base = f"Rose curve r = cos({k}·θ)."
    if petals:
        base += f" Number of petals: {petals}."
    base += " Roses close neatly when k is rational; for integer k, odd k gives k petals, even k gives 2k petals."
    return base

def trivia_hypotrochoid(R, r):
    loops = lcm(int(round(R)), int(round(r)))
    return f"Hypotrochoid with R≈{R:.2f}, r≈{r:.2f}. When R/r is rational the path closes; approximate loop count ~ LCM(⌊R⌉,⌊r⌉) = {loops}."

def numeric_stats(x, y):
    try:
        # Approx range ignoring NaNs/Infs
        mask = np.isfinite(x) & np.isfinite(y)
        if mask.sum() == 0: return "No finite points to summarize."
        xs, ys = x[mask], y[mask]
        return f"Approximate extents — x∈[{xs.min():.3g}, {xs.max():.3g}], y∈[{ys.min():.3g}, {ys.max():.3g}]. Points plotted: {mask.sum()}."
    except Exception:
        return ""

# ---------- Routes ----------
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/plot', methods=['POST'])
def api_plot():
    data = request.get_json(force=True)
    mode = data.get('mode', 'cartesian')
    theme = data.get('theme', 'light')
    lw = float(data.get('linewidth', 2.0))
    show_markers = bool(data.get('markers', False))

    traces = []
    layout = {
        "title": {"text": "Math Galleria", "x": 0.5},
        "xaxis": {"title": "x"},
        "yaxis": {"title": "y", "scaleanchor": "x", "scaleratio": 1},
        "paper_bgcolor": "#0b1220" if theme == "dark" else "white",
        "plot_bgcolor": "#0b1220" if theme == "dark" else "white",
        "font": {"color": "white" if theme == "dark" else "black"},
        "showlegend": False
    }
    trivia = []
    msg = None

    try:
        if data.get('preset') == 'lissajous':
            a = float(data.get('a', 3))
            b = float(data.get('b', 5))
            delta = float(data.get('delta', np.pi/2))
            t = np.linspace(0, 2*np.pi, 6000)
            X = np.sin(a*t + delta); Y = np.sin(b*t)
            traces.append({"type":"scatter","mode":"lines+markers" if show_markers else "lines",
                           "x":X.tolist(),"y":Y.tolist(), "line":{"width": lw}})
            layout["title"]["text"] = f"Lissajous (a={a}, b={b}, δ={delta:.2f})"
            trivia.append(trivia_lissajous(a,b))
            trivia.append(numeric_stats(X,Y))

        elif data.get('preset') == 'rose':
            k = float(data.get('k', 3))
            th = np.linspace(0, 2*np.pi*max(6, int(abs(k))+2), 6000)
            r = np.cos(k*th)
            X = r*np.cos(th); Y = r*np.sin(th)
            traces.append({"type":"scatter","mode":"lines" if not show_markers else "lines+markers",
                           "x":X.tolist(),"y":Y.tolist(), "line":{"width": lw}})
            layout["title"]["text"] = f"Rose curve r = cos({k}·θ)"
            trivia.append(trivia_rose(k))
            trivia.append(numeric_stats(X,Y))

        elif data.get('preset') == 'hypotrochoid':
            R = float(data.get('R', 5))
            r = float(data.get('r', 3))
            d = float(data.get('d', 0.6*abs(r)))
            loops = lcm(max(int(abs(R)),1), max(int(abs(r)),1))
            theta = np.linspace(0, 2*np.pi*(loops if loops>0 else 20), 6000)
            X = (R - r) * np.cos(theta) + d * np.cos(((R - r)/r) * theta)
            Y = (R - r) * np.sin(theta) - d * np.sin(((R - r)/r) * theta)
            traces.append({"type":"scatter","mode":"lines" if not show_markers else "lines+markers",
                           "x":X.tolist(),"y":Y.tolist(), "line":{"width": lw}})
            layout["title"]["text"] = f"Hypotrochoid (R={R}, r={r}, d={d})"
            trivia.append(trivia_hypotrochoid(R,r))
            trivia.append(numeric_stats(X,Y))

        elif data.get('preset') == 'harmanograph':
            A1 = float(data.get('A1', 1.0)); f1 = float(data.get('f1', 2.0)); p1 = float(data.get('p1', 0.0)); d1 = float(data.get('d1', 0.004))
            A2 = float(data.get('A2', 1.0)); f2 = float(data.get('f2', 3.0)); p2 = float(data.get('p2', np.pi/2)); d2 = float(data.get('d2', 0.006))
            A3 = float(data.get('A3', 1.0)); f3 = float(data.get('f3', 2.5)); p3 = float(data.get('p3', np.pi/4)); d3 = float(data.get('d3', 0.005))
            A4 = float(data.get('A4', 1.0)); f4 = float(data.get('f4', 3.5)); p4 = float(data.get('p4', np.pi/3)); d4 = float(data.get('d4', 0.007))
            t = np.linspace(0, 100, 80000)
            X = (A1*np.sin(f1*t + p1)*np.exp(-d1*t) + A2*np.sin(f2*t + p2)*np.exp(-d2*t))
            Y = (A3*np.sin(f3*t + p3)*np.exp(-d3*t) + A4*np.sin(f4*t + p4)*np.exp(-d4*t))
            traces.append({"type":"scatter","mode":"lines","x":X.tolist(),"y":Y.tolist(), "line":{"width": 1 if lw<1 else lw}})
            layout["title"]["text"] = "Harmanograph"
            trivia.append("Harmanographs simulate coupled damped pendulums; small frequency differences create striking beats and envelopes.")
            trivia.append(numeric_stats(X,Y))

        else:
            # Free modes
            if mode == 'cartesian':
                expr = data.get('y_expr', 'sin(x)')
                xmin = float(data.get('xmin', -10)); xmax = float(data.get('xmax', 10))
                n = min(max(int(data.get('n', 2000)), 200), 20000)
                x = sp.symbols('x')
                f, _ = safe_lambdify([x], expr)
                X = np.linspace(xmin, xmax, n); 
                Y = f(X)
                traces.append({"type":"scatter","mode":"lines" if not show_markers else "lines+markers",
                               "x":X.tolist(),"y":np.array(Y).tolist(), "line":{"width": lw}})
                layout["title"]["text"] = f"y = {expr}"
                trivia.append(numeric_stats(X, np.array(Y)))

            elif mode == 'parametric':
                t = sp.symbols('t')
                x_expr = data.get('x_expr', 'sin(3*t+pi/2)')
                y_expr = data.get('y_expr', 'sin(5*t)')
                tmin = float(data.get('tmin', 0)); tmax = float(data.get('tmax', 2*np.pi))
                n = min(max(int(data.get('n', 6000)), 500), 60000)
                fx, _ = safe_lambdify([t], x_expr); fy, _ = safe_lambdify([t], y_expr)
                T = np.linspace(tmin, tmax, n)
                X = fx(T); Y = fy(T)
                traces.append({"type":"scatter","mode":"lines" if not show_markers else "lines+markers",
                               "x":np.array(X).tolist(),"y":np.array(Y).tolist(), "line":{"width": lw}})
                layout["title"]["text"] = f"x(t)={x_expr}, y(t)={y_expr}"
                trivia.append(numeric_stats(np.array(X), np.array(Y)))

            elif mode == 'polar':
                th = sp.symbols('theta')
                r_expr = data.get('r_expr', 'cos(3*theta)')
                thmin = float(data.get('thmin', 0)); thmax = float(data.get('thmax', 2*np.pi*4))
                n = min(max(int(data.get('n', 6000)), 500), 60000)
                fr, _ = safe_lambdify([th], r_expr)
                TH = np.linspace(thmin, thmax, n)
                R = fr(TH)
                X = np.array(R)*np.cos(TH); Y = np.array(R)*np.sin(TH)
                traces.append({"type":"scatter","mode":"lines" if not show_markers else "lines+markers",
                               "x":X.tolist(),"y":Y.tolist(), "line":{"width": lw}})
                layout["title"]["text"] = f"r(θ) = {r_expr}"
                trivia.append(numeric_stats(X, Y))

            else:
                msg = "Unknown plotting mode."
    except Exception as e:
        msg = f"Error while generating plot: {e}"

    return jsonify({
        "traces": traces,
        "layout": layout,
        "trivia": trivia,
        "message": msg
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
