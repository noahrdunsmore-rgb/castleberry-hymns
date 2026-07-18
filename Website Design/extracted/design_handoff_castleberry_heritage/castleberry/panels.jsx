/* Castleberry Hymns — header, panels, downloader, dashboard, sign-in. Reads theme `t`. */

function Panel({ t, title, sub, right, children, pad = 22 }) {
  return (
    <section style={{ background: t.card, border: `1px solid ${t.line}`, borderRadius: t.radiusLg, boxShadow: t.shadow, overflow: 'hidden' }}>
      <div style={{ display: 'flex', alignItems: 'baseline', gap: 12, padding: `18px ${pad}px 0`, flexWrap: 'wrap' }}>
        <h2 style={{ margin: 0, fontFamily: t.display, fontWeight: t.displayWeight, fontSize: 25, color: t.ink, letterSpacing: '.005em', lineHeight: 1.12 }}>{title}</h2>
        {sub && <span style={{ fontFamily: t.body, fontSize: 14, color: t.sub, fontStyle: 'italic' }}>{sub}</span>}
        {right && <div style={{ marginLeft: 'auto' }}>{right}</div>}
      </div>
      <div style={{ height: 1, background: t.lineSoft, margin: `14px ${pad}px 0` }} />
      <div style={{ padding: pad }}>{children}</div>
    </section>
  );
}

/* ---- Design-direction switcher (exploration chrome) ---- */
function ThemeStrip({ t, themes, current, onPick }) {
  return (
    <div style={{ background: t.bg2, borderBottom: `1px solid ${t.line}` }}>
      <div style={{ maxWidth: 1280, margin: '0 auto', padding: '8px 26px', display: 'flex', alignItems: 'center', gap: 14, flexWrap: 'wrap' }}>
        <span style={{ fontFamily: t.body, fontSize: 11.5, fontWeight: 600, letterSpacing: '.14em', textTransform: 'uppercase', color: t.sub }}>Design Direction</span>
        <div style={{ display: 'flex', gap: 4, background: t.card, padding: 4, borderRadius: 999, border: `1px solid ${t.line}` }}>
          {Object.values(themes).map(th => {
            const on = th.key === current;
            return (
              <button key={th.key} onClick={() => onPick(th.key)} title={th.blurb} style={{
                fontFamily: t.body, fontSize: 13, fontWeight: 600, cursor: 'pointer', padding: '6px 14px',
                borderRadius: 999, border: 'none', transition: 'all .15s ease',
                background: on ? t.brand : 'transparent', color: on ? t.onBrand : t.sub,
              }}>{th.label}</button>
            );
          })}
        </div>
        <span style={{ fontFamily: t.body, fontSize: 13, color: t.faint, fontStyle: 'italic', marginLeft: 'auto' }}>
          {themes[current].blurb}
        </span>
      </div>
    </div>
  );
}

/* ---- Top header ---- */
function Header({ t, onSignOut }) {
  return (
    <header style={{ background: t.headerBg, borderBottom: `1px solid ${t.headerLine}` }}>
      {/* thin brand accent */}
      <div style={{ height: 3, background: `linear-gradient(90deg, ${t.brandDeep}, ${t.brandBright}, ${t.brandDeep})` }} />
      <div style={{ maxWidth: 1280, margin: '0 auto', padding: '14px 26px', display: 'flex', alignItems: 'center', gap: 16, flexWrap: 'wrap' }}>
        <Wordmark markSize={44} theme={t} />
        <div style={{ marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: 10, flexShrink: 0 }}>
          <Btn t={t} kind="brand" icon={<DeckGlyph c={t.onBrand} />}>Build Service Deck</Btn>
          <Btn t={t} kind="ghost" onDark={t.darkHeader} onClick={onSignOut}>Sign Out</Btn>
        </div>
      </div>
    </header>
  );
}

const DeckGlyph = ({ c }) => (
  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke={c} strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="3" y="4" width="18" height="13" rx="2" /><path d="M8 21h8M12 17v4" />
  </svg>
);
const SearchGlyph = ({ c }) => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke={c} strokeWidth="2.2" strokeLinecap="round"><circle cx="11" cy="11" r="7" /><path d="m20 20-3-3" /></svg>
);

/* ---- Tracker column ---- */
function Tracker({ t }) {
  const [period, setPeriod] = React.useState('6 Months');
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
      <Panel t={t} title="Recent Services" sub="What we've sung lately"
        right={<Btn t={t} kind="soft" small>View all 68 →</Btn>}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 13 }}>
          {CB_SERVICES.map(s => <ServiceCard key={s.id} t={t} s={s} />)}
        </div>
      </Panel>

      <Panel t={t} title="Most-Sung Hymns"
        right={
          <div style={{ display: 'flex', gap: 5, flexWrap: 'wrap' }}>
            {CB_PERIODS.map(p => <Chip key={p} t={t} active={p === period} onClick={() => setPeriod(p)}>{p}</Chip>)}
          </div>
        }>
        <TopSongs t={t} songs={CB_TOPSONGS} />
      </Panel>
    </div>
  );
}

/* ---- Downloader column ---- */
function Downloader({ t }) {
  const [q, setQ] = React.useState('');
  const [topic, setTopic] = React.useState('Grace');
  const [lib, setLib] = React.useState('All Libraries');
  const [cart, setCart] = React.useState(() => new Set(['It Is Well with My Soul']));

  const results = CB_LIBRARY.filter(s =>
    (!q || s.title.toLowerCase().includes(q.toLowerCase())) &&
    (!topic || s.topics.includes(topic)) &&
    (lib === 'All Libraries' || s.lib === lib)
  );
  const toggle = (title) => setCart(prev => { const n = new Set(prev); n.has(title) ? n.delete(title) : n.add(title); return n; });

  const fieldStyle = {
    fontFamily: t.body, fontSize: 14.5, color: t.ink, background: t.bg, padding: '10px 12px',
    border: `1px solid ${t.line}`, borderRadius: t.radius, outline: 'none', width: '100%', boxSizing: 'border-box',
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
      <Panel t={t} title="Hymn Downloader" sub={`${CB_STATS.totalSongs} songs · ${CB_STATS.libraries.join(' · ')}`}
        right={<Btn t={t} kind="gold" small icon={<SparkGlyph c={t.gold} />}>Match Sermon</Btn>}>

        {/* search + library */}
        <div style={{ display: 'flex', gap: 10, marginBottom: 14 }}>
          <div style={{ position: 'relative', flex: 1 }}>
            <span style={{ position: 'absolute', left: 12, top: '50%', transform: 'translateY(-50%)' }}><SearchGlyph c={t.faint} /></span>
            <input value={q} onChange={e => setQ(e.target.value)} placeholder="Search 892 hymns by title…"
              style={{ ...fieldStyle, paddingLeft: 36 }} />
          </div>
          <select value={lib} onChange={e => setLib(e.target.value)} style={{ ...fieldStyle, width: 'auto', cursor: 'pointer' }}>
            {['All Libraries', ...CB_STATS.libraries].map(l => <option key={l}>{l}</option>)}
          </select>
        </div>

        {/* topic chips */}
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: 7, marginBottom: 4 }}>
          {CB_TOPICS.slice(0, 12).map(tp => (
            <Chip key={tp} t={t} active={tp === topic} onClick={() => setTopic(tp === topic ? '' : tp)}>{tp}</Chip>
          ))}
          <Chip t={t} active={false}>+ {CB_TOPICS.length - 12} more</Chip>
        </div>
      </Panel>

      <Panel t={t} title={topic ? `Hymns on “${topic}”` : 'Library'} sub={`${results.length} found`}
        right={
          <Btn t={t} kind="brand" small icon={<DownloadGlyph c={t.onBrand} />}>
            Download {cart.size > 0 ? `(${cart.size})` : 'ZIP'}
          </Btn>
        }>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          {results.map((s, i) => {
            const inCart = cart.has(s.title);
            return (
              <div key={i} onClick={() => toggle(s.title)} style={{
                display: 'flex', alignItems: 'center', gap: 13, padding: '11px 12px', cursor: 'pointer',
                borderRadius: t.radius, background: inCart ? t.brandSoft : 'transparent',
                transition: 'background .14s ease',
              }}
                onMouseEnter={e => { if (!inCart) e.currentTarget.style.background = t.bg2; }}
                onMouseLeave={e => { if (!inCart) e.currentTarget.style.background = 'transparent'; }}>
                <span style={{
                  width: 21, height: 21, flex: 'none', borderRadius: 5, border: `1.5px solid ${inCart ? t.brand : t.line}`,
                  background: inCart ? t.brand : 'transparent', display: 'flex', alignItems: 'center', justifyContent: 'center',
                }}>{inCart && <CheckGlyph c={t.onBrand} />}</span>
                <span style={{ fontFamily: t.display, fontWeight: 600, fontSize: 17, color: t.ink, flex: 1, lineHeight: 1.2 }}>{s.title}</span>
                <span style={{ display: 'flex', gap: 6 }}>
                  {s.topics.slice(0, 2).map(tp => (
                    <span key={tp} style={{ fontFamily: t.body, fontSize: 11.5, color: t.sub, background: t.bg2, padding: '2px 8px', borderRadius: 999 }}>{tp}</span>
                  ))}
                </span>
                <span style={{ fontFamily: t.body, fontSize: 12, fontWeight: 600, color: t.faint, width: 86, textAlign: 'right' }}>{s.lib} · {s.no}</span>
              </div>
            );
          })}
        </div>
      </Panel>
    </div>
  );
}

const SparkGlyph = ({ c }) => (
  <svg width="14" height="14" viewBox="0 0 24 24" fill={c}><path d="M12 2l1.8 5.5L19 9l-5.2 1.5L12 16l-1.8-5.5L5 9l5.2-1.5z" /></svg>
);
const DownloadGlyph = ({ c }) => (
  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke={c} strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 3v12m0 0l-4-4m4 4l4-4M4 21h16" /></svg>
);
const CheckGlyph = ({ c }) => (
  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke={c} strokeWidth="3.2" strokeLinecap="round" strokeLinejoin="round"><path d="M20 6L9 17l-5-5" /></svg>
);

Object.assign(window, { Panel, ThemeStrip, Header, Tracker, Downloader });
