const $ = id => document.getElementById(id);
const ns = 'http://www.w3.org/2000/svg';
let run, time = 0, playing = false, previous, robot, trail, serial = 0;
function svg(tag, attrs, parent = $('map')) {
  const el = document.createElementNS(ns, tag);
  for (const [key, value] of Object.entries(attrs)) el.setAttribute(key, value);
  parent.append(el); return el;
}
function stop() { playing = false; $('play').textContent = 'Play'; previous = undefined; }
function renderMap() {
  const s = run.scenario, [w,h] = s.world_size_m;
  $('map').replaceChildren(); $('map').setAttribute('viewBox', `-0.5 -0.5 ${w+1} ${h+1}`);
  const group = svg('g', {transform:`translate(0 ${h}) scale(1 -1)`});
  for(let i=0;i<=10;i++) {
    svg('line',{x1:w*i/10,y1:0,x2:w*i/10,y2:h,stroke:'#27382d','stroke-width':0.015},group);
    svg('line',{x1:0,y1:h*i/10,x2:w,y2:h*i/10,stroke:'#27382d','stroke-width':0.015},group);
  }
  for(const o of s.obstacles) svg('rect',{x:o.x_m,y:o.y_m,width:o.width_m,height:o.height_m,fill:'#617467',rx:0.04},group);
  svg('circle',{cx:s.goal_m[0],cy:s.goal_m[1],r:s.goal_tolerance_m,fill:'#efc67c','fill-opacity':0.25,stroke:'#efc67c','stroke-width':0.035},group);
  svg('polyline',{points:run.trace.map(p=>p.position_m.join(',')).join(' '),fill:'none',stroke:'#55755d','stroke-width':0.04,'stroke-dasharray':'0.1 0.1'},group);
  trail = svg('polyline',{fill:'none',stroke:'#b5f5c6','stroke-width':0.055},group);
  robot = svg('circle',{r:s.robot_radius_m,fill:'#b5f5c6',stroke:'#effff2','stroke-width':0.03},group);
}
function seek(value) {
  if(!run) return;
  const trace=run.trace, end=trace.at(-1).t_s;
  time=Math.min(end, Math.max(0,Number(value)));
  let lo=0, hi=trace.length-1;
  while(lo<hi){const mid=Math.ceil((lo+hi)/2);if(trace[mid].t_s<=time)lo=mid;else hi=mid-1;}
  const a=trace[lo], b=trace[Math.min(lo+1,trace.length-1)];
  const f=b.t_s===a.t_s?0:(time-a.t_s)/(b.t_s-a.t_s);
  const pos=a.position_m.map((v,i)=>v+(b.position_m[i]-v)*f);
  robot.setAttribute('cx',pos[0]);robot.setAttribute('cy',pos[1]);
  robot.setAttribute('fill',run.events.some(e=>e.type==='collision'&&e.t_s<=time)?'#f1937f':'#b5f5c6');
  trail.setAttribute('points',[...trace.slice(0,lo+1).map(p=>p.position_m),pos].map(p=>p.join(',')).join(' '));
  $('timeline').value=time;$('clock').textContent=`${time.toFixed(2)} / ${end.toFixed(2)} s`;
}
function show(data, example) {
  stop();run=data.run;const m=data.metrics;
  $('run-name').textContent=run.run_id;
  $('source').textContent=example?'EXAMPLE FIXTURE':'IMPORTED TRACE';
  $('provenance').textContent=example?'This hand-authored fixture tests the replay interface. It is not a simulator result or an AI-discovered failure.':'This replay uses your imported trace. Its source and physical accuracy are determined by the simulator that produced it.';
  $('outcome').textContent=m.completed?'Goal reached':`${m.termination[0].toUpperCase()}${m.termination.slice(1)}`;
  $('metrics').replaceChildren();
  for(const [label,value] of [['Controller',run.controller_id],['Distance',`${m.distance_m.toFixed(2)} m`],['Elapsed',`${m.elapsed_s.toFixed(2)} s`],['Recorded collisions',m.recorded_collisions],['Samples',m.samples]]){
    const row=document.createElement('div'),dt=document.createElement('dt'),dd=document.createElement('dd');dt.textContent=label;dd.textContent=value;row.append(dt,dd);$('metrics').append(row);
  }
  $('events').replaceChildren();
  if(!run.events.length){const p=document.createElement('p');p.textContent='No events recorded in this trace.';$('events').append(p);}
  for(const event of [...run.events].sort((a,b)=>a.t_s-b.t_s)){
    const button=document.createElement('button');button.className='event';button.textContent=`${event.t_s.toFixed(2)} s · ${event.type.replaceAll('_',' ')}`;button.onclick=()=>{stop();seek(event.t_s);};$('events').append(button);
  }
  $('timeline').max=m.elapsed_s;$('timeline').disabled=m.elapsed_s===0;$('play').disabled=m.elapsed_s===0;
  renderMap();seek(0);
}
async function load(file) {
  const request=++serial;stop();$('error').hidden=true;
  try {
    if(file&&file.size>2000000)throw Error('Upload a JSON file smaller than 2 MB.');
    const response=await fetch(file?'/api/inspect':'/api/example',file?{method:'POST',headers:{'Content-Type':'application/json'},body:await file.text()}:{});
    const data=await response.json();if(!response.ok)throw Error(data.error||'Unable to load run');
    if(request===serial)show(data,!file);
  } catch(error){if(request===serial){$('error').textContent=error.message;$('error').hidden=false;}}
}
$('example').onclick=()=>load();
$('upload').onchange=event=>{if(event.target.files[0])load(event.target.files[0]);event.target.value='';};
$('timeline').oninput=event=>{stop();seek(event.target.value);};
$('play').onclick=()=>{if(playing){stop();return;}if(time>=run.trace.at(-1).t_s)seek(0);playing=true;previous=undefined;$('play').textContent='Pause';};
function tick(now){if(playing){if(previous!==undefined)seek(time+(now-previous)/1000);previous=now;if(time>=run.trace.at(-1).t_s)stop();}requestAnimationFrame(tick);}
requestAnimationFrame(tick);load();
