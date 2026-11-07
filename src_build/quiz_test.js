const {chromium, devices}=require('playwright');
(async()=>{const b=await chromium.launch();const ctx=await b.newContext({...devices['iPhone 13']});const p=await ctx.newPage();const e=[];p.on('pageerror',x=>e.push(x.message));
await p.goto('file://'+process.cwd()+'/slova-test.html');
await p.click('[data-tab=texts]'); await p.click('[data-g=lvl][data-v=B1]'); await p.click('.tcard >> nth=0');
console.log(await p.textContent('h1'), !!(await p.$('#quizTx')));
await p.click('#quizTx'); await p.click('#tqTr'); await p.screenshot({path:'q1.png'});
for(let i=0;i<6;i++){ await p.click('.opt >> nth='+(i%4)); if(i===0) await p.screenshot({path:'q2.png'}); await p.click('#tqNext'); }
console.log((await p.textContent('.res')).replace(/\s+/g,' ')); await p.screenshot({path:'q3.png',fullPage:true});
await p.click('#tqList'); console.log('badge:', await p.textContent('.tcard .meta'));
console.log('overflow', await p.evaluate(()=>document.documentElement.scrollWidth-innerWidth));
console.log(e); await b.close();})();
