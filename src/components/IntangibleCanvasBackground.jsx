import React, { useEffect, useRef } from 'react';

/**
 * ELEMENTO 1 DEFINITIVO — FONDO INTERACTIVO MULTIDISCIPLINARIO:
 * - Paleta de 4 colores por dominio sobre fondo neutro (siempre visible en toda la pantalla)
 * - 3 Planos de profundidad con Parallax escalonado
 * - Puentes en el Eje Z entre capas contiguas
 * - Jerarquía de nodos limpia (sin halos/brillos que distraigan)
 * - Cometas y estelas de flujo viajando por las conexiones
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

// 3 Planos de profundidad definitivos (0 = Primer Plano, 1 = Plano Medio, 2 = Plano Profundo)
const PLANE_CONFIGS = [
  {
    layer: 0,
    nodeCount: 34,
    hubCount: 8,
    sizeRange: [2.2, 3.0],
    hubSize: 4.2,
    speedMult: 1.0,
    edgeAlphaDark: 0.25,
    edgeAlphaLight: 0.29,
    nodeAlphaDark: 0.74,
    nodeAlphaLight: 0.8,
    linkDistScale: 1.0,
    parallaxStrength: -18,
    trailLength: 8,
    cometRadius: 1.85
  },
  {
    layer: 1,
    nodeCount: 28,
    hubCount: 4,
    sizeRange: [1.6, 2.15],
    hubSize: 3.1,
    speedMult: 0.65,
    edgeAlphaDark: 0.16,
    edgeAlphaLight: 0.19,
    nodeAlphaDark: 0.5,
    nodeAlphaLight: 0.56,
    linkDistScale: 0.82,
    parallaxStrength: -4,
    trailLength: 5,
    cometRadius: 1.4
  },
  {
    layer: 2,
    nodeCount: 26,
    hubCount: 0,
    sizeRange: [1.15, 1.55],
    hubSize: 0,
    speedMult: 0.42,
    edgeAlphaDark: 0.1,
    edgeAlphaLight: 0.13,
    nodeAlphaDark: 0.32,
    nodeAlphaLight: 0.36,
    linkDistScale: 0.68,
    parallaxStrength: 10,
    trailLength: 3,
    cometRadius: 1.1
  }
];

export default function IntangibleCanvasBackground({ colorMode = 'dark' }) {
  const canvasRef = useRef(null);
  const mouseRef = useRef({ x: -1000, y: -1000, targetX: -1000, targetY: -1000 });
  const colorModeRef = useRef(colorMode);

  useEffect(() => {
    colorModeRef.current = colorMode;
  }, [colorMode]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    let animationFrameId;
    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    mouseRef.current.x = width * 0.5;
    mouseRef.current.y = height * 0.5;
    mouseRef.current.targetX = width * 0.5;
    mouseRef.current.targetY = height * 0.5;

    const domains = ['finance', 'math', 'ds', 'aie'];

    const planes = PLANE_CONFIGS.map((cfg) => {
      const layerNodes = [];

      for (let h = 0; h < cfg.hubCount; h++) {
        const dom = domains[h % 4];
        const angle = (h / cfg.hubCount) * Math.PI * 2 + (cfg.layer * 0.5 + 0.35);
        const rx = width * (0.5 + Math.cos(angle) * (0.28 - cfg.layer * 0.04));
        const ry = height * (0.5 + Math.sin(angle) * (0.26 - cfg.layer * 0.04));
        layerNodes.push({
          id: `L${cfg.layer}_hub_${h}`,
          layer: cfg.layer,
          domain: dom,
          isHub: true,
          x: rx,
          y: ry,
          vx: (Math.random() - 0.5) * 0.38 * cfg.speedMult,
          vy: (Math.random() - 0.5) * 0.38 * cfg.speedMult,
          size: cfg.hubSize,
          trail: []
        });
      }

      for (let i = 0; i < cfg.nodeCount; i++) {
        const dom = domains[i % 4];
        const speed = (0.42 + Math.random() * 0.45) * cfg.speedMult;
        const dir = Math.random() * Math.PI * 2;
        const size =
          cfg.sizeRange[0] + Math.random() * (cfg.sizeRange[1] - cfg.sizeRange[0]);
        layerNodes.push({
          id: `L${cfg.layer}_n_${i}`,
          layer: cfg.layer,
          domain: dom,
          isHub: false,
          x: 35 + Math.random() * (width - 70),
          y: 35 + Math.random() * (height - 70),
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
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    };

    const handleMouseMove = (e) => {
      mouseRef.current.targetX = e.clientX;
      mouseRef.current.targetY = e.clientY;
    };

    window.addEventListener('resize', handleResize);
    window.addEventListener('mousemove', handleMouseMove);

    let time = 0;

    const drawComet = (x1, y1, x2, y2, t, rgb, alpha, radius, tailLen = 0.24) => {
      const tStart = Math.max(0, t - tailLen);
      const px = x1 + (x2 - x1) * t;
      const py = y1 + (y2 - y1) * t;
      const tx = x1 + (x2 - x1) * tStart;
      const ty = y1 + (y2 - y1) * tStart;

      const grad = ctx.createLinearGradient(tx, ty, px, py);
      grad.addColorStop(0, `rgba(${rgb}, 0)`);
      grad.addColorStop(1, `rgba(${rgb}, ${Math.min(1, alpha)})`);

      ctx.beginPath();
      ctx.moveTo(tx, ty);
      ctx.lineTo(px, py);
      ctx.strokeStyle = grad;
      ctx.lineWidth = radius * 1.45;
      ctx.lineCap = 'round';
      ctx.stroke();

      ctx.beginPath();
      ctx.arc(px, py, radius, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(${rgb}, ${Math.min(1, alpha)})`;
      ctx.fill();
    };

    const render = () => {
      time += 0.008;
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

      const spotRadius = 390;

      // Halo sutil del Spotlight
      const spotGrad = ctx.createRadialGradient(mx, my, 0, mx, my, spotRadius);
      spotGrad.addColorStop(0, isDark ? 'rgba(245, 158, 11, 0.065)' : 'rgba(180, 83, 9, 0.045)');
      spotGrad.addColorStop(0.5, isDark ? 'rgba(168, 85, 247, 0.04)' : 'rgba(109, 40, 217, 0.03)');
      spotGrad.addColorStop(1, 'rgba(0, 0, 0, 0)');
      ctx.fillStyle = spotGrad;
      ctx.fillRect(0, 0, width, height);

      const baseMaxDist = Math.min(width, height) * 0.21;

      // Renderizar los 3 planos desde el más lejano (2) hasta el frontal (0)
      for (let pIdx = planes.length - 1; pIdx >= 0; pIdx--) {
        const { cfg, nodes } = planes[pIdx];
        const parX = normMx * cfg.parallaxStrength;
        const parY = normMy * cfg.parallaxStrength;

        nodes.forEach((n) => {
          const rx = n.x + parX;
          const ry = n.y + parY;
          n.renderX = rx;
          n.renderY = ry;

          if (cfg.trailLength > 0) {
            n.trail.push({ x: rx, y: ry });
            if (n.trail.length > cfg.trailLength) n.trail.shift();
          }

          n.x += n.vx;
          n.y += n.vy;

          const pad = 26;
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
        });

        const planeMaxDist = baseMaxDist * cfg.linkDistScale;
        const baseEdgeAlpha = isDark ? cfg.edgeAlphaDark : cfg.edgeAlphaLight;
        const baseNodeAlpha = isDark ? cfg.nodeAlphaDark : cfg.nodeAlphaLight;

        // Conexiones internas del plano
        for (let i = 0; i < nodes.length; i++) {
          const n1 = nodes[i];
          const x1 = n1.renderX;
          const y1 = n1.renderY;
          const dMouse1 = Math.hypot(x1 - mx, y1 - my);
          const inf1 = Math.max(0, 1 - dMouse1 / spotRadius);

          for (let j = i + 1; j < nodes.length; j++) {
            const n2 = nodes[j];
            const x2 = n2.renderX;
            const y2 = n2.renderY;

            const isHubBridge = n1.isHub || n2.isHub;
            const linkLimit = isHubBridge ? planeMaxDist * 1.25 : planeMaxDist;

            const dNodes = Math.hypot(x1 - x2, y1 - y2);
            if (dNodes >= linkLimit) continue;

            const dMouse2 = Math.hypot(x2 - mx, y2 - my);
            const inf2 = Math.max(0, 1 - dMouse2 / spotRadius);
            const pairInf = (inf1 + inf2) * 0.5;
            const distFactor = 1 - dNodes / linkLimit;

            const spotBoost = pairInf * (0.48 / (1 + cfg.layer * 0.45));
            const alpha = distFactor * Math.min(0.86, baseEdgeAlpha + spotBoost);
            if (alpha < 0.015) continue;

            const rgb1 = palette[n1.domain].rgb;
            const rgb2 = palette[n2.domain].rgb;

            ctx.beginPath();
            ctx.moveTo(x1, y1);
            ctx.lineTo(x2, y2);

            if (n1.domain !== n2.domain) {
              const grad = ctx.createLinearGradient(x1, y1, x2, y2);
              grad.addColorStop(0, `rgba(${rgb1}, ${alpha})`);
              grad.addColorStop(1, `rgba(${rgb2}, ${alpha})`);
              ctx.strokeStyle = grad;
            } else {
              ctx.strokeStyle = `rgba(${rgb1}, ${alpha})`;
            }

            ctx.lineWidth = isHubBridge ? 1.35 : Math.max(0.5, 0.9 - cfg.layer * 0.12);
            ctx.stroke();

            const cometModulo = cfg.layer === 0 ? 3 : cfg.layer === 1 ? 4 : 6;
            if ((i + j) % cometModulo === 0 && distFactor > 0.28) {
              const pulseSpeed = (0.46 + (pairInf > 0.2 ? 0.18 : 0)) * cfg.speedMult;
              const pulseT = (time * pulseSpeed + (i * 0.19 + j * 0.13)) % 1;
              const pulseAlpha = Math.min(
                1,
                baseNodeAlpha * 0.85 + pairInf * (0.45 / (1 + cfg.layer * 0.35))
              );
              drawComet(
                x1,
                y1,
                x2,
                y2,
                pulseT,
                rgb2,
                pulseAlpha,
                isHubBridge ? cfg.cometRadius * 1.15 : cfg.cometRadius
              );
            }
          }
        }

        // Puentes en el Eje Z hacia el plano contiguo más cercano
        if (pIdx > 0) {
          const closerPlane = planes[pIdx - 1];
          const zMaxDist = planeMaxDist * 0.72;

          for (let i = 0; i < nodes.length; i += 2) {
            const deepNode = nodes[i];
            const x1 = deepNode.renderX;
            const y1 = deepNode.renderY;

            for (let j = 0; j < closerPlane.nodes.length; j++) {
              const nearNode = closerPlane.nodes[j];
              if (!nearNode.isHub && j % 3 !== 0) continue;

              const x2 = nearNode.renderX ?? nearNode.x;
              const y2 = nearNode.renderY ?? nearNode.y;
              const dZ = Math.hypot(x1 - x2, y1 - y2);

              if (dZ < zMaxDist) {
                const distFactor = 1 - dZ / zMaxDist;
                const dMouse = Math.hypot((x1 + x2) * 0.5 - mx, (y1 + y2) * 0.5 - my);
                const inf = Math.max(0, 1 - dMouse / spotRadius);
                const zAlpha = distFactor * (baseEdgeAlpha * 0.75 + inf * 0.22);

                const rgbDeep = palette[deepNode.domain].rgb;
                const rgbNear = palette[nearNode.domain].rgb;

                const grad = ctx.createLinearGradient(x1, y1, x2, y2);
                grad.addColorStop(0, `rgba(${rgbDeep}, ${zAlpha * 0.55})`);
                grad.addColorStop(1, `rgba(${rgbNear}, ${zAlpha * 1.15})`);

                ctx.beginPath();
                ctx.moveTo(x1, y1);
                ctx.lineTo(x2, y2);
                ctx.strokeStyle = grad;
                ctx.lineWidth = 0.7;
                ctx.stroke();

                if ((i + j) % 4 === 0 && distFactor > 0.32) {
                  const zT = (time * 0.38 + (i * 0.23 + j * 0.17)) % 1;
                  drawComet(
                    x1,
                    y1,
                    x2,
                    y2,
                    zT,
                    rgbNear,
                    Math.min(0.9, zAlpha * 2.4),
                    cfg.cometRadius * 1.05,
                    0.28
                  );
                }
              }
            }
          }
        }

        // Nodos limpios (sin halo ni brillo externo que distraiga)
        nodes.forEach((n) => {
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
            const trailAlpha = (isDark ? 0.16 : 0.2) * (cfg.layer === 0 ? 1 : 0.6);
            ctx.strokeStyle = `rgba(${domainRgb}, ${trailAlpha})`;
            ctx.lineWidth = n.isHub ? 1.6 : 1.05;
            ctx.stroke();
          }

          const activeAlpha = Math.min(
            1,
            baseNodeAlpha + inf * (0.28 / (1 + cfg.layer * 0.35))
          );
          const radius = n.size + inf * (cfg.layer === 0 ? 0.9 : 0.45);

          ctx.beginPath();
          ctx.arc(x, y, radius, 0, Math.PI * 2);
          ctx.fillStyle = `rgba(${domainRgb}, ${activeAlpha})`;
          ctx.fill();
        });
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
