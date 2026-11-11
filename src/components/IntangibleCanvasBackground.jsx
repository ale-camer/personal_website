import React, { useEffect, useRef } from 'react';

/**
 * ELEMENTO 1 DEFINITIVO — FONDO INTERACTIVO MULTIDISCIPLINARIO (ULTRA-LIVIANO):
 * - Optimizado para 60fps estables en mobile y desktop (cero createLinearGradient por arista)
 * - Escala automáticamente la cantidad de nodos en pantallas móviles (< 768px)
 * - Pausa el loop de renderizado cuando la pestaña no está visible (document.hidden)
 */
const DOMAIN_COLORS = {
  dark: {
    finance: { rgb: '245, 158, 11', hex: '#f59e0b' },
    math: { rgb: '16, 185, 129', hex: '#10b981' },
    ds: { rgb: '168, 85, 247', hex: '#a855f7' },
    aie: { rgb: '244, 63, 94', hex: '#f43f5e' }
  },
  light: {
    finance: { rgb: '180, 83, 9', hex: '#b45309' },
    math: { rgb: '4, 120, 87', hex: '#047857' },
    ds: { rgb: '109, 40, 217', hex: '#6d28d9' },
    aie: { rgb: '190, 18, 60', hex: '#be123c' }
  }
};

const PLANE_CONFIGS = [
  {
    layer: 0,
    nodeCount: 28,
    hubCount: 6,
    sizeRange: [2.2, 3.0],
    hubSize: 4.1,
    speedMult: 1.0,
    edgeAlphaDark: 0.25,
    edgeAlphaLight: 0.29,
    nodeAlphaDark: 0.74,
    nodeAlphaLight: 0.8,
    linkDistScale: 1.0,
    parallaxStrength: -16,
    trailLength: 5,
    cometRadius: 1.8
  },
  {
    layer: 1,
    nodeCount: 22,
    hubCount: 4,
    sizeRange: [1.6, 2.1],
    hubSize: 3.0,
    speedMult: 0.65,
    edgeAlphaDark: 0.16,
    edgeAlphaLight: 0.19,
    nodeAlphaDark: 0.5,
    nodeAlphaLight: 0.56,
    linkDistScale: 0.82,
    parallaxStrength: -4,
    trailLength: 3,
    cometRadius: 1.35
  },
  {
    layer: 2,
    nodeCount: 18,
    hubCount: 0,
    sizeRange: [1.15, 1.5],
    hubSize: 0,
    speedMult: 0.42,
    edgeAlphaDark: 0.1,
    edgeAlphaLight: 0.13,
    nodeAlphaDark: 0.32,
    nodeAlphaLight: 0.36,
    linkDistScale: 0.68,
    parallaxStrength: 8,
    trailLength: 0,
    cometRadius: 1.05
  }
];

export default function IntangibleCanvasBackground({ colorMode = 'dark', isPaused = false }) {
  const canvasRef = useRef(null);
  const mouseRef = useRef({ x: -1000, y: -1000, targetX: -1000, targetY: -1000 });
  const colorModeRef = useRef(colorMode);
  const isPausedRef = useRef(isPaused);

  useEffect(() => {
    colorModeRef.current = colorMode;
  }, [colorMode]);

  useEffect(() => {
    isPausedRef.current = isPaused;
  }, [isPaused]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d', { alpha: false });

    let animationFrameId;
    let width = window.innerWidth;
    let height = window.innerHeight;

    // Hardware Tiering estilo QuantLambda (detecta gama por núcleos CPU, pantalla táctil y resolución)
    const getHardwareProfile = () => {
      const vw = window.innerWidth || 1280;
      const isTouch =
        typeof window.matchMedia === 'function' &&
        window.matchMedia('(hover: none), (pointer: coarse)').matches;
      const cores = navigator.hardwareConcurrency || 4;

      // Tier 1: Smartphone (<= 680px o pantalla táctil chica)
      if (vw <= 680 || (isTouch && vw <= 768)) {
        return {
          tier: 'mobile',
          isMobile: true,
          dpr: cores <= 4 ? 0.78 : 0.9,
          densityScale: 0.36,
          frameIntervalMs: 1000 / 30 // 30 FPS estables sin recalentar batería ni trabar scroll
        };
      }
      // Tier 2: Tablet (681px - 1024px o touch)
      if (vw <= 1024 || isTouch) {
        return {
          tier: 'tablet',
          isMobile: true,
          dpr: 1.05,
          densityScale: 0.62,
          frameIntervalMs: 1000 / 45 // 45 FPS
        };
      }
      // Tier 3: Desktop (> 1024px)
      return {
        tier: 'desktop',
        isMobile: false,
        dpr: Math.min(window.devicePixelRatio || 1, 1.65),
        densityScale: 1.0,
        frameIntervalMs: 0 // 60 FPS nativo
      };
    };

    let hw = getHardwareProfile();
    let isMobile = hw.isMobile;

    const applyCanvasSize = () => {
      width = window.innerWidth;
      height = window.innerHeight;
      hw = getHardwareProfile();
      isMobile = hw.isMobile;
      const dpr = hw.dpr;
      canvas.width = Math.round(width * dpr);
      canvas.height = Math.round(height * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    };
    applyCanvasSize();

    mouseRef.current.x = width * 0.5;
    mouseRef.current.y = height * 0.5;
    mouseRef.current.targetX = width * 0.5;
    mouseRef.current.targetY = height * 0.5;

    const domains = ['finance', 'math', 'ds', 'aie'];
    const densityScale = hw.densityScale;

    const planes = PLANE_CONFIGS.map((cfg) => {
      const layerNodes = [];
      const hubTotal = Math.max(0, Math.round(cfg.hubCount * densityScale));
      const regularTotal = Math.max(6, Math.round(cfg.nodeCount * densityScale));

      for (let h = 0; h < hubTotal; h++) {
        const dom = domains[h % 4];
        const angle = (h / hubTotal) * Math.PI * 2 + (cfg.layer * 0.5 + 0.35);
        const rx = width * (0.5 + Math.cos(angle) * (0.28 - cfg.layer * 0.04));
        const ry = height * (0.5 + Math.sin(angle) * (0.26 - cfg.layer * 0.04));
        layerNodes.push({
          id: `L${cfg.layer}_hub_${h}`,
          layer: cfg.layer,
          domain: dom,
          isHub: true,
          x: rx,
          y: ry,
          vx: (Math.random() - 0.5) * 0.36 * cfg.speedMult,
          vy: (Math.random() - 0.5) * 0.36 * cfg.speedMult,
          size: cfg.hubSize,
          trail: []
        });
      }

      for (let i = 0; i < regularTotal; i++) {
        const dom = domains[i % 4];
        const speed = (0.4 + Math.random() * 0.42) * cfg.speedMult;
        const dir = Math.random() * Math.PI * 2;
        const size = cfg.sizeRange[0] + Math.random() * (cfg.sizeRange[1] - cfg.sizeRange[0]);
        layerNodes.push({
          id: `L${cfg.layer}_n_${i}`,
          layer: cfg.layer,
          domain: dom,
          isHub: false,
          x: 35 + Math.random() * Math.max(40, width - 70),
          y: 35 + Math.random() * Math.max(40, height - 70),
          vx: Math.cos(dir) * speed,
          vy: Math.sin(dir) * speed,
          size,
          trail: []
        });
      }

      return { cfg, nodes: layerNodes };
    });

    const handleResize = () => {
      if (!canvas) return;
      applyCanvasSize();
    };

    const handleMouseMove = (e) => {
      mouseRef.current.targetX = e.clientX;
      mouseRef.current.targetY = e.clientY;
    };

    window.addEventListener('resize', handleResize, { passive: true });
    window.addEventListener('mousemove', handleMouseMove, { passive: true });

    let time = 0;
    let lastFrameTime = 0;

    // Dibuja el cometa en 2 trazos simples sin alocar objetos CanvasGradient por frame
    const drawCometFast = (x1, y1, x2, y2, t, rgb, alpha, radius, tailLen = 0.22) => {
      const tStart = Math.max(0, t - tailLen);
      const px = x1 + (x2 - x1) * t;
      const py = y1 + (y2 - y1) * t;
      const tx = x1 + (x2 - x1) * tStart;
      const ty = y1 + (y2 - y1) * tStart;
      const a = Math.min(1, alpha);

      ctx.beginPath();
      ctx.moveTo(tx, ty);
      ctx.lineTo(px, py);
      ctx.strokeStyle = `rgba(${rgb}, ${(a * 0.48).toFixed(2)})`;
      ctx.lineWidth = radius * 1.35;
      ctx.lineCap = 'round';
      ctx.stroke();

      ctx.beginPath();
      ctx.arc(px, py, radius, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(${rgb}, ${a.toFixed(2)})`;
      ctx.fill();
    };

    const render = (now = 0) => {
      if (document.hidden || isPausedRef.current) {
        animationFrameId = requestAnimationFrame(render);
        return;
      }

      if (hw.frameIntervalMs > 0 && now - lastFrameTime < hw.frameIntervalMs) {
        animationFrameId = requestAnimationFrame(render);
        return;
      }
      lastFrameTime = now;

      time += hw.frameIntervalMs > 0 ? 0.014 : 0.008;
      const isDark = colorModeRef.current === 'dark';
      const palette = DOMAIN_COLORS[isDark ? 'dark' : 'light'];

      mouseRef.current.x += (mouseRef.current.targetX - mouseRef.current.x) * 0.08;
      mouseRef.current.y += (mouseRef.current.targetY - mouseRef.current.y) * 0.08;
      const mx = mouseRef.current.x;
      const my = mouseRef.current.y;

      const normMx = (mx - width * 0.5) / (width * 0.5 || 1);
      const normMy = (my - height * 0.5) / (height * 0.5 || 1);

      ctx.fillStyle = isDark ? '#09090c' : '#f6f4ef';
      ctx.fillRect(0, 0, width, height);

      const spotRadius = isMobile ? 260 : 390;

      // Único gradiente radial por frame (1 por frame en total)
      const spotGrad = ctx.createRadialGradient(mx, my, 0, mx, my, spotRadius);
      spotGrad.addColorStop(0, isDark ? 'rgba(245, 158, 11, 0.06)' : 'rgba(180, 83, 9, 0.04)');
      spotGrad.addColorStop(0.5, isDark ? 'rgba(168, 85, 247, 0.035)' : 'rgba(109, 40, 217, 0.025)');
      spotGrad.addColorStop(1, 'rgba(0, 0, 0, 0)');
      ctx.fillStyle = spotGrad;
      ctx.fillRect(0, 0, width, height);

      const baseMaxDist = Math.min(width, height) * (isMobile ? 0.25 : 0.21);

      for (let pIdx = planes.length - 1; pIdx >= 0; pIdx--) {
        const { cfg, nodes } = planes[pIdx];
        const parX = normMx * cfg.parallaxStrength;
        const parY = normMy * cfg.parallaxStrength;
        const maxTrail = isMobile ? 0 : cfg.trailLength;

        for (let k = 0; k < nodes.length; k++) {
          const n = nodes[k];
          const rx = n.x + parX;
          const ry = n.y + parY;
          n.renderX = rx;
          n.renderY = ry;

          if (maxTrail > 0) {
            n.trail.push({ x: rx, y: ry });
            if (n.trail.length > maxTrail) n.trail.shift();
          }

          n.x += n.vx;
          n.y += n.vy;

          const pad = 24;
          if (n.x < pad) {
            n.x = pad;
            n.vx = Math.abs(n.vx);
          } else if (n.x > width - pad) {
            n.x = width - pad;
            n.vx = -Math.abs(n.vx);
          }
          if (n.y < pad) {
            n.y = pad;
            n.vy = Math.abs(n.vy);
          } else if (n.y > height - pad) {
            n.y = height - pad;
            n.vy = -Math.abs(n.vy);
          }
        }

        const planeMaxDist = baseMaxDist * cfg.linkDistScale;
        const baseEdgeAlpha = isDark ? cfg.edgeAlphaDark : cfg.edgeAlphaLight;
        const baseNodeAlpha = isDark ? cfg.nodeAlphaDark : cfg.nodeAlphaLight;

        for (let i = 0; i < nodes.length; i++) {
          const n1 = nodes[i];
          const x1 = n1.renderX;
          const y1 = n1.renderY;
          const dMouse1 = Math.hypot(x1 - mx, y1 - my);
          const inf1 = Math.max(0, 1 - dMouse1 / spotRadius);
          const rgb1 = palette[n1.domain].rgb;

          for (let j = i + 1; j < nodes.length; j++) {
            const n2 = nodes[j];
            const x2 = n2.renderX;
            const y2 = n2.renderY;

            // Descarte rápido por bounding box antes de Math.hypot
            const dx = Math.abs(x1 - x2);
            const dy = Math.abs(y1 - y2);
            const isHubBridge = n1.isHub || n2.isHub;
            const linkLimit = isHubBridge ? planeMaxDist * 1.25 : planeMaxDist;
            if (dx >= linkLimit || dy >= linkLimit) continue;

            const dNodes = Math.hypot(dx, dy);
            if (dNodes >= linkLimit) continue;

            const dMouse2 = Math.hypot(x2 - mx, y2 - my);
            const inf2 = Math.max(0, 1 - dMouse2 / spotRadius);
            const pairInf = (inf1 + inf2) * 0.5;
            const distFactor = 1 - dNodes / linkLimit;

            const spotBoost = pairInf * (0.48 / (1 + cfg.layer * 0.45));
            const alpha = distFactor * Math.min(0.86, baseEdgeAlpha + spotBoost);
            if (alpha < 0.02) continue;

            ctx.beginPath();
            ctx.moveTo(x1, y1);
            ctx.lineTo(x2, y2);
            ctx.strokeStyle = `rgba(${rgb1}, ${alpha.toFixed(2)})`;
            ctx.lineWidth = isHubBridge ? 1.3 : Math.max(0.5, 0.85 - cfg.layer * 0.12);
            ctx.stroke();

            const cometModulo = isMobile ? 6 : cfg.layer === 0 ? 4 : 6;
            if ((i + j) % cometModulo === 0 && distFactor > 0.3) {
              const pulseSpeed = (0.46 + (pairInf > 0.2 ? 0.16 : 0)) * cfg.speedMult;
              const pulseT = (time * pulseSpeed + (i * 0.19 + j * 0.13)) % 1;
              const pulseAlpha = Math.min(
                1,
                baseNodeAlpha * 0.85 + pairInf * (0.42 / (1 + cfg.layer * 0.35))
              );
              drawCometFast(
                x1,
                y1,
                x2,
                y2,
                pulseT,
                palette[n2.domain].rgb,
                pulseAlpha,
                isHubBridge ? cfg.cometRadius * 1.1 : cfg.cometRadius
              );
            }
          }
        }

        // Nodos limpios
        for (let k = 0; k < nodes.length; k++) {
          const n = nodes[k];
          const x = n.renderX;
          const y = n.renderY;
          const dMouse = Math.hypot(x - mx, y - my);
          const inf = Math.max(0, 1 - dMouse / spotRadius);
          const domainRgb = palette[n.domain].rgb;

          if (n.trail.length > 2) {
            ctx.beginPath();
            ctx.moveTo(n.trail[0].x, n.trail[0].y);
            for (let tIdx = 1; tIdx < n.trail.length; tIdx++) {
              ctx.lineTo(n.trail[tIdx].x, n.trail[tIdx].y);
            }
            const trailAlpha = (isDark ? 0.15 : 0.19) * (cfg.layer === 0 ? 1 : 0.6);
            ctx.strokeStyle = `rgba(${domainRgb}, ${trailAlpha.toFixed(2)})`;
            ctx.lineWidth = n.isHub ? 1.5 : 1.0;
            ctx.stroke();
          }

          const activeAlpha = Math.min(
            1,
            baseNodeAlpha + inf * (0.28 / (1 + cfg.layer * 0.35))
          );
          const radius = n.size + inf * (cfg.layer === 0 ? 0.85 : 0.4);

          ctx.beginPath();
          ctx.arc(x, y, radius, 0, Math.PI * 2);
          ctx.fillStyle = `rgba(${domainRgb}, ${activeAlpha.toFixed(2)})`;
          ctx.fill();
        }
      }

      animationFrameId = requestAnimationFrame(render);
    };

    render();

    return () => {
      cancelAnimationFrame(animationFrameId);
      window.removeEventListener('resize', handleResize);
      window.removeEventListener('mousemove', handleMouseMove);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      style={{
        position: 'fixed',
        inset: 0,
        width: '100vw',
        height: '100vh',
        pointerEvents: 'none',
        zIndex: 0
      }}
    />
  );
}
