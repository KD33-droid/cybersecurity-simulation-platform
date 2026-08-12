function goModules(){
  window.location = "modules.html"
}

function startModule(){
  window.location = "loading.html"
}

async function checkLabStatus(){
  try{
    let r = await fetch("http://localhost:8000/lab-status")
    let d = await r.json()

    document.getElementById("labStatus").innerText =
      d.running ? "Running" : "Not Running"
  }catch{}
}

if(document.getElementById("labStatus")){
  checkLabStatus()
}

setInterval(()=>{
  let rpsEl = document.getElementById("rps")
  if(!rpsEl) return

  fetch("http://localhost:9000/metrics")
  .then(r=>r.json())
  .then(d=>{
    document.getElementById("rps").innerText = d.rps
    let s = document.getElementById("status")
    s.innerText = d.state
    s.className = d.state
  })
  .catch(()=>{})
},2000)

function stopLab(){
  fetch("http://localhost:8000/stop-ddos",{method:"POST"})
}
