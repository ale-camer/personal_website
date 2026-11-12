import React, { useEffect, useRef, useState } from 'react';
import {
  BG_VERTEX_SHADER,
  BG_FRAGMENT_SHADER,
  PARTICLE_VERTEX_SHADER,
  PARTICLE_FRAGMENT_SHADER,
  LIGHT_BG_FRAGMENT_SHADER,
  LIGHT_PARTICLE_VERTEX_SHADER,
  LIGHT_PARTICLE_FRAGMENT_SHADER,
} from './webbHorizonShaders';

function createShader(gl, type, source) {
  const shader = gl.createShader(type);
  gl.shaderSource(shader, source);
  gl.compileShader(shader);
  if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
    console.error('WebGL Shader Error:', gl.getShaderInfoLog(shader));
    gl.deleteShader(shader);
    return null;
  }
  return shader;
}

function createProgram(gl, vsSource, fsSource) {
  const vs = createShader(gl, gl.VERTEX_SHADER, vsSource);
  const fs = createShader(gl, gl.FRAGMENT_SHADER, fsSource);
  if (!vs || !fs) return null;
  const program = gl.createProgram();
  gl.attachShader(program, vs);
  gl.attachShader(program, fs);
  gl.linkProgram(program);
  if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
    console.error('WebGL Program Error:', gl.getProgramInfoLog(program));
    return null;
  }
  return program;
}

export const DARK_ARTWORKS = {
  EN: [
    {
      id: 0,
      title: 'Pillars of Creation (NGC 3324)  ⟷  Implied Volatility Surface σ(K,T)',
      medium: 'JWST Near-Infrared Dust Pillars • Black-Scholes-Merton Manifold',
    },
    {
      id: 1,
      title: 'Einstein Gravitational Ring (SMACS 0723)  ⟷  Markowitz Efficient Frontier',
      medium: 'Relativistic Spacetime Lensing • Optimal Risk-Return Tangency',
    },
    {
      id: 2,
      title: 'Bipolar Hourglass Nebula (L1527)  ⟷  Limit Order Book Depth V(p,t)',
      medium: 'Protostellar Accretion Shockwave • High-Frequency Liquidity Microstructure',
    },
    {
      id: 3,
      title: 'Southern Ring Nebula (NGC 3132)  ⟷  Itô-Fokker-Planck Probability Density',
      medium: 'Concentric Stellar Ejecta Shells • Stochastic Dispersion Trajectories',
    },
  ],
  ES: [
    {
      id: 0,
      title: 'Pilares de la Creación (NGC 3324)  ⟷  Superficie de Volatilidad Implícita σ(K,T)',
      medium: 'Pilares infrarrojos del JWST • Variedad de Black-Scholes-Merton',
    },
    {
      id: 1,
      title: 'Anillo Gravitacional de Einstein (SMACS 0723)  ⟷  Frontera Eficiente de Markowitz',
      medium: 'Lente gravitacional relativista • Tangencia óptima riesgo-retorno',
    },
    {
      id: 2,
      title: 'Nebulosa Reloj de Arena Bipolar (L1527)  ⟷  Profundidad de Order Book V(p,t)',
      medium: 'Onda de choque protoestelar • Microestructura de liquidez de alta frecuencia',
    },
    {
      id: 3,
      title: 'Nebulosa del Anillo del Sur (NGC 3132)  ⟷  Densidad de Difusión de Itô-Fokker-Planck',
      medium: 'Capas concéntricas de eyección estelar • Trayectorias de dispersión estocástica',
    },
  ],
};

export const LIGHT_ARTWORKS = {
  EN: [
    {
      id: 0,
      title: 'Fibonacci Sunflower (137.5°)  ⟷  Golden Spiral & Fibonacci Arcs',
      medium: 'Botanical Golden Phyllotaxis • Golden Ratio Retracement Manifold (23.6% • 38.2% • 61.8%)',
    },
    {
      id: 1,
      title: 'Emerald Mountain Ridge & Rivers  ⟷  Iso-Sharpe & Alpha Topography',
      medium: 'Spring Meltwater Watershed • Risk-Return Efficiency Contour Manifold',
    },
    {
      id: 2,
      title: 'Sacred Water Lotus & Pond Ripples  ⟷  Harmonic Wave Interference',
      medium: 'Botanical Water Mandala • Liquidity Cycle Wave Propagation',
    },
    {
      id: 3,
      title: 'Botanical Double Helix (DNA)  ⟷  Statistical Cointegration (Pairs)',
      medium: 'Intertwined Chlorophyll Strands • Mean-Reverting Stationary Spread (±2σ)',
    },
  ],
  ES: [
    {
      id: 0,
      title: 'Girasol de Fibonacci (137.5°)  ⟷  Espiral Áurea & Arcos de Fibonacci',
      medium: 'Filotaxis botánica de semillas • Niveles de proporción áurea φ (23.6% • 38.2% • 61.8%)',
    },
    {
      id: 1,
      title: 'Cordillera Esmeralda & Ríos  ⟷  Topografía Iso-Sharpe & Alfa',
      medium: 'Cuenca hidrográfica de deshielo • Curvas de nivel de eficiencia riesgo-retorno',
    },
    {
      id: 2,
      title: 'Flor de Loto & Estanque  ⟷  Interferencia Armónica de Ondas',
      medium: 'Mandala acuático y ondas de estanque • Propagación armónica de volatilidad',
    },
    {
      id: 3,
      title: 'ADN Botánico (Doble Hélice)  ⟷  Cointegración Estadística (Pairs)',
      medium: 'Hebras de clorofila entrelazadas • Reversión a la media y spread estacionario (±2σ)',
    },
  ],
};

export default function WebbDeepFieldCanvas({
  isPaused = false,
  lang = 'EN',
  lightMode = false,
  selectedScene = null, // null = continuous 4-pair cycle identical to Dark Mode, 0..3 = fixed pair
  morphOverride = null, // null = continuous sine wave, 0 = 100% Nature/Cosmos, 1 = 100% Quant
  onActiveSceneChange = null,
}) {
  const canvasRef = useRef(null);
  const [activePairIdx, setActivePairIdx] = useState(
    selectedScene !== null ? Number(selectedScene) % 4 : 0
  );

  const isPausedRef = useRef(isPaused);
  const lightModeRef = useRef(lightMode);
  const selectedSceneRef = useRef(selectedScene);
  const morphOverrideRef = useRef(morphOverride);
  const onActiveSceneChangeRef = useRef(onActiveSceneChange);
  const lastReportedIdxRef = useRef(activePairIdx);
  const forceDrawRef = useRef(true);

  useEffect(() => {
    isPausedRef.current = isPaused;
    forceDrawRef.current = true;
  }, [isPaused]);

  useEffect(() => {
    lightModeRef.current = lightMode;
    forceDrawRef.current = true;
  }, [lightMode]);

  useEffect(() => {
    selectedSceneRef.current = selectedScene;
    forceDrawRef.current = true;
    if (selectedScene !== null) {
      const idx = Number(selectedScene) % 4;
      lastReportedIdxRef.current = idx;
      setActivePairIdx(idx);
    }
  }, [selectedScene]);

  useEffect(() => {
    morphOverrideRef.current = morphOverride;
  }, [morphOverride]);

  useEffect(() => {
    onActiveSceneChangeRef.current = onActiveSceneChange;
  }, [onActiveSceneChange]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const getHardwareProfile = () => {
      const vw = window.innerWidth || 1280;
      const isTouch =
        typeof window.matchMedia === 'function' &&
        window.matchMedia('(hover: none), (pointer: coarse)').matches;
      const cores = navigator.hardwareConcurrency || 4;

      // Tier 1: Smartphone (<= 680px)
      if (vw <= 680 || (isTouch && vw <= 768)) {
        return {
          tier: 'mobile',
          dpr: cores <= 4 ? 0.65 : 0.75,
          particles: 2800,
          antialias: false,
          speedMult: 1.2,
        };
      }
      // Tier 2: Tablet (681px - 1024px or touch screen)
      if (vw <= 1024 || isTouch) {
        return {
          tier: 'tablet',
          dpr: 0.9,
          particles: 5500,
          antialias: false,
          speedMult: 1.1,
        };
      }
      // Tier 3: Desktop (> 1024px)
      return {
        tier: 'desktop',
        dpr: Math.min(window.devicePixelRatio || 1, 1.35),
        particles: 9500,
        antialias: false,
        speedMult: 1.0,
      };
    };

    const profile = getHardwareProfile();

    const gl = canvas.getContext('webgl', {
      alpha: false,
      antialias: profile.antialias,
      powerPreference: 'high-performance',
    });
    if (!gl) return;

    // Lazy shader compilation: only compile the active mode on first paint so the first frame appears immediately
    let darkSuite = null;
    let lightSuite = null;

    const getDarkSuite = () => {
      if (darkSuite) return darkSuite;
      const bgProgram = createProgram(gl, BG_VERTEX_SHADER, BG_FRAGMENT_SHADER);
      const ptProgram = createProgram(gl, PARTICLE_VERTEX_SHADER, PARTICLE_FRAGMENT_SHADER);
      if (!bgProgram || !ptProgram) return null;
      darkSuite = {
        bgProgram,
        ptProgram,
        bgPosLoc: gl.getAttribLocation(bgProgram, 'aPos'),
        bgResLoc: gl.getUniformLocation(bgProgram, 'uResolution'),
        bgTimeLoc: gl.getUniformLocation(bgProgram, 'uTime'),
        bgPairLoc: gl.getUniformLocation(bgProgram, 'uPair'),
        bgMorphLoc: gl.getUniformLocation(bgProgram, 'uMorph'),
        bgHorizLoc: gl.getUniformLocation(bgProgram, 'uShowHorizon'),
        ptSeedLoc: gl.getAttribLocation(ptProgram, 'aSeed'),
        ptTimeLoc: gl.getUniformLocation(ptProgram, 'uTime'),
        ptResLoc: gl.getUniformLocation(ptProgram, 'uResolution'),
        ptDprLoc: gl.getUniformLocation(ptProgram, 'uDpr'),
        ptPairLoc: gl.getUniformLocation(ptProgram, 'uPair'),
        ptMorphLoc: gl.getUniformLocation(ptProgram, 'uMorph'),
      };
      return darkSuite;
    };

    const getLightSuite = () => {
      if (lightSuite) return lightSuite;
      const lightBgProgram = createProgram(gl, BG_VERTEX_SHADER, LIGHT_BG_FRAGMENT_SHADER);
      const lightPtProgram = createProgram(gl, LIGHT_PARTICLE_VERTEX_SHADER, LIGHT_PARTICLE_FRAGMENT_SHADER);
      if (!lightBgProgram || !lightPtProgram) return null;
      lightSuite = {
        lightBgProgram,
        lightPtProgram,
        lBgPosLoc: gl.getAttribLocation(lightBgProgram, 'aPos'),
        lBgResLoc: gl.getUniformLocation(lightBgProgram, 'uResolution'),
        lBgTimeLoc: gl.getUniformLocation(lightBgProgram, 'uTime'),
        lBgPairLoc: gl.getUniformLocation(lightBgProgram, 'uPair'),
        lBgMorphLoc: gl.getUniformLocation(lightBgProgram, 'uMorph'),
        lPtSeedLoc: gl.getAttribLocation(lightPtProgram, 'aSeed'),
        lPtTimeLoc: gl.getUniformLocation(lightPtProgram, 'uTime'),
        lPtResLoc: gl.getUniformLocation(lightPtProgram, 'uResolution'),
        lPtDprLoc: gl.getUniformLocation(lightPtProgram, 'uDpr'),
        lPtPairLoc: gl.getUniformLocation(lightPtProgram, 'uPair'),
        lPtMorphLoc: gl.getUniformLocation(lightPtProgram, 'uMorph'),
      };
      return lightSuite;
    };

    if (lightModeRef.current) {
      if (!getLightSuite()) return;
    } else {
      if (!getDarkSuite()) return;
    }

    const quadVerts = new Float32Array([-1, -1, 1, -1, -1, 1, -1, 1, 1, -1, 1, 1]);
    const quadBuf = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, quadBuf);
    gl.bufferData(gl.ARRAY_BUFFER, quadVerts, gl.STATIC_DRAW);

    const MAX_PARTICLES = 24000;
    let activeParticleCount = profile.particles;
    let dpr = profile.dpr;
    let speedMult = profile.speedMult;

    const particleSeeds = new Float32Array(MAX_PARTICLES * 3);
    for (let i = 0; i < MAX_PARTICLES; i++) {
      const rawU = Math.random() * 2 - 1;
      particleSeeds[i * 3 + 0] = rawU;
      particleSeeds[i * 3 + 1] = Math.random();
      particleSeeds[i * 3 + 2] = Math.random();
    }
    const particleBuf = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, particleBuf);
    gl.bufferData(gl.ARRAY_BUFFER, particleSeeds, gl.STATIC_DRAW);

    const resize = () => {
      if (!canvas.parentElement) return;
      const nextProfile = getHardwareProfile();
      dpr = nextProfile.dpr;
      activeParticleCount = nextProfile.particles;
      speedMult = nextProfile.speedMult;
      const rect = canvas.parentElement.getBoundingClientRect();
      const rawW = rect.width > 10 ? rect.width : window.innerWidth;
      const rawH = rect.height > 10 ? rect.height : window.innerHeight;
      const width = Math.max(1, Math.floor(rawW * dpr));
      const height = Math.max(1, Math.floor(rawH * dpr));
      if (canvas.width !== width || canvas.height !== height) {
        canvas.width = width;
        canvas.height = height;
        gl.viewport(0, 0, canvas.width, canvas.height);
      }
    };
    resize();
    window.addEventListener('resize', resize);
    let ro = null;
    if (typeof ResizeObserver !== 'undefined' && canvas.parentElement) {
      ro = new ResizeObserver(() => resize());
      ro.observe(canvas.parentElement);
    }

    let isOffscreen = false;
    let io = null;
    if (typeof IntersectionObserver !== 'undefined' && canvas.parentElement) {
      io = new IntersectionObserver(
        (entries) => {
          if (entries[0]) isOffscreen = !entries[0].isIntersecting;
        },
        { threshold: 0.05 }
      );
      io.observe(canvas.parentElement);
    }

    let animId;
    let lastTime = performance.now();
    let lastDrawTime = 0;
    const minFrameMs = profile.tier === 'mobile' ? 1000 / 30 : profile.tier === 'tablet' ? 1000 / 45 : 0;
    let elapsed = 0;
    let currentPairFloat = selectedSceneRef.current !== null ? Number(selectedSceneRef.current) % 4 : 0;

    // Dynamic FPS auto-scaler for battery-saver / slower mobile GPUs
    let sampleFrames = 0;
    let sampleTimeAccum = 0;
    let didAutoScaleDown = false;

    const render = (now) => {
      if (document.hidden || isOffscreen) {
        lastTime = now;
        animId = requestAnimationFrame(render);
        return;
      }
      if (minFrameMs > 0 && now - lastDrawTime < minFrameMs) {
        animId = requestAnimationFrame(render);
        return;
      }
      lastDrawTime = now;

      const rawDeltaMs = now - lastTime;
      const dt = Math.min(0.1, Math.max(0, rawDeltaMs * 0.001));
      lastTime = now;

      if (!isPausedRef.current || forceDrawRef.current) {
        forceDrawRef.current = false;
        if (!didAutoScaleDown && rawDeltaMs > 0 && rawDeltaMs < 250) {
          sampleFrames += 1;
          sampleTimeAccum += rawDeltaMs;
          if (sampleFrames === 28) {
            const avgMs = sampleTimeAccum / sampleFrames;
            if (avgMs > 26 && profile.tier !== 'desktop') {
              didAutoScaleDown = true;
              dpr = Math.max(0.65, dpr * 0.78);
              activeParticleCount = Math.max(4500, Math.floor(activeParticleCount * 0.65));
              const rect = canvas.parentElement?.getBoundingClientRect();
              const rawW = rect && rect.width > 10 ? rect.width : window.innerWidth;
              const rawH = rect && rect.height > 10 ? rect.height : window.innerHeight;
              canvas.width = Math.max(1, Math.floor(rawW * dpr));
              canvas.height = Math.max(1, Math.floor(rawH * dpr));
              gl.viewport(0, 0, canvas.width, canvas.height);
            }
          }
        }

        elapsed += dt * speedMult;

        // Exact same morph and pair cadence across both Dark Mode and Light Mode
        const activeMorph =
          morphOverrideRef.current !== null
            ? morphOverrideRef.current
            : 0.5 - 0.5 * Math.cos(elapsed * 0.65);

        let activePair = 0;
        if (selectedSceneRef.current !== null) {
          const target = Number(selectedSceneRef.current) % 4;
          // Shortest circular distance on mod 4 ring for smooth glide when user clicks a button
          let diff = ((target - currentPairFloat + 2.0) % 4.0 + 4.0) % 4.0 - 2.0;
          currentPairFloat = (currentPairFloat + diff * Math.min(1.0, dt * 3.2) + 4.0) % 4.0;
          activePair = currentPairFloat;
        } else {
          activePair = (elapsed * 0.12) % 4.0;
          currentPairFloat = activePair;
        }

        const pairIdx = Math.floor((activePair + 0.5) % 4.0) % 4;
        if (lastReportedIdxRef.current !== pairIdx) {
          lastReportedIdxRef.current = pairIdx;
          setActivePairIdx(pairIdx);
          if (onActiveSceneChangeRef.current) {
            onActiveSceneChangeRef.current(pairIdx);
          }
        }

        if (lightModeRef.current) {
          const ls = getLightSuite();
          if (ls) {
            gl.disable(gl.BLEND);
            gl.useProgram(ls.lightBgProgram);
            gl.bindBuffer(gl.ARRAY_BUFFER, quadBuf);
            gl.enableVertexAttribArray(ls.lBgPosLoc);
            gl.vertexAttribPointer(ls.lBgPosLoc, 2, gl.FLOAT, false, 0, 0);
            gl.uniform2f(ls.lBgResLoc, canvas.width, canvas.height);
            gl.uniform1f(ls.lBgTimeLoc, elapsed);
            gl.uniform1f(ls.lBgPairLoc, activePair);
            gl.uniform1f(ls.lBgMorphLoc, activeMorph);
            gl.drawArrays(gl.TRIANGLES, 0, 6);

            gl.enable(gl.BLEND);
            gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);
            gl.useProgram(ls.lightPtProgram);
            gl.bindBuffer(gl.ARRAY_BUFFER, particleBuf);
            gl.enableVertexAttribArray(ls.lPtSeedLoc);
            gl.vertexAttribPointer(ls.lPtSeedLoc, 3, gl.FLOAT, false, 0, 0);
            gl.uniform1f(ls.lPtTimeLoc, elapsed);
            gl.uniform2f(ls.lPtResLoc, canvas.width, canvas.height);
            gl.uniform1f(ls.lPtDprLoc, dpr);
            gl.uniform1f(ls.lPtPairLoc, activePair);
            gl.uniform1f(ls.lPtMorphLoc, activeMorph);
            gl.drawArrays(gl.POINTS, 0, activeParticleCount);
          }
        } else {
          const ds = getDarkSuite();
          if (ds) {
            gl.disable(gl.BLEND);
            gl.useProgram(ds.bgProgram);
            gl.bindBuffer(gl.ARRAY_BUFFER, quadBuf);
            gl.enableVertexAttribArray(ds.bgPosLoc);
            gl.vertexAttribPointer(ds.bgPosLoc, 2, gl.FLOAT, false, 0, 0);
            gl.uniform2f(ds.bgResLoc, canvas.width, canvas.height);
            gl.uniform1f(ds.bgTimeLoc, elapsed);
            gl.uniform1f(ds.bgPairLoc, activePair);
            gl.uniform1f(ds.bgMorphLoc, activeMorph);
            gl.uniform1f(ds.bgHorizLoc, 1.0);
            gl.drawArrays(gl.TRIANGLES, 0, 6);

            gl.enable(gl.BLEND);
            gl.blendFunc(gl.SRC_ALPHA, gl.ONE);
            gl.useProgram(ds.ptProgram);
            gl.bindBuffer(gl.ARRAY_BUFFER, particleBuf);
            gl.enableVertexAttribArray(ds.ptSeedLoc);
            gl.vertexAttribPointer(ds.ptSeedLoc, 3, gl.FLOAT, false, 0, 0);
            gl.uniform1f(ds.ptTimeLoc, elapsed);
            gl.uniform2f(ds.ptResLoc, canvas.width, canvas.height);
            gl.uniform1f(ds.ptDprLoc, dpr);
            gl.uniform1f(ds.ptPairLoc, activePair);
            gl.uniform1f(ds.ptMorphLoc, activeMorph);
            gl.drawArrays(gl.POINTS, 0, activeParticleCount);
          }
        }
      }

      animId = requestAnimationFrame(render);
    };

    animId = requestAnimationFrame(render);

    return () => {
      cancelAnimationFrame(animId);
      window.removeEventListener('resize', resize);
      if (ro) ro.disconnect();
      if (io) io.disconnect();
      gl.deleteBuffer(quadBuf);
      gl.deleteBuffer(particleBuf);
      if (darkSuite) {
        gl.deleteProgram(darkSuite.bgProgram);
        gl.deleteProgram(darkSuite.ptProgram);
      }
      if (lightSuite) {
        gl.deleteProgram(lightSuite.lightBgProgram);
        gl.deleteProgram(lightSuite.lightPtProgram);
      }
    };
  }, []);

  const currentList = lightMode
    ? LIGHT_ARTWORKS[lang] || LIGHT_ARTWORKS.EN
    : DARK_ARTWORKS[lang] || DARK_ARTWORKS.EN;
  const displayIdx = selectedScene !== null ? Number(selectedScene) % 4 : activePairIdx;
  const currentPiece = currentList[displayIdx] || currentList[0];

  return (
    <div
      style={{
        position: 'absolute',
        inset: 0,
        width: '100%',
        height: '100%',
        backgroundColor: lightMode ? '#DAF3EE' : '#000000',
        overflow: 'hidden',
        transition: 'background-color 0.35s ease',
      }}
    >
      <canvas ref={canvasRef} style={{ width: '100%', height: '100%', display: 'block' }} />

      {/* GALLERY ARTWORK PLACARD (BOTTOM-CENTER, IDENTICAL TO DARK MODE) */}
      <div
        className="resp-home-artwork-placard"
        style={{
          position: 'absolute',
          bottom: '0.65rem',
          left: '50%',
          transform: 'translateX(-50%)',
          zIndex: 20,
          pointerEvents: 'none',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          textAlign: 'center',
          gap: '0.15rem',
          width: '90%',
          maxWidth: '620px',
        }}
      >
        <div
          className="serif-heading resp-home-artwork-title"
          style={{
            fontSize: '0.88rem',
            fontStyle: 'italic',
            color: lightMode ? 'rgba(11, 29, 22, 0.96)' : 'rgba(255, 255, 255, 0.92)',
            fontWeight: 500,
            letterSpacing: '0.01em',
            textShadow: lightMode
              ? '0 1px 8px rgba(255, 255, 255, 0.88)'
              : '0 1px 6px rgba(0, 0, 0, 0.85)',
          }}
        >
          {currentPiece.title}
        </div>
        <div
          className="resp-home-artwork-medium"
          style={{
            fontSize: '0.72rem',
            fontWeight: 500,
            color: lightMode ? 'rgba(18, 44, 34, 0.78)' : 'rgba(255, 255, 255, 0.62)',
            letterSpacing: '0.03em',
            textShadow: lightMode
              ? '0 1px 6px rgba(255, 255, 255, 0.78)'
              : '0 1px 4px rgba(0, 0, 0, 0.75)',
          }}
        >
          {currentPiece.medium}
        </div>
      </div>
    </div>
  );
}



