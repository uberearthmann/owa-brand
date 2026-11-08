"""
Open Worlds layout plugin for Tutor (Indigo 22.1, legacy MFEs).

Adds, through Open edX plugin slots (no core changes):
  - header links (dashboard): My courses, Catalog, Help
  - Help link in the course player header
  - logo alt text = site name
  - dashboard: "Welcome back" heading, Up next + Help sidebar,
    Resume mission / Course outline card buttons
  - player: Dates and Discussion tabs hidden
  - footer: site name, year, footer links (replaces Indigo's footer)
  - turns off Indigo's light/dark toggle (the brand is dark only)

Install (on the server):
  curl -fsSL <raw url of this file> -o "$(tutor plugins printroot)/owa_layout.py"
  tutor plugins enable owa_layout
  tutor config save
  (then rebuild the MFE image; see owa-brand/tutor/README.md)

Change links without a rebuild (restart lms only):
  tutor config save --set 'OWA_HEADER_LINKS=[...]'
  tutor config save --set OWA_HELP_URL=https://...
  tutor config save --set 'INDIGO_FOOTER_NAV_LINKS=[...]'

Remove: tutor plugins disable owa_layout, tutor config save, rebuild.
"""

from tutor import hooks
from tutormfe.hooks import PLUGIN_SLOTS

# ---------------------------------------------------------------- config

hooks.Filters.CONFIG_DEFAULTS.add_items(
    [
        (
            "OWA_HEADER_LINKS",
            [
                {"title": "My courses", "url": "/dashboard"},
                {"title": "Catalog", "url": "/courses"},
                {"title": "Help", "url": "/help"},
            ],
        ),
        ("OWA_HELP_URL", "/help"),
    ]
)

hooks.Filters.CONFIG_OVERRIDES.add_items(
    [
        # Dark-only brand: hide Indigo's light/dark switch everywhere.
        ("INDIGO_ENABLE_DARK_TOGGLE", False),
        # Footer links (read by the OWA footer below).
        (
            "INDIGO_FOOTER_NAV_LINKS",
            [
                {"title": "Help", "url": "/help"},
                {"title": "Privacy", "url": "/privacy"},
                {"title": "Terms", "url": "/tos"},
            ],
        ),
    ]
)

hooks.Filters.ENV_PATCHES.add_item(
    (
        "mfe-lms-common-settings",
        """
MFE_CONFIG["OWA_HEADER_LINKS"] = {{ OWA_HEADER_LINKS }}
MFE_CONFIG["OWA_HELP_URL"] = "{{ OWA_HELP_URL }}"
""",
    )
)

# ------------------------------------------------------------ components
# Rendered into env.config.jsx inside setConfig(); React, useState,
# useEffect, getConfig and getAuthenticatedHttpClient come from Indigo's
# imports. No double braces anywhere: this text goes through Jinja.

OWA_COMPONENTS = r"""
const OWA_CSS = `
/* ---------- header links (dashboard) ---------- */
.owa-nav { display: flex; gap: 32px; align-items: center; flex-wrap: wrap; }
.owa-nav a { font-weight: 600; font-size: 16px; color: #A9BBBF; text-decoration: none; padding: 8px 0 5px; border-bottom: 3px solid transparent; }
.owa-nav a:hover { color: #EDEDED; }
.owa-nav a[aria-current="page"] { color: #EDEDED; border-bottom-color: #FE019A; }
.owa-help-link { color: #A9BBBF; font-weight: 600; font-size: 15px; text-decoration: none; margin: 0 16px; }
.owa-help-link:hover { color: #EDEDED; }

/* ---------- dashboard heading ---------- */
.course-list-heading-container .course-list-title { font-size: 0 !important; line-height: 0; margin: 0 0 8px; }
.course-list-heading-container .course-list-title::before { content: "MY COURSES"; display: block; font-size: 14px; font-weight: 600; letter-spacing: .28em; line-height: 1.2; color: #8DA0A5; margin-bottom: 14px; }
.course-list-heading-container .course-list-title::after {
  content: "Welcome back"; display: inline-block; font-weight: 900; font-size: clamp(48px, 7vw, 88px);
  line-height: .95; letter-spacing: -.055em; color: #EDEDED; padding-right: .24em;
  background: linear-gradient(#FE019A, #FE019A) no-repeat right .02em bottom .2em / .17em .17em;
}

/* ---------- card buttons ---------- */
.owa-card-actions { display: flex; gap: 12px; flex-wrap: wrap; }
[data-test-id="CourseCardActions"]:has(.owa-card-actions) > a,
[data-test-id="CourseCardActions"]:has(.owa-card-actions) > button { display: none !important; }
.owa-btn { display: inline-flex; align-items: center; height: 48px; padding: 0 22px; border-radius: 12px; font-weight: 800; font-size: 15px; text-decoration: none !important; border: 1.5px solid transparent; }
.owa-btn-primary { background: #FE019A; color: #18262C !important; }
.owa-btn-primary:hover { background: #FF3DB2; }
.owa-btn-light { background: #EDEDED; color: #18262C !important; }
.owa-btn-ghost { border-color: #2E4048; color: #EDEDED !important; font-weight: 600; padding: 0 18px; }
.owa-btn-ghost:hover { border-color: #A9BBBF; }
.owa-btn:focus-visible, .owa-nav a:focus-visible, .owa-help-link:focus-visible, .owa-footer a:focus-visible { outline: 3px solid #FE019A; outline-offset: 2px; }

/* ---------- dashboard sidebar ---------- */
.owa-side { display: flex; flex-direction: column; gap: 16px; }
.owa-upnext { position: relative; overflow: hidden; background: #142026; border: 1px solid #2E4048; border-radius: 20px; padding: 28px; display: flex; flex-direction: column; gap: 14px; }
.owa-upnext svg { position: absolute; right: -60px; top: -40px; width: 320px; height: 260px; pointer-events: none; }
.owa-upnext > * { position: relative; }
.owa-eyebrow { font-size: 13px; font-weight: 700; letter-spacing: .24em; color: #26D9C6; }
.owa-upnext-title { font-weight: 900; font-size: 30px; line-height: 1.05; letter-spacing: -.035em; color: #EDEDED; margin: 0; }
.owa-muted { font-size: 15px; line-height: 1.5; color: #A9BBBF; margin: 0; }
.owa-upnext .owa-btn { align-self: flex-start; }
.owa-help-card { background: #20323A; border: 1px solid #2E4048; border-radius: 20px; padding: 24px 28px; display: flex; flex-direction: column; gap: 8px; }
.owa-help-card h3 { font-weight: 700; font-size: 17px; margin: 0; color: #EDEDED; }
.owa-help-card a { font-weight: 700; font-size: 15px; color: #FE019A; text-decoration: none; }

/* ---------- course player ---------- */
.course-tabs-navigation a.nav-link[href$="/dates"],
.course-tabs-navigation a.nav-link[href*="discussion"],
nav a.nav-link[href$="/dates"],
nav a.nav-link[href*="/discussion"] { display: none !important; }

/* ---------- footer ---------- */
.owa-footer { border-top: 1px solid #2E4048; background: #18262C; color: #8DA0A5; font-size: 14px; margin-top: 48px; }
.owa-footer-inner { max-width: 1328px; margin: 0 auto; padding: 28px 24px; display: flex; gap: 16px 32px; align-items: center; justify-content: space-between; flex-wrap: wrap; }
.owa-footer-name { font-weight: 700; color: #EDEDED; }
.owa-footer nav { display: flex; gap: 24px; flex-wrap: wrap; }
.owa-footer a { color: #A9BBBF; text-decoration: none; font-weight: 600; }
.owa-footer a:hover { color: #EDEDED; }
`;

const owaUrl = (u) => {
  if (!u) { return '#'; }
  if (/^(https?:|mailto:|tel:)/.test(u)) { return u; }
  return `${getConfig().LMS_BASE_URL}${u.startsWith('/') ? '' : '/'}${u}`;
};

const owaIsCurrent = (href) => {
  try {
    const target = new URL(href, window.location.href);
    const here = window.location;
    if (target.pathname === '/dashboard') {
      return here.pathname.includes('learner-dashboard') || here.pathname === '/dashboard';
    }
    return target.host === here.host && here.pathname.startsWith(target.pathname) && target.pathname !== '/';
  } catch (e) { return false; }
};

let owaHomePromise = null;
const owaLoadHome = () => {
  if (!owaHomePromise) {
    owaHomePromise = getAuthenticatedHttpClient()
      .get(`${getConfig().LMS_BASE_URL}/api/learner_home/init`)
      .then((r) => r.data)
      .catch((e) => { console.error('OWA: learner home', e); return null; });
  }
  return owaHomePromise;
};
const useOwaHome = () => {
  const [data, setData] = useState(null);
  useEffect(() => {
    let live = true;
    owaLoadHome().then((d) => { if (live) { setData(d); } });
    return () => { live = false; };
  }, []);
  return data;
};

const OwaStyles = () => <style>{OWA_CSS}</style>;

const OwaMainMenu = () => {
  const links = getConfig().OWA_HEADER_LINKS || [];
  return (
    <nav className="owa-nav" aria-label="Main">
      {links.map((l) => {
        const href = owaUrl(l.url);
        return (
          <a key={l.title} href={href} aria-current={owaIsCurrent(href) ? 'page' : undefined}>{l.title}</a>
        );
      })}
    </nav>
  );
};

const OwaHelpLink = () => (
  <a className="owa-help-link" href={owaUrl(getConfig().OWA_HELP_URL)}>Help</a>
);

const OwaLogo = () => {
  const config = getConfig();
  const base = config.LMS_BASE_URL;
  const name = config.SITE_NAME || 'Home';
  return (
    <>
      <style>
        {`
          #root header .logo-image.logo-white { display: none; }
          [data-paragon-theme-variant="dark"] #root header .logo-image { display: none; }
          [data-paragon-theme-variant="dark"] #root header .logo-white { display: block; }
        `}
      </style>
      <a href={`${base}/dashboard`} className="logo" aria-label={`${name}, my courses`}>
        <img className="logo-image" src={`${base}/static/indigo/images/logo.png`} alt={name} />
        <img className="logo-image logo-white" src={`${base}/static/indigo/images/logo-white.png`} alt={name} />
      </a>
    </>
  );
};

const OwaCardActions = ({ cardId }) => {
  const home = useOwaHome();
  if (!home || !home.courses) { return null; }
  const index = parseInt(String(cardId).replace('card-', ''), 10);
  const course = home.courses[index];
  if (!course || !course.courseRun) { return null; }
  const run = course.courseRun;
  const started = course.enrollment && course.enrollment.hasStarted;
  if (run.isArchived) {
    return (
      <div className="owa-card-actions">
        <a className="owa-btn owa-btn-ghost" href={owaUrl(run.homeUrl)}>Review course</a>
      </div>
    );
  }
  return (
    <div className="owa-card-actions">
      {started
        ? <a className="owa-btn owa-btn-primary" href={owaUrl(run.resumeUrl || run.homeUrl)}>Resume mission</a>
        : <a className="owa-btn owa-btn-light" href={owaUrl(run.homeUrl)}>Start course</a>}
      {started && <a className="owa-btn owa-btn-ghost" href={owaUrl(run.homeUrl)}>Course outline</a>}
    </div>
  );
};

const owaPickNext = (courses) => {
  const open = (courses || []).filter((c) => c.courseRun && !c.courseRun.isArchived);
  const started = open.filter((c) => c.enrollment && c.enrollment.hasStarted);
  const byRecent = (a, b) => new Date(b.enrollment.lastEnrolled || 0) - new Date(a.enrollment.lastEnrolled || 0);
  if (started.length) { return { course: started.sort(byRecent)[0], started: true }; }
  if (open.length) { return { course: open[0], started: false }; }
  return null;
};

const OwaSidebar = () => {
  const home = useOwaHome();
  const next = home ? owaPickNext(home.courses) : null;
  return (
    <aside className="owa-side" aria-label="Up next">
      {next && (
        <div className="owa-upnext">
          <svg aria-hidden="true" viewBox="0 0 320 260"><g fill="none" stroke="#26D9C6" strokeWidth="1" opacity=".35"><circle cx="260" cy="60" r="60" /><circle cx="260" cy="60" r="95" /><circle cx="260" cy="60" r="130" /></g></svg>
          <div className="owa-eyebrow">UP NEXT</div>
          <h3 className="owa-upnext-title">{next.course.course.courseName}</h3>
          <p className="owa-muted">{next.started ? 'Pick up right where you left off.' : 'Your first mission is ready.'}</p>
          <a
            className="owa-btn owa-btn-primary"
            href={owaUrl(next.started ? (next.course.courseRun.resumeUrl || next.course.courseRun.homeUrl) : next.course.courseRun.homeUrl)}
          >
            Go
          </a>
        </div>
      )}
      <div className="owa-help-card">
        <h3>Stuck on something?</h3>
        <p className="owa-muted">How missions work, resetting a password, and more.</p>
        <a href={owaUrl(getConfig().OWA_HELP_URL)}>Get help</a>
      </div>
    </aside>
  );
};

const OwaFooter = () => {
  const config = getConfig();
  const links = config.INDIGO_FOOTER_NAV_LINKS || [];
  return (
    <>
      <OwaStyles />
      <footer className="owa-footer">
        <div className="owa-footer-inner">
          <span>
            <span className="owa-footer-name">{config.SITE_NAME || ''}</span>
            {` © ${new Date().getFullYear()}`}
          </span>
          <nav aria-label="Footer">
            {links.map((l) => <a key={l.title} href={owaUrl(l.url)}>{l.title}</a>)}
          </nav>
        </div>
      </footer>
    </>
  );
};
"""

OWA_FINAL = r"""
// OWA: logo alt text = site name (swap Indigo's logo widget renderer).
if (config.pluginSlots) {
  Object.values(config.pluginSlots).forEach((slot) => {
    (slot.plugins || []).forEach((p) => {
      if (p.widget && p.widget.id === 'custom_logo') { p.widget.RenderWidget = OwaLogo; }
    });
  });
}
"""

hooks.Filters.ENV_PATCHES.add_items(
    [
        ("mfe-env-config-runtime-definitions", OWA_COMPONENTS),
        ("mfe-env-config-runtime-final", OWA_FINAL),
    ]
)

# ----------------------------------------------------------------- slots


def _insert(widget_id, component, priority=50):
    return f"""
    {{
        op: PLUGIN_OPERATIONS.Insert,
        widget: {{
            id: '{widget_id}',
            type: DIRECT_PLUGIN,
            priority: {priority},
            RenderWidget: {component},
        }},
    }},"""


HIDE_DEFAULT = """
    {
        op: PLUGIN_OPERATIONS.Hide,
        widgetId: 'default_contents',
    },"""

# Footer (and the shared OWA stylesheet that rides along with it) in every
# app Indigo styles, plus sign-in. A foreign footer widget makes Indigo's
# runtime-final drop its own footer.
for mfe in [
    "learning",
    "learner-dashboard",
    "profile",
    "account",
    "discussions",
    "authoring",
    "catalog",
    "authn",
]:
    PLUGIN_SLOTS.add_item(
        (
            mfe,
            "org.openedx.frontend.layout.footer.v1",
            HIDE_DEFAULT + _insert("owa_footer", "OwaFooter", 1),
        )
    )

PLUGIN_SLOTS.add_items(
    [
        # Dashboard header links
        (
            "learner-dashboard",
            "org.openedx.frontend.layout.header_desktop_main_menu.v1",
            HIDE_DEFAULT + _insert("owa_main_menu", "OwaMainMenu"),
        ),
        (
            "learner-dashboard",
            "org.openedx.frontend.layout.header_mobile_main_menu.v1",
            HIDE_DEFAULT + _insert("owa_main_menu_mobile", "OwaMainMenu"),
        ),
        # Dashboard sidebar: Up next + Help instead of "Looking for a new challenge"
        (
            "learner-dashboard",
            "org.openedx.frontend.learner_dashboard.widget_sidebar.v1",
            HIDE_DEFAULT + _insert("owa_sidebar", "OwaSidebar"),
        ),
        # Course card buttons
        (
            "learner-dashboard",
            "org.openedx.frontend.learner_dashboard.course_card_action.v1",
            _insert("owa_card_actions", "OwaCardActions"),
        ),
        # Course player header: Help link (Indigo already hid the default)
        (
            "learning",
            "learning_help_slot",
            _insert("owa_help_link", "OwaHelpLink", 5),
        ),
    ]
)
