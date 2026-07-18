/* Castleberry Hymns — app shell: routing, theme switch, layout. */

const { useState, useEffect } = React;

function injectFonts() {
  if (document.getElementById('cb-fonts')) return;
  const l = document.createElement('link');
  l.id = 'cb-fonts'; l.rel = 'stylesheet';
  l.href = 'https://fonts.googleapis.com/css2?family=' + window.CB_FONTS + '&display=swap';
  document.head.appendChild(l);
}

const TWEAK_DEFAULTS = /*EDITMODE-BEGIN*/{
  "direction": "heritage",
  "screen": "dashboard",
  "greeting": "Grace & peace, Thomas.",
  "showStaff": true,
  "leftPanelTone": "crimson"
}/*EDITMODE-END*/;

function App() {
  const [tw, setTweak] = useTweaks(TWEAK_DEFAULTS);
  const themeKey = window.CB_THEMES[tw.direction] ? tw.direction : 'parchment';
  const screen = tw.screen || 'dashboard';
  const t = window.CB_THEMES[themeKey];

  useEffect(() => { injectFonts(); }, []);
  useEffect(() => { document.body.style.background = t.bg; }, [t]);

  const setThemeKey = (k) => setTweak('direction', k);
  const setScreen = (s) => setTweak('screen', s);

  return (
    <div style={{ minHeight: '100vh', background: t.bg, fontFamily: t.body, color: t.ink }}>
      <ThemeStrip t={t} themes={window.CB_THEMES} current={themeKey} onPick={setThemeKey} />

      {screen === 'signin' ? (
        <SignIn t={t} tw={tw} onEnter={() => setScreen('dashboard')} />
      ) : (
        <>
          <Header t={t} onSignOut={() => setScreen('signin')} />
          <main style={{ maxWidth: 1280, margin: '0 auto', padding: '30px 26px 60px' }}>
            {/* greeting */}
            <div style={{ display: 'flex', alignItems: 'flex-end', justifyContent: 'space-between', gap: 20, flexWrap: 'wrap', marginBottom: 22 }}>
              <div style={{ minWidth: 280 }}>
                <Label t={t}>Worship Dashboard</Label>
                <h1 style={{ fontFamily: t.display, fontWeight: t.displayWeight, fontSize: 36, lineHeight: 1.08, color: t.ink, margin: '8px 0 0', letterSpacing: '.005em' }}>
                  {tw.greeting}
                </h1>
                <p style={{ fontFamily: t.body, fontSize: 15.5, color: t.sub, margin: '10px 0 0', fontStyle: 'italic' }}>
                  Here’s what the congregation has been singing — updated {CB_STATS.updated}.
                </p>
              </div>
              <div style={{ display: 'flex', gap: 10, flexShrink: 0 }}>
                <Btn t={t} kind="ghost" icon={<CalGlyph c={t.ink} />}>This Week</Btn>
                <Btn t={t} kind="brand" icon={<PlusGlyph c={t.onBrand} />}>Log a Service</Btn>
              </div>
            </div>

            {/* stat bar */}
            <div style={{ marginBottom: 26 }}><StatBar t={t} stats={CB_STATS} /></div>

            {/* two columns */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 24, alignItems: 'start' }}>
              <Tracker t={t} />
              <Downloader t={t} />
            </div>

            <footer style={{ textAlign: 'center', marginTop: 48, paddingTop: 26, borderTop: `1px solid ${t.line}` }}>
              <div style={{ display: 'inline-flex', alignItems: 'center', gap: 9, color: t.faint }}>
                <HeartMark size={20} red={t.brand} knockout={t.bg} />
                <span style={{ fontFamily: t.body, fontSize: 13, fontStyle: 'italic' }}>
                  “Sing unto the Lord a new song.” — Psalm 96:1
                </span>
              </div>
            </footer>
          </main>
        </>
      )}

      <TweaksPanel>
        <TweakSection label="Design Direction" />
        <TweakSelect label="Look" value={tw.direction}
          options={Object.values(window.CB_THEMES).map(th => ({ value: th.key, label: th.label }))}
          onChange={(v) => setTweak('direction', v)} />
        <TweakSection label="Screen" />
        <TweakRadio label="View" value={tw.screen} options={['signin', 'dashboard']}
          onChange={(v) => setTweak('screen', v)} />
        <TweakSection label="Content" />
        <TweakText label="Greeting" value={tw.greeting} onChange={(v) => setTweak('greeting', v)} />
        <TweakRadio label="Sign-in panel" value={tw.leftPanelTone} options={['crimson', 'photo']}
          onChange={(v) => setTweak('leftPanelTone', v)} />
        <TweakToggle label="Staff lines" value={tw.showStaff} onChange={(v) => setTweak('showStaff', v)} />
      </TweaksPanel>
    </div>
  );
}

const CalGlyph = ({ c }) => (
  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke={c} strokeWidth="2" strokeLinecap="round"><rect x="3" y="4" width="18" height="17" rx="2" /><path d="M3 9h18M8 2v4M16 2v4" /></svg>
);
const PlusGlyph = ({ c }) => (
  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke={c} strokeWidth="2.4" strokeLinecap="round"><path d="M12 5v14M5 12h14" /></svg>
);

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
