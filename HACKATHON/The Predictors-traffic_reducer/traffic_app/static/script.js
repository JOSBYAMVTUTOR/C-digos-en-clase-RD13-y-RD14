document.addEventListener('DOMContentLoaded', () => {


    const inputs = {
        norte: document.getElementById('input-north'),
        sur: document.getElementById('input-south'),
        este: document.getElementById('input-east'),
        oeste: document.getElementById('input-west')
    };

    const valueDisplays = {
        norte: document.getElementById('val-north'),
        sur: document.getElementById('val-south'),
        este: document.getElementById('val-east'),
        oeste: document.getElementById('val-west')
    };

    const carsVisuals = {
        norte: document.getElementById('cars-north'),
        sur: document.getElementById('cars-south'),
        este: document.getElementById('cars-east'),
        oeste: document.getElementById('cars-west')
    };

    const lights = {
        0: document.getElementById('light-north'),
        1: document.getElementById('light-south'),
        2: document.getElementById('light-east'),
        3: document.getElementById('light-west')
    };

    const priorityResult = document.getElementById('priority-result');
    const liveToggle = document.getElementById('live-mode-toggle');
    const cvButton = document.getElementById('activate-cv');
    const cvStatus = document.getElementById('cv-toggle-status');
    const pedestrianCount = document.getElementById('pedestrian-count');
    const emergencyStatus = document.getElementById('emergency-status');

    let liveInterval = null;
    let cvModeActive = false;


    Object.keys(inputs).forEach(key => {
        inputs[key].addEventListener('input', (e) => {
            valueDisplays[key].textContent = e.target.value;
            updateVisualDensity(key, e.target.value);
            if (!cvModeActive) updatePrediction();
        });
    });

 
    liveToggle.addEventListener('change', () => {
        cvModeActive = liveToggle.checked;

        stopSimulation();

        Object.values(inputs).forEach(i => i.disabled = cvModeActive);

        if (cvButton) {
            cvButton.textContent = cvModeActive
                ? "DEACTIVATE TRAFFIC CONTROL"
                : "ACTIVATE TRAFFIC CONTROL";
            cvButton.classList.toggle('active', cvModeActive);
        }

        if (cvStatus) {
            cvStatus.textContent = cvModeActive ? "ON - AUTO CONTROL" : "OFF";
            cvStatus.style.color = cvModeActive ? "#4ade80" : "white";
        }

        updatePrediction();
    });

    if (cvButton) {
        cvButton.addEventListener('click', () => {
            liveToggle.checked = !liveToggle.checked;
            liveToggle.dispatchEvent(new Event('change'));
        });
    }

  
    function startSimulation() {
        stopSimulation();
        liveInterval = setInterval(fetchSimulation, 2000);
    }

    function stopSimulation() {
        if (liveInterval) clearInterval(liveInterval);
        liveInterval = null;
    }

    function fetchSimulation() {
        fetch('/simulate')
            .then(res => res.json())
            .then(data => {
                ['norte','sur','este','oeste'].forEach(k => {
                    inputs[k].value = data[k];
                    valueDisplays[k].textContent = data[k];
                    updateVisualDensity(k, data[k]);
                });
                updatePrediction();
            });
    }


    function updateVisualDensity(direction, value) {
        carsVisuals[direction].style.opacity = 0.2 + (value / 100) * 0.8;
    }

    function updatePrediction() {

        const payload = cvModeActive
            ? { live_mode: true }
            : {
                norte: inputs.norte.value,
                sur: inputs.sur.value,
                este: inputs.este.value,
                oeste: inputs.oeste.value
            };

        fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        })
        .then(res => res.json())
        .then(data => {
            if (data.error) return console.error(data.error);

            if (data.traffic_data) {
                ['norte','sur','este','oeste'].forEach(k => {
                    inputs[k].value = data.traffic_data[k];
                    valueDisplays[k].textContent = data.traffic_data[k];
                    updateVisualDensity(k, data.traffic_data[k]);
                });

                if (pedestrianCount)
                    pedestrianCount.textContent = data.traffic_data.pedestrians ?? 0;

                if (emergencyStatus) {
                    emergencyStatus.textContent = data.traffic_data.emergency ? "YES" : "NO";
                    emergencyStatus.style.color = data.traffic_data.emergency ? "red" : "lime";
                }
            }

            setLights(data.prediction);

            if (data.traffic_data?.emergency) {
                priorityResult.textContent = "EMERGENCY";
                priorityResult.style.color = "red";
            } else if (data.traffic_data?.pedestrians > 5) {
                priorityResult.textContent = "PEDESTRIANS";
                priorityResult.style.color = "yellow";
            }
        });
    }

    function setLights(winnerIndex) {
        document.querySelectorAll('.bulb.green').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.bulb.red').forEach(b => b.classList.add('active'));
        document.querySelectorAll('.road').forEach(r => r.classList.remove('active-road'));

        const names = ['NORTE','SUR','ESTE','OESTE'];
        const roads = ['.road.north','.road.south','.road.east','.road.west'];

        lights[winnerIndex]?.querySelector('.bulb.green').classList.add('active');
        lights[winnerIndex]?.querySelector('.bulb.red').classList.remove('active');
        document.querySelector(roads[winnerIndex])?.classList.add('active-road');

        priorityResult.textContent = names[winnerIndex];
        priorityResult.style.color = 'var(--green-light)';
    }

    updatePrediction();
});
