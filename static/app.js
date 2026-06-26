document.addEventListener('DOMContentLoaded', () => {
    // ─── DOM refs ──────────────────────────────────
    const uploadZone    = document.getElementById('uploadZone');
    const fileInput     = document.getElementById('fileInput');
    const preview       = document.getElementById('preview');
    const placeholder   = document.getElementById('uploadPlaceholder');
    const browseBtn     = document.getElementById('browseBtn');
    const sampleBtn     = document.getElementById('sampleBtn');
    const analyzeBtn    = document.getElementById('analyzeBtn');
    const btnText       = document.getElementById('analyzeBtnText');
    const spinner       = document.getElementById('analyzeSpinner');
    const slidesSection = document.getElementById('slidesSection');

    let currentFile = null;
    let colorMap = {};

    // ─── Load colors on page load ──────────────────
    fetch('/api/colors').then(r => r.json()).then(c => {
        colorMap = c;
        renderLegend(c);
    }).catch(() => {});

    // ─── File Handling ─────────────────────────────
    browseBtn.addEventListener('click', e => { e.stopPropagation(); fileInput.click(); });
    sampleBtn.addEventListener('click', async e => {
        e.stopPropagation();
        sampleBtn.textContent = '⏳ Loading…';
        sampleBtn.disabled = true;
        try {
            const res = await fetch('/api/sample');
            if (!res.ok) throw new Error('Failed to load sample');
            const blob = await res.blob();
            loadFile(new File([blob], 'eurosat_sample.jpg', { type: 'image/jpeg' }));
        } catch (err) {
            alert('Could not load sample. Make sure training was run first.');
        } finally {
            sampleBtn.textContent = '🎲 Load Random EuroSAT Sample';
            sampleBtn.disabled = false;
        }
    });

    uploadZone.addEventListener('click', e => { if (!e.target.closest('button')) fileInput.click(); });
    uploadZone.addEventListener('dragover', e => { e.preventDefault(); uploadZone.classList.add('dragover'); });
    uploadZone.addEventListener('dragleave', () => uploadZone.classList.remove('dragover'));
    uploadZone.addEventListener('drop', e => {
        e.preventDefault(); uploadZone.classList.remove('dragover');
        if (e.dataTransfer.files.length) loadFile(e.dataTransfer.files[0]);
    });
    fileInput.addEventListener('change', () => { if (fileInput.files.length) loadFile(fileInput.files[0]); });

    function loadFile(file) {
        if (!file.type.startsWith('image/')) return alert('Please select an image file.');
        currentFile = file;
        const reader = new FileReader();
        reader.onload = e => {
            preview.src = e.target.result;
            preview.hidden = false;
            placeholder.style.display = 'none';
            analyzeBtn.disabled = false;
        };
        reader.readAsDataURL(file);
    }

    // ─── Analyze ───────────────────────────────────
    analyzeBtn.addEventListener('click', async () => {
        if (!currentFile) return;
        btnText.textContent = '⏳ Analyzing…';
        spinner.hidden = false;
        analyzeBtn.disabled = true;

        try {
            const fd = new FormData();
            fd.append('file', currentFile);
            const res = await fetch('/api/predict', { method: 'POST', body: fd });
            const data = await res.json();
            if (!res.ok || data.error) throw new Error(data.error || 'Server error');
            renderResults(data);
        } catch (err) {
            alert('Error: ' + err.message);
        } finally {
            btnText.textContent = '🔬 Run Classification';
            spinner.hidden = true;
            analyzeBtn.disabled = false;
        }
    });

    // ─── Render Results ────────────────────────────
    function renderResults(data) {
        slidesSection.hidden = false;
        setTimeout(() => slidesSection.scrollIntoView({ behavior: 'smooth', block: 'start' }), 100);

        // CNN Slide
        fillSlide('cnn', data.resnet, 'bar-blue');
        // BDH Slide
        fillSlide('bdh', data.baby_dragon, 'bar-purple');
        // Live Compare
        renderLiveCompare(data);
        // Activate first tab
        document.querySelector('.tab[data-tab="cnn"]').click();
    }

    function fillSlide(prefix, result, barClass) {
        const rgb = result.color || [128,128,128];
        const cssColor = `rgb(${rgb[0]},${rgb[1]},${rgb[2]})`;

        document.getElementById(`${prefix}-color`).style.backgroundColor = cssColor;
        document.getElementById(`${prefix}-class`).textContent = result.prediction;
        document.getElementById(`${prefix}-class`).style.color = cssColor;
        document.getElementById(`${prefix}-desc`).textContent = result.description || '';
        document.getElementById(`${prefix}-conf`).textContent = (result.confidence * 100).toFixed(2) + '%';
        document.getElementById(`${prefix}-time`).textContent = result.inference_ms + ' ms';

        // Show Grad-CAM heatmap
        const camImg = document.getElementById(`${prefix}-cam`);
        const camPlaceholder = document.getElementById(`${prefix}-cam-placeholder`);
        if (camImg && result.cam_image) {
            camImg.src = result.cam_image;
            camImg.hidden = false;
            if (camPlaceholder) camPlaceholder.hidden = true;
        }

        renderChart(`${prefix}-chart`, result.all_probs, barClass);
    }

    // Boost dim colors so they're visible on dark backgrounds
    function boostColor(rgb) {
        const [r,g,b] = rgb;
        const brightness = (r + g + b) / 3;
        if (brightness < 100) {
            const factor = 1.8;
            return [Math.min(255, Math.round(r * factor + 40)),
                    Math.min(255, Math.round(g * factor + 40)),
                    Math.min(255, Math.round(b * factor + 40))];
        }
        return rgb;
    }

    function renderChart(id, probs, barClass) {
        const el = document.getElementById(id);
        const sorted = Object.entries(probs).sort((a,b) => b[1] - a[1]);
        el.innerHTML = sorted.map(([name, val]) => {
            const rawRgb = colorMap[name] || [128,128,128];
            const rgb = boostColor(rawRgb);
            const color = `rgb(${rgb.join(',')})`;
            return `
                <div class="prob-row">
                    <span class="prob-name" style="color:${color};font-weight:600">${name}</span>
                    <div class="prob-color-dot" style="background:${color}"></div>
                    <div class="prob-bar-bg"><div class="prob-bar" data-w="${(val*100).toFixed(1)}" style="background:${color}"></div></div>
                    <span class="prob-pct" style="color:${color};font-weight:600">${(val*100).toFixed(1)}%</span>
                </div>`;
        }).join('');
        requestAnimationFrame(() => {
            el.querySelectorAll('.prob-bar').forEach(b => b.style.width = b.dataset.w + '%');
        });
    }

    function renderLiveCompare(data) {
        const r = data.resnet, b = data.baby_dragon;
        const rColor = `rgb(${(r.color||[59,130,246]).join(',')})`;
        const bColor = `rgb(${(b.color||[168,85,247]).join(',')})`;

        document.getElementById('liveCompare').innerHTML = `
            <div class="compare-card">
                <div class="compare-color-bar" style="background:${rColor}"></div>
                <h4>🧠 ResNet-18</h4>
                <div class="val" style="color:${rColor}">${r.prediction}</div>
                <div class="meta">${(r.confidence*100).toFixed(2)}% confidence · ${r.inference_ms} ms</div>
            </div>
            <div class="compare-card">
                <div class="compare-color-bar" style="background:${bColor}"></div>
                <h4>🐉 Baby Dragon Hatchling</h4>
                <div class="val" style="color:${bColor}">${b.prediction}</div>
                <div class="meta">${(b.confidence*100).toFixed(2)}% confidence · ${b.inference_ms} ms</div>
            </div>
        `;

        // Side-by-side Grad-CAM comparison
        const camCompare = document.getElementById('camCompare');
        if (camCompare) {
            let html = '';
            if (r.cam_image) {
                html += `<div class="cam-compare-card">
                    <h4>🧠 ResNet-18 Attention</h4>
                    <img src="${r.cam_image}" alt="ResNet Grad-CAM">
                    <div class="cam-pred" style="color:${rColor}">${r.prediction}</div>
                </div>`;
            }
            if (b.cam_image) {
                html += `<div class="cam-compare-card">
                    <h4>🐉 BDH Attention</h4>
                    <img src="${b.cam_image}" alt="BDH Grad-CAM">
                    <div class="cam-pred" style="color:${bColor}">${b.prediction}</div>
                </div>`;
            }
            if (html) camCompare.innerHTML = html;
        }
    }

    // ─── Tabs ──────────────────────────────────────
    document.querySelectorAll('.tab').forEach(tab => {
        tab.addEventListener('click', () => {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.slide').forEach(s => s.classList.remove('active'));
            tab.classList.add('active');
            document.getElementById('slide-' + tab.dataset.tab).classList.add('active');
        });
    });

    // ─── Land Cover Legend ─────────────────────────
    function renderLegend(colors) {
        const grid = document.getElementById('legendGrid');
        if (!grid) return;
        grid.innerHTML = Object.entries(colors).map(([name, rgb]) =>
            `<div class="legend-item">
                <div class="legend-swatch" style="background:rgb(${rgb.join(',')})"></div>
                <span>${name}</span>
            </div>`
        ).join('');
    }

    // ─── Load Training Metrics ─────────────────────
    fetch('/api/metrics').then(r => r.json()).then(data => {
        if (!data || !data.resnet) return;
        renderMetrics(data);
    }).catch(() => {});

    function renderMetrics(data) {
        const rows = [
            { label: 'Accuracy',       r: data.resnet.accuracy,          d: data.baby_dragon.accuracy,          pct: true,  higher: true },
            { label: 'Precision',      r: data.resnet.precision,         d: data.baby_dragon.precision,         pct: true,  higher: true },
            { label: 'Recall',         r: data.resnet.recall,            d: data.baby_dragon.recall,            pct: true,  higher: true },
            { label: 'F1-Score',       r: data.resnet.f1,                d: data.baby_dragon.f1,                pct: true,  higher: true },
            { label: 'Inference (ms)', r: data.resnet.inference_time_ms, d: data.baby_dragon.inference_time_ms, pct: false, higher: false },
            { label: 'Train Time (s)', r: data.resnet.train_time_s,      d: data.baby_dragon.train_time_s,      pct: false, higher: false },
            { label: 'Parameters',     r: data.resnet.parameters,        d: data.baby_dragon.parameters,        pct: false, higher: false },
        ];
        const tbody = document.getElementById('metricsBody');
        tbody.innerHTML = rows.map(row => {
            const fmt = v => row.pct ? (v*100).toFixed(2)+'%' : (typeof v==='number' && v > 9999 ? (v/1e6).toFixed(2)+'M' : v);
            const rWins = row.higher ? row.r >= row.d : row.r <= row.d;
            return `<tr>
                <td style="font-family:Inter;color:var(--text)">${row.label}</td>
                <td class="${rWins?'blue':''}">${fmt(row.r)}</td>
                <td class="${!rWins?'purple':''}">${fmt(row.d)}</td>
                <td class="winner">${rWins ? '🧠 ResNet' : '🐉 BDH'}</td>
            </tr>`;
        }).join('');
    }
});
