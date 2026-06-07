function updateClock() {
  const now = new Date();
  const hour = now.getHours();
  const greeting = hour < 12 ? "Good morning" : hour < 17 ? "Good afternoon" : "Good evening";
  document.getElementById("greeting").textContent = greeting;
  document.getElementById("date-time").textContent = now.toLocaleDateString("en-US", {
    weekday: "long", month: "long", day: "numeric"
  }) + "  " + now.toLocaleTimeString("en-US", { hour: "numeric", minute: "2-digit" });
}

async function loadWeather() {
  const currentEl = document.getElementById("weather-current");
  const forecastEl = document.getElementById("weather-forecast");
  try {
    const res = await fetch("/api/weather");
    const data = await res.json();
    if (data.error) throw new Error(data.error);

    const c = data.current;
    currentEl.className = "";
    currentEl.innerHTML = `
      <div class="weather-main">
        <img src="https://openweathermap.org/img/wn/${c.icon}@2x.png" alt="${c.description}" />
        <div>
          <div class="weather-temp">${c.temp}&deg;F</div>
          <div class="weather-desc">${c.description}</div>
        </div>
      </div>
      <div class="weather-meta">Feels like ${c.feels_like}&deg; &middot; Humidity ${c.humidity}% &middot; ${data.location}</div>
    `;

    const hourlyEl = document.getElementById("weather-hourly");
    hourlyEl.innerHTML = data.hourly.map(h => `
      <div class="forecast-day">
        <div class="day-label">${h.time}</div>
        <img src="https://openweathermap.org/img/wn/${h.icon}.png" alt="${h.description}" />
        <div class="temps">${h.temp}&deg;</div>
      </div>
    `).join("");

    forecastEl.innerHTML = data.forecast.map(d => `
      <div class="forecast-day">
        <div class="day-label">${d.date.split(",")[0]}</div>
        <img src="https://openweathermap.org/img/wn/${d.icon}.png" alt="${d.description}" />
        <div class="temps">${d.temp_high}&deg; <span>${d.temp_low}&deg;</span></div>
      </div>
    `).join("");
  } catch (e) {
    currentEl.textContent = "Could not load weather.";
    currentEl.className = "loading";
  }
}

async function loadCalendar() {
  const el = document.getElementById("calendar-events");
  try {
    const res = await fetch("/api/calendar");
    const data = await res.json();
    if (data.error) throw new Error(data.error);

    if (!data.events.length) {
      el.className = "no-events";
      el.innerHTML = "<li>No upcoming events.</li>";
      return;
    }

    el.className = "";
    el.innerHTML = data.events.map(e => `
      <li>
        <div class="event-title">${e.title}</div>
        <div class="event-time">${e.start}</div>
      </li>
    `).join("");
  } catch (e) {
    el.textContent = "Could not load calendar.";
    el.className = "loading";
  }
}

function initTheme() {
  const saved = localStorage.getItem("theme") || "light";
  document.documentElement.setAttribute("data-theme", saved);
  document.querySelectorAll(".theme-btn").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.theme === saved);
  });
}

document.querySelectorAll(".theme-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    const theme = btn.dataset.theme;
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);
    document.querySelectorAll(".theme-btn").forEach(b => {
      b.classList.toggle("active", b.dataset.theme === theme);
    });
  });
});

initTheme();
updateClock();
setInterval(updateClock, 30000);
loadWeather();
loadCalendar();
