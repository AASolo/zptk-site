/* ЗПТК — общий скрипт сайта: меню, счётчики, тема, звук, цели Метрики. */
(function(){
  var root=document.documentElement;

  /* Мобильное меню */
  var b=document.getElementById('zBurger'), m=document.getElementById('zMnav');
  function setMenu(open){ if(!b||!m) return; m.hidden=!open; b.setAttribute('aria-expanded', open?'true':'false');
    b.querySelector('.z-ic-close').hidden=!open; b.querySelector('.z-ic-open').hidden=open; }
  if(b&&m){ b.addEventListener('click',function(){ setMenu(m.hidden); });
    Array.prototype.forEach.call(m.querySelectorAll('a'),function(a){ a.addEventListener('click',function(){ setMenu(false); }); });
    window.addEventListener('resize',function(){ if(window.innerWidth>1180) setMenu(false); }); }

  /* Тема день / вечер */
  function setTheme(t){root.classList.remove('z-day','z-night');root.classList.add('z-'+t);try{localStorage.setItem('zptk-theme',t)}catch(e){}}
  Array.prototype.forEach.call(document.querySelectorAll('[data-z="theme"]'),function(btn){btn.addEventListener('click',function(){setTheme(root.classList.contains('z-night')?'day':'night');});});

  /* Звук электричества */
  var snd=null;function eng(){if(!snd){snd=(function(){
var AC=window.AudioContext||window.webkitAudioContext;if(!AC){return {on:function(){},off:function(){}};}
var ctx=null,master=null,timer=null,noise=null;
function build(){
ctx=new AC();master=ctx.createGain();master.gain.value=0;
var comp=ctx.createDynamicsCompressor();master.connect(comp);comp.connect(ctx.destination);
var hum=ctx.createGain();hum.gain.value=0.55;hum.connect(master);
var lp=ctx.createBiquadFilter();lp.type='lowpass';lp.frequency.value=700;lp.connect(hum);
[[50,0.5],[100,0.42],[150,0.2],[200,0.12],[250,0.06],[300,0.05]].forEach(function(p){var o=ctx.createOscillator();o.type='sine';o.frequency.value=p[0];o.detune.value=(Math.random()-0.5)*6;var g=ctx.createGain();g.gain.value=p[1];o.connect(g);g.connect(lp);o.start();});
var saw=ctx.createOscillator();saw.type='sawtooth';saw.frequency.value=100;var bp=ctx.createBiquadFilter();bp.type='bandpass';bp.frequency.value=1200;bp.Q.value=0.8;var sg=ctx.createGain();sg.gain.value=0.035;saw.connect(bp);bp.connect(sg);sg.connect(master);saw.start();
var lfo=ctx.createOscillator();lfo.frequency.value=0.23;var lg=ctx.createGain();lg.gain.value=0.12;lfo.connect(lg);lg.connect(hum.gain);lfo.start();
var len=ctx.sampleRate*2;noise=ctx.createBuffer(1,len,ctx.sampleRate);var d=noise.getChannelData(0);for(var i=0;i<len;i++){d[i]=Math.random()*2-1;}
var hs=ctx.createBufferSource();hs.buffer=noise;hs.loop=true;var hf=ctx.createBiquadFilter();hf.type='highpass';hf.frequency.value=4000;var hg=ctx.createGain();hg.gain.value=0.012;hs.connect(hf);hf.connect(hg);hg.connect(master);hs.start();
}
function crackle(){
if(!ctx){return;}var t=ctx.currentTime+0.02,n=3+Math.floor(Math.random()*8);
for(var k=0;k<n;k++){var s=ctx.createBufferSource();s.buffer=noise;var f=ctx.createBiquadFilter();f.type='bandpass';f.frequency.value=2500+Math.random()*4000;f.Q.value=1.5;var g=ctx.createGain();var st=t+k*(0.01+Math.random()*0.05),dur=0.005+Math.random()*0.03,a=0.15+Math.random()*0.5;g.gain.setValueAtTime(0,st);g.gain.linearRampToValueAtTime(a,st+0.002);g.gain.exponentialRampToValueAtTime(0.0001,st+dur);s.connect(f);f.connect(g);g.connect(master);s.start(st,Math.random()*1.5,dur+0.02);}
if(Math.random()<0.25){var o=ctx.createOscillator();o.type='square';o.frequency.setValueAtTime(900+Math.random()*600,t);o.frequency.exponentialRampToValueAtTime(120,t+0.25);var of=ctx.createBiquadFilter();of.type='lowpass';of.frequency.value=3000;var og=ctx.createGain();og.gain.setValueAtTime(0.0001,t);og.gain.exponentialRampToValueAtTime(0.06,t+0.01);og.gain.exponentialRampToValueAtTime(0.0001,t+0.3);o.connect(of);of.connect(og);og.connect(master);o.start(t);o.stop(t+0.35);}
timer=setTimeout(crackle,1800+Math.random()*4500);
}
return {
on:function(){if(!ctx){build();}if(ctx.state==='suspended'){ctx.resume();}master.gain.cancelScheduledValues(ctx.currentTime);master.gain.setTargetAtTime(0.22,ctx.currentTime,0.4);clearTimeout(timer);timer=setTimeout(crackle,900);},
off:function(){if(!ctx){return;}clearTimeout(timer);master.gain.cancelScheduledValues(ctx.currentTime);master.gain.setTargetAtTime(0,ctx.currentTime,0.15);setTimeout(function(){if(ctx&&!(master.gain.value>0.01)){ctx.suspend();}},900);}
};
})();}return snd;}
  var btns=document.querySelectorAll('[data-z="sound"]');
  function setSound(on,save){root.classList.toggle('z-snd-on',on);Array.prototype.forEach.call(btns,function(x){x.setAttribute('aria-pressed',on?'true':'false');});if(on){eng().on();}else if(snd){snd.off();}if(save){try{localStorage.setItem('zptk-sound',on?'on':'off')}catch(e){}}}
  Array.prototype.forEach.call(btns,function(x){x.addEventListener('click',function(){setSound(!root.classList.contains('z-snd-on'),true);});});
  var pref=null;try{pref=localStorage.getItem('zptk-sound')}catch(e){}
  if(pref==='on'){var first=function(ev){if(ev.target.closest&&ev.target.closest('[data-z="sound"]'))return;document.removeEventListener('pointerdown',first,true);setSound(true,false);};document.addEventListener('pointerdown',first,true);}

  /* Цели Яндекс.Метрики: скачивание презентации и переходы в направления */
  function goal(name,params){ try{ if(window.ym&&window.ZPTK_YM){ window.ym(window.ZPTK_YM,'reachGoal',name,params||{}); } }catch(e){} }
  document.addEventListener('click',function(e){
    var a=e.target.closest&&e.target.closest('a'); if(!a) return;
    var href=a.getAttribute('href')||'';
    if(/\.pdf($|\?)/i.test(href)) goal('pdf_download',{file:href.split('/').pop()});
    else if(/napravleniya\//.test(href)) goal('direction_click',{direction:href.split('/').pop().replace('.html','')});
    else if(/^mailto:/.test(href)) goal('email_click');
    else if(/^tel:/.test(href)) goal('phone_click');
  });

  /* Счётчики цифр */
  var nums=document.querySelectorAll('[data-count]'); if(!nums.length) return;
  var reduce=false; try{ reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches; }catch(e){}
  if(reduce||!('IntersectionObserver' in window)) return;
  function fmt(n){ return String(n).replace(/\B(?=(\d{3})+(?!\d))/g,' '); }
  var io=new IntersectionObserver(function(es){ es.forEach(function(en){ if(!en.isIntersecting) return; io.unobserve(en.target);
    var el=en.target, to=+el.getAttribute('data-count'), start=null;
    function tick(t){ if(start===null) start=t; var p=Math.min(1,(t-start)/1800), k=1-Math.pow(1-p,3);
      el.textContent=fmt(Math.round(to*k)); if(p<1) requestAnimationFrame(tick); }
    requestAnimationFrame(tick); }); },{threshold:.4});
  Array.prototype.forEach.call(nums,function(el){ io.observe(el); });
})();

/* Подпись автора сайта */
(function(){
  try{console.log('%c⚡ ЗПТК %c сайт разработан kapa ','background:#008DD2;color:#fff;padding:4px 8px;border-radius:4px 0 0 4px;font-weight:600','background:#0A2A42;color:#3DB4F0;padding:4px 8px;border-radius:0 4px 4px 0');}catch(e){}
  var toast=null,hide=null;
  function show(){
    if(!toast){toast=document.createElement('div');toast.className='z-kapa';toast.setAttribute('role','status');
      toast.innerHTML='⚡ Сайт разработан <b>kapa</b>';document.body.appendChild(toast);}
    clearTimeout(hide);requestAnimationFrame(function(){toast.classList.add('on');});
    hide=setTimeout(function(){toast.classList.remove('on');},3500);
  }
  var t=document.querySelector('[data-zk]'),n=0,last=0;
  if(t){t.addEventListener('click',function(){var now=Date.now();n=(now-last<600)?n+1:1;last=now;if(n>=5){n=0;show();}});}
  var buf='';document.addEventListener('keydown',function(e){if(!e.key||e.key.length!==1)return;buf=(buf+e.key.toLowerCase()).slice(-4);if(buf==='kapa'||buf==='кфзф')show();});
})();
