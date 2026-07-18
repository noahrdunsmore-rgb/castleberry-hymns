/* Castleberry Church of Christ — logo: heart cradling a family + wordmark.
   Recreated as clean vector from the brand mark (warm red heart, three figures). */

// The heart mark. `tone` controls the figure knockout color so it reads on any bg.
function HeartMark({ size = 40, red = '#E0231F', knockout = 'currentColor' }) {
  // viewBox 0 0 100 96. Asymmetric warm heart; three standing family figures knocked out.
  return (
    <svg width={size} height={size * 0.96} viewBox="0 0 100 96" role="img" aria-label="Castleberry Church of Christ">
      <defs>
        <linearGradient id="cbHeart" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stopColor={red} />
          <stop offset="100%" stopColor={red} />
        </linearGradient>
      </defs>
      {/* Heart body: left lobe lower/rounder, right lobe taller — welcoming lean */}
      <path
        d="M50 92
           C 30 74, 6 58, 6 34
           C 6 18, 18 8, 32 8
           C 41 8, 47 13, 50 19
           C 53 11, 61 4, 72 4
           C 88 4, 96 16, 96 31
           C 96 56, 70 74, 50 92 Z"
        fill="url(#cbHeart)"
      />
      {/* Three family figures (tall→short) — round head + flared robe body, knocked out */}
      <g fill={knockout}>
        {/* adult */}
        <circle cx="40" cy="49" r="6.6" />
        <path d="M37.8 57 C 31 60, 30 74, 30 84 L 50 84 C 50 74, 49 60, 42.2 57 Z" />
        {/* middle child */}
        <circle cx="54" cy="55" r="5.6" />
        <path d="M52.2 62 C 46.4 64.5, 45.6 76, 45.6 84 L 62.4 84 C 62.4 76, 61.6 64.5, 55.8 62 Z" />
        {/* small child */}
        <circle cx="66" cy="61" r="4.7" />
        <path d="M64.4 67 C 59.6 69, 59 78, 59 84 L 73 84 C 73 78, 72.4 69, 67.6 67 Z" />
      </g>
    </svg>
  );
}

// Full lockup: mark + stacked "CASTLEBERRY / CHURCH OF CHRIST" wordmark.
function Wordmark({ markSize = 42, stacked = true, theme }) {
  const t = theme || {};
  const top = t.wordTop || '#8A8A8A';      // "CASTLEBERRY"
  const ink = t.wordInk || '#1C1C1C';      // "CHURCH ... CHRIST"
  const mid = t.wordMid || '#9A9A9A';      // "OF"
  const red = t.brand || '#E0231F';
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
      <HeartMark size={markSize} red={red} knockout={t.headerBg || '#1C1C1C'} />
      <div style={{ lineHeight: 1, fontFamily: t.wordFont || "'Oswald', sans-serif" }}>
        <div style={{
          fontWeight: 700, letterSpacing: '.02em',
          fontSize: markSize * 0.46, color: top, textTransform: 'uppercase',
        }}>Castleberry</div>
        <div style={{
          fontWeight: 600, letterSpacing: '.01em',
          fontSize: markSize * 0.46, color: ink, textTransform: 'uppercase', marginTop: 2,
        }}>
          Church <span style={{ color: mid }}>of</span> Christ
        </div>
      </div>
    </div>
  );
}

Object.assign(window, { HeartMark, Wordmark });
