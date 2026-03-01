from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from database import init_db, log_interaction, get_recent_logs
from utils import generate_product_module, generate_proposal_module, generate_impact_module

app = FastAPI(title="Rayeva AI – Full Assignment")

@app.on_event("startup")
async def startup_event():
    init_db()

HTML_PAGE = """<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rayeva AI – Sustainable Commerce</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.6.0/css/all.min.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
        body { font-family: 'Inter', system-ui, sans-serif; }
        .title-font { font-family: 'Space Grotesk', sans-serif; }
        .glass { background: rgba(255,255,255,0.07); backdrop-filter: blur(24px); }
        .card-hover { transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); }
        .card-hover:hover { transform: translateY(-12px) scale(1.02); box-shadow: 0 30px 60px -15px rgb(16 185 129 / 0.3); }
        .faq-answer { max-height: 0; overflow: hidden; transition: max-height 0.5s cubic-bezier(0.4, 0, 0.2, 1); }
        .faq-item.open .faq-answer { max-height: 400px; }
        .toast { animation: slideUp 0.4s ease forwards; }
        @keyframes slideUp { from { transform: translateY(80px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
    </style>
</head>
<body class="bg-zinc-950 text-zinc-100 min-h-screen">
<div class="max-w-7xl mx-auto p-6">
    <!-- Advanced Navbar -->
    <nav class="flex items-center justify-between mb-12 border-b border-zinc-800 pb-6">
        <div class="flex items-center gap-4">
            <div class="w-11 h-11 bg-gradient-to-br from-emerald-500 to-teal-400 rounded-3xl flex items-center justify-center text-3xl shadow-xl">🌱</div>
            <div>
                <h1 class="title-font text-4xl font-semibold tracking-tighter">rayeva</h1>
                <p class="text-emerald-400 text-sm -mt-1">Sustainable AI Commerce</p>
            </div>
        </div>
        <div class="flex items-center gap-6">
            <select id="model-select" class="bg-zinc-900 border border-zinc-700 rounded-2xl px-5 py-3 text-sm focus:outline-none focus:border-emerald-500">
                <option value="ml">ML-Powered (Local)</option>
            </select>
            <button onclick="toggleTheme()" id="theme-btn" class="w-11 h-11 flex items-center justify-center rounded-2xl bg-zinc-900 hover:bg-zinc-800 border border-zinc-700 transition-all">
                <i id="theme-icon" class="fas fa-moon text-xl"></i>
            </button>
        </div>
    </nav>

    <div class="text-center mb-16">
        <div class="inline-flex items-center gap-3 bg-emerald-900/50 text-emerald-400 px-6 py-2 rounded-3xl text-sm mb-4">
            <span class="w-2 h-2 bg-emerald-400 rounded-full animate-pulse"></span> LIVE IN KADAPA, ANDHRA PRADESH
        </div>
        <h2 class="title-font text-6xl font-bold tracking-tighter bg-gradient-to-r from-white via-emerald-300 to-teal-300 bg-clip-text text-transparent">AI for Sustainable Commerce</h2>
        <p class="mt-4 text-zinc-400 max-w-2xl mx-auto">Module 1–3 fully implemented • Module 4 WhatsApp Bot Simulation</p>
    </div>

    <!-- Tabs -->
    <div class="flex border-b border-zinc-800 mb-10 overflow-x-auto pb-1">
        <button onclick="switchTab(0)" id="tab0" class="tab-btn active px-10 py-5 font-medium border-b-4 border-emerald-500 text-emerald-400">Module 1</button>
        <button onclick="switchTab(1)" id="tab1" class="tab-btn px-10 py-5 font-medium border-b-4 border-transparent hover:text-white">Module 2</button>
        <button onclick="switchTab(2)" id="tab2" class="tab-btn px-10 py-5 font-medium border-b-4 border-transparent hover:text-white">Module 3</button>
        <button onclick="switchTab(3)" id="tab3" class="tab-btn px-10 py-5 font-medium border-b-4 border-transparent hover:text-white">Module 4</button>
    </div>

    <!-- Tab Contents -->
    <div id="tab-content-0" class="tab-content">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div class="glass rounded-3xl p-10 card-hover">
                <h3 class="text-3xl font-semibold mb-8 flex items-center gap-4"><i class="fas fa-tags text-emerald-400"></i>Module 1: Auto-Category &amp; Tags</h3>
                <textarea id="description" rows="7" class="w-full bg-zinc-900 border border-zinc-700 rounded-3xl px-7 py-6 focus:outline-none focus:border-emerald-500 text-lg" placeholder="bamboo spoon reusable eco kitchen"></textarea>
                <button onclick="runModule1()" class="mt-8 w-full bg-gradient-to-r from-emerald-500 to-teal-500 hover:brightness-110 py-6 rounded-3xl font-semibold text-xl">GENERATE CATALOG</button>
            </div>
            <div class="glass rounded-3xl p-10"><pre id="res1" class="bg-black/60 p-8 rounded-3xl overflow-auto max-h-[520px] text-emerald-200 font-mono text-base"></pre></div>
        </div>
    </div>

    <div id="tab-content-1" class="tab-content hidden">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div class="glass rounded-3xl p-10 card-hover">
                <h3 class="text-3xl font-semibold mb-8">Module 2: B2B Proposal Generator</h3>
                <input id="company" value="GreenMart Retail" class="w-full bg-zinc-900 border border-zinc-700 rounded-3xl px-7 py-6 mb-5 text-lg">
                <input id="budget" type="number" value="65000" class="w-full bg-zinc-900 border border-zinc-700 rounded-3xl px-7 py-6 text-lg">
                <button onclick="runModule2()" class="mt-8 w-full bg-gradient-to-r from-emerald-500 to-teal-500 hover:brightness-110 py-6 rounded-3xl font-semibold text-xl">GENERATE PROPOSAL</button>
            </div>
            <div class="glass rounded-3xl p-10"><pre id="res2" class="bg-black/60 p-8 rounded-3xl overflow-auto max-h-[520px] text-emerald-200 font-mono text-base"></pre><canvas id="budgetChart" class="mt-8"></canvas></div>
        </div>
    </div>

    <div id="tab-content-2" class="tab-content hidden">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div class="glass rounded-3xl p-10 card-hover">
                <h3 class="text-3xl font-semibold mb-8">Module 3: Impact Reporting</h3>
                <textarea id="order_summary" rows="7" class="w-full bg-zinc-900 border border-zinc-700 rounded-3xl px-7 py-6 focus:outline-none focus:border-emerald-500 text-lg" placeholder="Bamboo Cutlery Set x 8&#10;Compostable Box x 15"></textarea>
                <button onclick="runModule3()" class="mt-8 w-full bg-gradient-to-r from-emerald-500 to-teal-500 hover:brightness-110 py-6 rounded-3xl font-semibold text-xl">GENERATE IMPACT REPORT</button>
            </div>
            <div class="glass rounded-3xl p-10"><pre id="res3" class="bg-black/60 p-8 rounded-3xl overflow-auto max-h-[520px] text-emerald-200 font-mono text-base"></pre></div>
        </div>
    </div>

    <!-- Module 4 -->
    <div id="tab-content-3" class="tab-content hidden">
        <div class="glass rounded-3xl p-10">
            <div class="flex items-center justify-between mb-8">
                <div class="flex items-center gap-4">
                    <i class="fab fa-whatsapp text-5xl text-emerald-400"></i>
                    <h3 class="text-3xl font-semibold">Module 4: WhatsApp Support Bot</h3>
                </div>
                <div class="bg-red-900/40 border border-red-500 text-red-400 px-6 py-3 rounded-3xl text-sm font-medium">🚧 We are working on the WhatsApp bot</div>
            </div>

            <!-- FAQ -->
            <div class="mb-12">
                <h4 class="text-2xl font-semibold mb-6 flex items-center gap-3"><i class="fas fa-list-check"></i>10 Sample Questions (click to expand)</h4>
                <div id="faq-list" class="space-y-4"></div>
            </div>

            <!-- Live Chat -->
            <div>
                <h4 class="text-2xl font-semibold mb-6">Live Chat Simulation</h4>
                <div id="chat-log" class="bg-zinc-900 rounded-3xl h-96 p-7 overflow-auto mb-6 space-y-5"></div>
                <div class="flex gap-4">
                    <input id="wa_input" class="flex-1 bg-zinc-900 border border-zinc-700 rounded-3xl px-7 py-6 text-lg" placeholder="Type message (e.g. order status)">
                    <button onclick="sendWA()" class="bg-emerald-500 hover:bg-emerald-600 px-12 rounded-3xl font-semibold text-lg">SEND</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Logs -->
    <div class="mt-16 glass rounded-3xl p-10">
        <div class="flex justify-between items-center mb-8">
            <h3 class="text-3xl font-semibold">Audit Logs</h3>
            <button onclick="loadLogs()" class="px-8 py-3 bg-zinc-800 hover:bg-zinc-700 rounded-3xl text-sm flex items-center gap-3"><i class="fas fa-sync"></i> Refresh Logs</button>
        </div>
        <div id="logs" class="space-y-4 max-h-80 overflow-auto"></div>
    </div>
</div>

<script>
let currentTab = 0;
const faqs = [
    {q:"What is my order status?",a:"Order #ORD456 shipped 28 Feb. Expected 4 Mar."},
    {q:"How do I return a product?",a:"30-day return. Print label from dashboard."},
    {q:"What is your refund policy?",a:"Full refund in 7 days if unused. Escalated."},
    {q:"Do you ship internationally?",a:"Yes to 12 countries. 8-12 days delivery."},
    {q:"Are products plastic-free?",a:"100% plastic-free or compostable."},
    {q:"Delivery time in India?",a:"Kadapa: 2-4 days. Rest India: 5-7 days."},
    {q:"Can I track order?",a:"Track link sent on WhatsApp & email."},
    {q:"Payment methods?",a:"UPI, Cards, Wallets, COD."},
    {q:"Warranty on products?",a:"6-month replacement warranty."},
    {q:"Contact human support?",a:"Reply HUMAN or call +91-9876543210."}
];

function loadFAQs() {
    let html = '';
    faqs.forEach((f,i) => {
        html += `<div class="faq-item glass rounded-3xl border border-zinc-700 cursor-pointer overflow-hidden" onclick="this.classList.toggle('open')">
            <div class="px-8 py-6 flex justify-between items-center">
                <span class="font-medium">${f.q}</span>
                <i class="fas fa-chevron-down transition-transform"></i>
            </div>
            <div class="faq-answer px-8 pb-6 text-emerald-300 border-t border-zinc-700">${f.a}</div>
        </div>`;
    });
    document.getElementById('faq-list').innerHTML = html;
}

function switchTab(n) {
    document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
    document.getElementById(`tab-content-${n}`).classList.remove('hidden');
    document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active','border-emerald-500','text-emerald-400'));
    document.getElementById(`tab${n}`).classList.add('active','border-emerald-500','text-emerald-400');
    currentTab = n;
}

async function runModule1() {
    const form = new FormData(); form.append('description', document.getElementById('description').value);
    const res = await fetch('/module1', {method:'POST', body:form});
    const data = await res.json();
    document.getElementById('res1').textContent = JSON.stringify(data, null, 2);
    loadLogs();
}

async function runModule2() {
    const form = new FormData(); 
    form.append('company', document.getElementById('company').value);
    form.append('budget', document.getElementById('budget').value);
    const res = await fetch('/module2', {method:'POST', body:form});
    const data = await res.json();
    document.getElementById('res2').textContent = JSON.stringify(data, null, 2);
    if (data.recommended_products) drawChart(data);
    loadLogs();
}

async function runModule3() {
    const form = new FormData(); form.append('order_summary', document.getElementById('order_summary').value);
    const res = await fetch('/module3', {method:'POST', body:form});
    const data = await res.json();
    document.getElementById('res3').textContent = JSON.stringify(data, null, 2);
    loadLogs();
}

function drawChart(data) {
    const ctx = document.getElementById('budgetChart');
    if (window.myChart) window.myChart.destroy();
    window.myChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: data.recommended_products.map(p => p.name.substring(0,18)),
            datasets: [{ data: data.recommended_products.map(p => p.quantity * p.unit_cost), backgroundColor: ['#10b981','#14b8a6','#22d3ee'] }]
        },
        options: { cutout: '72%', plugins: { legend: { labels: { color: '#d1fae5' } } } }
    });
}

function appendChat(sender, text) {
    const div = document.createElement('div');
    div.className = `flex ${sender==='You' ? 'justify-end' : 'justify-start'}`;
    div.innerHTML = `<div class="${sender==='You' ? 'bg-emerald-600' : 'bg-zinc-800'} max-w-[80%] rounded-3xl px-6 py-4">${text}</div>`;
    document.getElementById('chat-log').appendChild(div);
    div.scrollIntoView({behavior:'smooth'});
}

function getBotReply(msg) {
    msg = msg.toLowerCase();
    if (msg.includes('status') || msg.includes('order')) return 'Your order #ORD456 was shipped on 28 Feb 2025. Expected: 4 Mar.';
    if (msg.includes('return')) return 'Returns accepted within 30 days. Print label from dashboard.';
    if (msg.includes('refund')) {
        appendChat('System', '🚨 ESCALATED TO HUMAN SUPPORT (Ticket #SUP789)');
        return 'Refund request logged. Team will contact you in 2 hours.';
    }
    return 'Thank you! How else can I assist with your sustainable order?';
}

function sendWA() {
    let msg = document.getElementById('wa_input').value.trim();
    if (!msg) return;
    appendChat('You', msg);
    setTimeout(() => appendChat('Bot', getBotReply(msg)), 600);
    document.getElementById('wa_input').value = '';
    loadLogs();
}

async function loadLogs() {
    const res = await fetch('/logs');
    const logs = await res.json();
    let html = '';
    logs.forEach(l => {
        html += `<div class="glass rounded-3xl p-6 text-xs"><div class="flex justify-between text-emerald-400 mb-2"><span>${l[0]}</span><span class="font-mono">${l[1]}</span></div></div>`;
    });
    document.getElementById('logs').innerHTML = html || '<p class="text-zinc-500 text-center py-12">No logs yet</p>';
}

function toggleTheme() {
    document.documentElement.classList.toggle('dark');
    const icon = document.getElementById('theme-icon');
    icon.classList.toggle('fa-moon');
    icon.classList.toggle('fa-sun');
}

window.onload = () => {
    loadFAQs();
    loadLogs();
    switchTab(0);
    document.getElementById('chat-log').innerHTML = '<div class="text-center py-20 text-emerald-400">WhatsApp simulation ready – type above</div>';
    document.documentElement.classList.add('dark');
};
</script>
</body></html>"""

@app.get("/", response_class=HTMLResponse)
async def home():
    return HTML_PAGE

@app.post("/module1")
async def module1(request: Request):
    form = await request.form()
    description = form.get("description", "")
    result = generate_product_module(description)
    log_interaction("catalog", {"description": description}, result)
    return result

@app.post("/module2")
async def module2(request: Request):
    form = await request.form()
    company = form.get("company", "")
    try:
        budget = float(form.get("budget", 0))
    except:
        budget = 0
    result = generate_proposal_module(company, budget)
    log_interaction("proposal", {"company": company, "budget": budget}, result)
    return result

@app.post("/module3")
async def module3(request: Request):
    form = await request.form()
    order_summary = form.get("order_summary", "")
    result = generate_impact_module(order_summary)
    log_interaction("impact", {"order_summary": order_summary}, result)
    return result

@app.get("/logs")
async def api_logs():
    return get_recent_logs()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
