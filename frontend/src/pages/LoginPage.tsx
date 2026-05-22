import { FormEvent, useState } from 'react';
import { Navigate } from 'react-router-dom';
import { isAuthenticated, login } from '../api/client';
import { useAuth } from '../context/AuthContext';

export function LoginPage() {
  const { refresh } = useAuth();
  const [username, setUsername] = useState('hr@company.com');
  const [password, setPassword] = useState('demo1234');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  if (isAuthenticated()) return <Navigate to="/" replace />;

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await login(username, password);
      await refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Ошибка входа');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <form className="login-card" onSubmit={handleSubmit}>
        <div className="brand login-brand">
          <span className="brand-icon">◆</span>
          <span>OnboardPro</span>
        </div>
        <p className="login-subtitle">Система онбординга сотрудников</p>
        {error && <div className="alert-error">{error}</div>}
        <label>
          Логин
          <input
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            autoComplete="username"
            required
          />
        </label>
        <label>
          Пароль
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            autoComplete="current-password"
            required
          />
        </label>
        <button type="submit" className="btn-primary" disabled={loading}>
          {loading ? 'Вход…' : 'Войти'}
        </button>
        <p className="login-hint">
          Демо: hr@company.com / employee@company.com — пароль demo1234
        </p>
      </form>
    </div>
  );
}
