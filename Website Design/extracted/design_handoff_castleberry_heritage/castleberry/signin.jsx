/* Castleberry Hymns — Sign-in / welcome experience. Reads theme `t`. */

function SignIn({ t, tw, onEnter }) {
  const showStaff = !tw || tw.showStaff !== false;
  const usePhoto = tw && tw.leftPanelTone === 'photo';
  const [mode, setMode] = React.useState('signin'); // signin | register
  const field = {
    fontFamily: t.body, fontSize: 15, color: t.ink, background: t.card, padding: '12px 14px',
    border: `1px solid ${t.line}`, borderRadius: t.radius, outline: 'none', width: '100%', boxSizing: 'border-box',
  };
  const lbl = { fontFamily: t.body, fontSize: 12.5, fontWeight: 600, letterSpacing: '.04em', color: t.sub, marginBottom: 6, display: 'block' };

  return (
    <div style={{ minHeight: '100vh', display: 'grid', gridTemplateColumns: '1.05fr .95fr', fontFamily: t.body }}>
      {/* Left — warm welcome panel */}
      <div style={{ position: 'relative', background: usePhoto ? t.headerBg : (t.darkHeader ? t.headerBg : `linear-gradient(160deg, ${t.brandDeep}, ${t.brand})`), color: t.onBrand, overflow: 'hidden', display: 'flex', flexDirection: 'column', justifyContent: 'space-between', padding: '52px 56px' }}>
        {usePhoto && (
          <div aria-hidden style={{ position: 'absolute', inset: 0 }}>
            <div style={{ position: 'absolute', inset: 0, background: `linear-gradient(160deg, ${t.brandDeep}ee, ${t.brand}cc)` }} />
          </div>
        )}
        {/* faint staff lines */}
        {showStaff && <div aria-hidden style={{ position: 'absolute', inset: 0, opacity: .07, background: `repeating-linear-gradient(0deg, transparent 0 22px, ${t.onBrand} 22px 23px)` }} />}
        <div style={{ position: 'relative', display: 'flex', alignItems: 'center', gap: 13 }}>
          <HeartMark size={50} red={t.onBrand} knockout={t.darkHeader ? t.headerBg : t.brand} />
          <div style={{ fontFamily: t.wordFont, lineHeight: 1.05 }}>
            <div style={{ fontWeight: 700, fontSize: 21, letterSpacing: '.02em', textTransform: 'uppercase' }}>Castleberry</div>
            <div style={{ fontWeight: 600, fontSize: 21, letterSpacing: '.01em', textTransform: 'uppercase', opacity: .82 }}>Church of Christ</div>
          </div>
        </div>

        <div style={{ position: 'relative' }}>
          <div style={{ fontFamily: t.body, fontSize: 13, letterSpacing: '.22em', textTransform: 'uppercase', opacity: .8, marginBottom: 18 }}>Worship Planning Tools</div>
          <h1 style={{ fontFamily: t.display, fontWeight: t.displayWeight, fontSize: 52, lineHeight: 1.04, margin: '0 0 18px' }}>
            Every hymn we’ve<br />lifted together.
          </h1>
          <p style={{ fontFamily: t.body, fontSize: 17, lineHeight: 1.6, maxWidth: 420, opacity: .9, margin: 0 }}>
            Track what the congregation has sung, discover hymns by topic, and build service decks — all in one quiet, well-kept place.
          </p>
        </div>

        <div style={{ position: 'relative', display: 'flex', gap: 30, opacity: .92 }}>
          {[['168', 'hymns sung'], ['892', 'in the library'], ['68', 'services kept']].map(([n, l]) => (
            <div key={l}>
              <div style={{ fontFamily: t.display, fontWeight: t.displayWeight, fontSize: 30 }}>{n}</div>
              <div style={{ fontFamily: t.body, fontSize: 12.5, letterSpacing: '.08em', textTransform: 'uppercase', opacity: .8 }}>{l}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Right — form */}
      <div style={{ background: t.bg, display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '40px' }}>
        <div style={{ width: '100%', maxWidth: 380 }}>
          <div style={{ display: 'flex', gap: 4, background: t.bg2, padding: 4, borderRadius: 999, marginBottom: 28, width: 'fit-content' }}>
            {['signin', 'register'].map(m => (
              <button key={m} onClick={() => setMode(m)} style={{
                fontFamily: t.body, fontSize: 13.5, fontWeight: 600, cursor: 'pointer', padding: '7px 18px',
                borderRadius: 999, border: 'none', transition: 'all .15s ease',
                background: mode === m ? t.card : 'transparent', color: mode === m ? t.brand : t.sub,
                boxShadow: mode === m ? t.shadow : 'none',
              }}>{m === 'signin' ? 'Sign In' : 'Request Access'}</button>
            ))}
          </div>

          <h2 style={{ fontFamily: t.display, fontWeight: t.displayWeight, fontSize: 30, color: t.ink, margin: '0 0 6px' }}>
            {mode === 'signin' ? 'Welcome back' : 'Join the team'}
          </h2>
          <p style={{ fontFamily: t.body, fontSize: 14.5, color: t.sub, margin: '0 0 26px', lineHeight: 1.5 }}>
            {mode === 'signin' ? 'Sign in to plan worship and review what we’ve sung.' : 'New leaders are approved by an elder before access is granted.'}
          </p>

          <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
            {mode === 'register' && (
              <div><label style={lbl}>Full Name</label><input style={field} placeholder="Thomas Holder" /></div>
            )}
            <div><label style={lbl}>Email</label><input style={field} placeholder="you@castleberry.org" /></div>
            <div><label style={lbl}>Password</label><input type="password" style={field} placeholder="••••••••" /></div>
            <button onClick={onEnter} style={{
              fontFamily: t.body, fontWeight: 600, fontSize: 15.5, cursor: 'pointer', marginTop: 4,
              padding: '13px', borderRadius: t.radius, border: 'none', background: t.brand, color: t.onBrand,
              boxShadow: t.shadowLg, transition: 'filter .15s ease',
            }}
              onMouseEnter={e => e.currentTarget.style.filter = 'brightness(.95)'}
              onMouseLeave={e => e.currentTarget.style.filter = 'none'}>
              {mode === 'signin' ? 'Sign In' : 'Request Access'}
            </button>
            {mode === 'register' && (
              <div style={{ display: 'flex', alignItems: 'center', gap: 9, padding: '11px 14px', background: t.brandSoft, borderRadius: t.radius }}>
                <ClockGlyph c={t.brand} />
                <span style={{ fontFamily: t.body, fontSize: 13, color: t.brandDeep, lineHeight: 1.45 }}>
                  Your request will be pending until an elder approves it.
                </span>
              </div>
            )}
          </div>

          <p style={{ fontFamily: t.body, fontSize: 13, color: t.faint, textAlign: 'center', marginTop: 26, fontStyle: 'italic' }}>
            “Speaking to yourselves in psalms and hymns and spiritual songs.” — Eph. 5:19
          </p>
        </div>
      </div>
    </div>
  );
}

const ClockGlyph = ({ c }) => (
  <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke={c} strokeWidth="2" strokeLinecap="round" style={{ flex: 'none' }}><circle cx="12" cy="12" r="9" /><path d="M12 7v5l3 2" /></svg>
);

Object.assign(window, { SignIn });
