/* Castleberry Hymns — shared UI primitives + Tracker components. Reads theme tokens `t`. */

const NoteGlyph = ({ c, size = 13 }) => (
  <span style={{ color: c, fontSize: size, lineHeight: 1, transform: 'translateY(1px)', display: 'inline-block' }}>♪</span>
);

const PinGlyph = ({ c, size = 11 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill={c} style={{ flex: 'none' }}>
    <path d="M12 2C8.1 2 5 5.1 5 9c0 5.2 7 13 7 13s7-7.8 7-13c0-3.9-3.1-7-7-7zm0 9.5A2.5 2.5 0 1112 6a2.5 2.5 0 010 5.5z" />
  </svg>
);

function Btn({ t, kind = 'brand', children, onClick, icon, small, onDark }) {
  const base = {
    display: 'inline-flex', alignItems: 'center', gap: 8, cursor: 'pointer',
    fontFamily: t.body, fontWeight: 600, fontSize: small ? 13 : 14.5,
    padding: small ? '7px 13px' : '10px 18px', borderRadius: t.radius,
    border: '1px solid transparent', transition: 'all .15s ease', whiteSpace: 'nowrap',
    letterSpacing: '.01em',
  };
  const kinds = {
    brand: { background: t.brand, color: t.onBrand, boxShadow: t.shadow },
    ghost: onDark
      ? { background: 'transparent', color: t.headerInk, borderColor: t.headerLine }
      : { background: 'transparent', color: t.ink, borderColor: t.line },
    soft: { background: t.brandSoft, color: t.brand, borderColor: 'transparent' },
    gold: { background: 'transparent', color: t.gold, borderColor: t.goldSoft },
  };
  return (
    <button onClick={onClick} style={{ ...base, ...kinds[kind] }}
      onMouseEnter={e => { e.currentTarget.style.filter = 'brightness(.96)'; e.currentTarget.style.transform = 'translateY(-1px)'; }}
      onMouseLeave={e => { e.currentTarget.style.filter = 'none'; e.currentTarget.style.transform = 'none'; }}>
      {icon}{children}
    </button>
  );
}

function Label({ t, children, color }) {
  return (
    <div style={{
      fontFamily: t.body, fontWeight: 600, fontSize: 11.5, letterSpacing: '.16em',
      textTransform: 'uppercase', color: color || t.gold,
    }}>{children}</div>
  );
}

function Chip({ t, active, children, onClick }) {
  return (
    <button onClick={onClick} style={{
      fontFamily: t.body, fontSize: 13.5, fontWeight: active ? 600 : 500, cursor: 'pointer',
      padding: '6px 13px', borderRadius: 999, transition: 'all .14s ease',
      border: `1px solid ${active ? 'transparent' : t.line}`,
      background: active ? t.brand : t.card,
      color: active ? t.onBrand : t.sub,
    }}
      onMouseEnter={e => { if (!active) { e.currentTarget.style.borderColor = t.brand; e.currentTarget.style.color = t.brand; } }}
      onMouseLeave={e => { if (!active) { e.currentTarget.style.borderColor = t.line; e.currentTarget.style.color = t.sub; } }}>
      {children}
    </button>
  );
}

/* ---- Service-type badge ---- */
function TypeBadge({ t, kind, children }) {
  const map = {
    wed: { bg: t.brandSoft, fg: t.brand },
    sun: { bg: t.goldSoft, fg: t.gold },
    am: { bg: t.lineSoft, fg: t.sub },
  };
  const c = map[kind] || map.am;
  return (
    <span style={{
      fontFamily: t.body, fontSize: 11.5, fontWeight: 600, letterSpacing: '.04em',
      padding: '3px 9px', borderRadius: 999, background: c.bg, color: c.fg,
      textTransform: 'uppercase', whiteSpace: 'nowrap',
    }}>{children}</span>
  );
}

/* ---- Recent service card ---- */
function ServiceCard({ t, s }) {
  return (
    <div style={{
      background: t.card, border: `1px solid ${t.line}`, borderLeft: `3px solid ${t.brand}`,
      borderRadius: t.radius, padding: '16px 18px 15px 20px', boxShadow: t.shadow,
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 10, flexWrap: 'wrap', marginBottom: 11 }}>
        <span style={{ fontFamily: t.display, fontWeight: t.displayWeight, fontSize: 21, color: t.ink, lineHeight: 1.12 }}>
          {s.date}
        </span>
        <TypeBadge t={t} kind={s.kind}>{s.type}</TypeBadge>
        <span style={{ display: 'inline-flex', alignItems: 'center', gap: 5, marginLeft: 'auto',
          fontFamily: t.body, fontSize: 13, color: t.sub, background: t.bg2,
          padding: '4px 10px', borderRadius: 999 }}>
          <PinGlyph c={t.brand} /> {s.leader}
        </span>
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
        {s.hymns.map((h, i) => (
          <div key={i} style={{ display: 'flex', alignItems: 'baseline', gap: 9 }}>
            <NoteGlyph c={t.gold} />
            <span style={{ fontFamily: t.display, fontWeight: 600, fontSize: 17.5, color: t.ink, letterSpacing: '.005em', lineHeight: 1.25 }}>{h}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

/* ---- Stat bar ---- */
function StatBar({ t, stats }) {
  const items = [
    { n: stats.uniqueHymns, l: 'Unique Hymns' },
    { n: stats.servicesTracked, l: 'Services Tracked' },
    { n: stats.songLeaders, l: 'Song Leaders' },
  ];
  return (
    <div style={{
      background: t.statBg, color: t.onBrand, borderRadius: t.radiusLg,
      display: 'grid', gridTemplateColumns: 'repeat(3,1fr) 1.5fr', alignItems: 'center',
      boxShadow: t.shadowLg, overflow: 'hidden',
    }}>
      {items.map((it, i) => (
        <div key={i} style={{ padding: '20px 16px', textAlign: 'center',
          borderRight: `1px solid rgba(255,255,255,.16)` }}>
          <div style={{ fontFamily: t.display, fontWeight: t.displayWeight, fontSize: 40, lineHeight: 1, fontVariantNumeric: 'tabular-nums' }}>{it.n}</div>
          <div style={{ fontFamily: t.body, fontSize: 11.5, letterSpacing: '.13em', textTransform: 'uppercase', opacity: .85, marginTop: 7 }}>{it.l}</div>
        </div>
      ))}
      <div style={{ padding: '20px 22px', textAlign: 'center' }}>
        <div style={{ fontFamily: t.display, fontWeight: t.displayWeight, fontSize: 34, lineHeight: 1 }}>{stats.trackingSince}</div>
        <div style={{ fontFamily: t.body, fontSize: 11.5, letterSpacing: '.13em', textTransform: 'uppercase', opacity: .85, marginTop: 7 }}>Tracking Since</div>
      </div>
    </div>
  );
}

/* ---- Top songs bar chart ---- */
function TopSongs({ t, songs }) {
  const max = Math.max(...songs.map(s => s.count));
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 11 }}>
      {songs.map((s, i) => (
        <div key={i} style={{ display: 'grid', gridTemplateColumns: '1fr', gap: 5 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', gap: 12 }}>
            <span style={{ fontFamily: t.display, fontWeight: 600, fontSize: 16.5, color: t.ink, lineHeight: 1.2 }}>{s.title}</span>
            <span style={{ fontFamily: t.body, fontWeight: 600, fontSize: 13, color: t.sub, fontVariantNumeric: 'tabular-nums' }}>{s.count}×</span>
          </div>
          <div style={{ height: 9, borderRadius: 999, background: t.bg2, overflow: 'hidden' }}>
            <div style={{ width: `${(s.count / max) * 100}%`, height: '100%', borderRadius: 999,
              background: `linear-gradient(90deg, ${t.brandDeep}, ${t.brand})` }} />
          </div>
        </div>
      ))}
    </div>
  );
}

Object.assign(window, { NoteGlyph, PinGlyph, Btn, Label, Chip, TypeBadge, ServiceCard, StatBar, TopSongs });
