/**
 * Debris Careers — Ambient Soothing Canvas & Theme Controller
 * Generates an organic, calming particulate constellation that relaxes the mind.
 */

(function () {
  // --- 1. Theme Controller ---
  const THEME_KEY = "debris_careers_theme";

  function getSavedTheme() {
    return localStorage.getItem(THEME_KEY) || "light";
  }

  function applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem(THEME_KEY, theme);
    updateToggleButtons(theme);
  }

  function updateToggleButtons(theme) {
    document.querySelectorAll(".theme-toggle-btn").forEach((btn) => {
      const isDark = theme === "dark";
      btn.innerHTML = isDark
        ? `<span class="theme-icon">☀️</span> <span class="theme-label">Light Mode</span>`
        : `<span class="theme-icon">🌙</span> <span class="theme-label">Dark Mode</span>`;
    });
  }

  // Initialize theme on script run
  const initialTheme = getSavedTheme();
  applyTheme(initialTheme);

  document.addEventListener("DOMContentLoaded", () => {
    // Re-verify theme in DOM
    applyTheme(getSavedTheme());

    // Bind all theme toggle buttons
    document.querySelectorAll(".theme-toggle-btn").forEach((btn) => {
      btn.addEventListener("click", () => {
        const current = document.documentElement.getAttribute("data-theme") || "light";
        const next = current === "light" ? "dark" : "light";
        applyTheme(next);
      });
    });

    // --- 2. Ambient Relaxing Dots Canvas ---
    initAmbientCanvas();
  });

  function initAmbientCanvas() {
    const canvas = document.getElementById("ambientCanvas");
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    window.addEventListener("resize", () => {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    });

    // Mouse tracking for soothing gentle interaction
    const mouse = { x: null, y: null, radius: 140 };
    window.addEventListener("mousemove", (e) => {
      mouse.x = e.clientX;
      mouse.y = e.clientY;
    });
    window.addEventListener("mouseleave", () => {
      mouse.x = null;
      mouse.y = null;
    });

    // Particle definition
    const particleCount = Math.min(Math.floor((width * height) / 16000), 75);
    const particles = [];

    class Particle {
      constructor() {
        this.reset(true);
      }

      reset(init = false) {
        this.x = init ? Math.random() * width : Math.random() < 0.5 ? -10 : width + 10;
        this.y = init ? Math.random() * height : Math.random() * height;
        // Slow, soothing harmonic velocities
        this.vx = (Math.random() - 0.5) * 0.45;
        this.vy = (Math.random() - 0.5) * 0.45;
        this.baseRadius = 1.4 + Math.random() * 2.2;
        this.radius = this.baseRadius;
        this.phase = Math.random() * Math.PI * 2;
        this.phaseSpeed = 0.015 + Math.random() * 0.02;
      }

      update() {
        this.phase += this.phaseSpeed;
        this.x += this.vx + Math.sin(this.phase) * 0.2;
        this.y += this.vy + Math.cos(this.phase) * 0.2;

        // Gentle mouse interaction (smooth deflection and relaxation)
        if (mouse.x !== null && mouse.y !== null) {
          const dx = mouse.x - this.x;
          const dy = mouse.y - this.y;
          const dist = Math.hypot(dx, dy);
          if (dist < mouse.radius) {
            const force = (1 - dist / mouse.radius) * 0.6;
            this.x -= (dx / dist) * force;
            this.y -= (dy / dist) * force;
          }
        }

        // Soft screen wrapping
        if (this.x < -30) this.x = width + 30;
        if (this.x > width + 30) this.x = -30;
        if (this.y < -30) this.y = height + 30;
        if (this.y > height + 30) this.y = -30;
      }

      draw(isDark) {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        const pulse = 0.5 + 0.5 * Math.sin(this.phase);
        if (isDark) {
          ctx.fillStyle = `rgba(220, 230, 255, ${0.18 + pulse * 0.22})`;
          ctx.shadowBlur = 8;
          ctx.shadowColor = "rgba(220, 230, 255, 0.3)";
        } else {
          ctx.fillStyle = `rgba(35, 40, 50, ${0.14 + pulse * 0.16})`;
          ctx.shadowBlur = 0;
        }
        ctx.fill();
        ctx.shadowBlur = 0;
      }
    }

    for (let i = 0; i < particleCount; i++) {
      particles.push(new Particle());
    }

    // Main animation loop
    function animate() {
      ctx.clearRect(0, 0, width, height);
      const isDark = document.documentElement.getAttribute("data-theme") === "dark";

      // Draw soothing connective lines between close particles
      const maxDist = 115;
      for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
          const dx = particles[i].x - particles[j].x;
          const dy = particles[i].y - particles[j].y;
          const dist = Math.hypot(dx, dy);

          if (dist < maxDist) {
            const alpha = (1 - dist / maxDist) * (isDark ? 0.08 : 0.05);
            ctx.beginPath();
            ctx.moveTo(particles[i].x, particles[i].y);
            ctx.lineTo(particles[j].x, particles[j].y);
            ctx.strokeStyle = isDark ? `rgba(210, 225, 255, ${alpha})` : `rgba(30, 35, 45, ${alpha})`;
            ctx.lineWidth = 0.8;
            ctx.stroke();
          }
        }
      }

      // Update and draw dots
      for (let i = 0; i < particles.length; i++) {
        particles[i].update();
        particles[i].draw(isDark);
      }

      requestAnimationFrame(animate);
    }

    animate();
  }
})();
