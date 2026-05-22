import { Link, Outlet, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const nav = [
  { to: '/', label: 'Главная' },
  { to: '/programs', label: 'Программы', hr: true },
  { to: '/onboarding', label: 'Онбординг' },
  { to: '/analytics', label: 'Аналитика', hr: true },
];

export function Layout() {
  const { user, isHr, logout } = useAuth();
  const location = useLocation();

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <span className="brand-icon">◆</span>
          <span>OnboardPro</span>
        </div>
        <nav>
          {nav
            .filter((item) => !item.hr || isHr)
            .map((item) => (
              <Link
                key={item.to}
                to={item.to}
                className={location.pathname === item.to ? 'active' : ''}
              >
                {item.label}
              </Link>
            ))}
        </nav>
        <div className="sidebar-footer">
          <div className="user-chip">
            <strong>{user?.full_name}</strong>
            <span>{user?.role}</span>
          </div>
          <button type="button" className="btn-ghost" onClick={logout}>
            Выйти
          </button>
        </div>
      </aside>
      <main className="main-content">
        <Outlet />
      </main>
    </div>
  );
}
