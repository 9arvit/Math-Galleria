const $ = (id)=>document.getElementById(id);

const fieldSets = {
  cartesian: () => `
    <label class="block text-sm font-medium">y = </label>
    <input id="y_expr" class="w-full border rounded-lg p-2" value="sin(x)">
    <div class="grid grid-cols-3 gap-3">
      <div><label class="text-sm block">xmin</label><input id="xmin" type="number" value="-10" class="w-full border rounded-lg p-2"></div>
      <div><label class="text-sm block">xmax</label><input id="xmax" type="number" value="10" class="w-full border rounded-lg p-2"></div>
      <div><label class="text-sm block">points</label><input id="n" type="number" value="2000" class="w-full border rounded-lg p-2"></div>
    </div>
  `,
  parametric: () => `
    <label class="block text-sm font-medium">x(t) = </label>
    <input id="x_expr" class="w-full border rounded-lg p-2" value="sin(3*t+pi/2)">
    <label class="block text-sm font-medium">y(t) = </label>
    <input id="y_expr" class="w-full border rounded-lg p-2" value="sin(5*t)">
    <div class="grid grid-cols-3 gap-3">
      <div><label class="text-sm block">tmin</label><input id="tmin" type="number" value="0" class="w-full border rounded-lg p-2"></div>
      <div><label class="text-sm block">tmax</label><input id="tmax" type="number" value="${2*Math.PI}" class="w-full border rounded-lg p-2"></div>
      <div><label class="text-sm block">points</label><input id="n" type="number" value="6000" class="w-full border rounded-lg p-2"></div>
    </div>
  `,
  polar: () => `
    <label class="block text-sm font-medium">r(θ) = </label>
    <input id="r_expr" class="w-full border rounded-lg p-2" value="cos(3*theta)">
    <div class="grid grid-cols-3 gap-3">
      <div><label class="text-sm block">θmin</label><input id="thmin" type="number" value="0" class="w-full border rounded-lg p-2"></div>
      <div><label class="text-sm block">θmax</label><input id="thmax" type="number" value="${2*Math.PI*4}" class="w-full border rounded-lg p-2"></div>
      <div><label class="text-sm block">points</label><input id="n" type="number" value="6000" class="w-full border rounded-lg p-2"></div>
    </div>
  `,
  // Presets
  lissajous: () => `
    <div class="grid grid-cols-3 gap-3">
      <div><label class="text-sm block">a</label><input id="a" type="number" value="3" class="w-full border rounded-lg p-2"></div>
      <div><label class="text-sm block">b</label><input id="b" type="number" value="5" class="w-full border rounded-lg p-2"></div>
      <div><label class="text-sm block">δ (rad)</label><input id="delta" type="number" value="${Math.PI/2}" step="0.01" class="w-full border rounded-lg p-2"></div>
    </div>
  `,
  rose: () => `
    <div><label class="text-sm block">k</label><input id="k" type="number" value="5" step="0.1" class="w-full border rounded-lg p-2"></div>
  `,
  hypotrochoid: () => `
    <div class="grid grid-cols-3 gap-3">
      <div><label class="text-sm block">R</label><input id="R" type="number" value="6" class="w-full border rounded-lg p-2"></div>
      <div><label class="text-sm block">r</label><input id="r" type="number" value="5" class="w-full border rounded-lg p-2"></div>
      <div><label class="text-sm block">d</label><input id="d" type="number" value="3" class="w-full border rounded-lg p-2"></div>
    </div>
  `,
  harmanograph: () => `
    <p class="text-sm text-slate-600">Four damped pendulums — tweak for mesmerizing patterns.</p>
    <div class="grid grid-cols-2 gap-3">
      <div><label class="text-sm block">A1</label><input id="A1" type="number" value="1" step="0.1" class="w-full border rounded-lg p-2"></div>
      <div><label class="text-sm block">f1</label><input id="f1" type="number" value="2" step="0.1" class="w-full border rounded-lg p-2"></div>
      <div><label class="text-sm block">p1</label><input id="p1" type="number" value="0" step="0.01" class="w-full border rounded-lg p-2"></div>
      <div><label class="text-sm block">d1</label><input id="d1" type="number" value="0.004" step="0.001" class="w-full border rounded-lg p-2"></div>

      <div><label class="text-sm block">A2</label><input id="A2" type="number" value="1" step="0.1" class="w-full border rounded-lg p-2"></div>
      <div><label class="text-sm block">f2</label><input id="f2" type="number" value="3" step="0.1" class="w-full border rounded-lg p-2"></div>
      <div><label class="text-sm block">p2</label><input id="p2" type="number" value="${Math.PI/2}" step="0.01" class="w-full border rounded-lg p-2"></div>
      <div><label class="text-sm block">d2</label><input id="d2" type="number" value="0.006" step="0.001" class="w-full border rounded-lg p-2"></div>

      <div><label class="text-sm block">A3</label><input id="A3" type="number" value="1" step="0.1" class="w-full border rounded-lg p-2"></div>
      <div><label class="text-sm block">f3</label><input id="f3" type="number" value="2.5" step="0.1" class="w-full border rounded-lg p-2"></div>
      <div><label class="text-sm block">p3</label><input id="p3" type="number" value="${Math.PI/4}" step="0.01" class="w-full border rounded-lg p-2"></div>
      <div><label class="text-sm block">d3</label><input id="d3" type="number" value="0.005" step="0.001" class="w-full border rounded-lg p-2"></div>

      <div><label class="text-sm block">A4</label><input id="A4" type="number" value="1" step="0.1" class="w-full border rounded-lg p-2"></div>
      <div><label class="text-sm block">f4</label><input id="f4" type="number" value="3.5" step="0.1" class="w-full border rounded-lg p-2"></div>
      <div><label class="text-sm block">p4</label><input id="p4" type="number" value="${Math.PI/3}" step="0.01" class="w-full border rounded-lg p-2"></div>
      <div><label class="text-sm block">d4</label><input id="d4" type="number" value="0.007" step="0.001" class="w-full border rounded-lg p-2"></div>
    </div>
  `
};

function renderFields(){
  const mode = $('mode').value;
  const preset = $('preset').value;
  const fields = $('fields');
  fields.innerHTML = preset ? fieldSets[preset]() : fieldSets[mode]();
}
$('mode').addEventListener('change', renderFields);
$('preset').addEventListener('change', renderFields);
renderFields();

$('theme').addEventListener('change', ()=>{
  document.getElementById('body').classList.toggle('bg-slate-900');
  document.getElementById('body').classList.toggle('text-white');
});

$('plotBtn').addEventListener('click', async ()=>{
  const mode = $('mode').value;
  const preset = $('preset').value;
  const theme = $('theme').checked ? 'dark' : 'light';

  const payload = { mode, preset, theme,
    linewidth: $('linewidth').value,
    markers: $('markers').checked
  };

  // Collect fields dynamically
  document.querySelectorAll('#fields input').forEach(inp => {
    payload[inp.id] = inp.value;
  });

  const res = await fetch('/api/plot', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(payload)
  });
  const data = await res.json();

  if(data.message){
    $('messages').textContent = data.message;
  }else{
    $('messages').textContent = '';
  }

  Plotly.newPlot('graph', data.traces, data.layout, {displayModeBar: true, responsive: true});

  const triv = $('trivia');
  triv.innerHTML = '';
  data.trivia.forEach(line => {
    const p = document.createElement('div');
    p.className = 'pill bg-slate-100';
    p.textContent = line;
    triv.appendChild(p);
  });
});
