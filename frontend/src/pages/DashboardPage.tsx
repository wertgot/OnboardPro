import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../api/client';
import { useAuth } from '../context/AuthContext';
import type { Analytics, InstanceSummary, Program } from '../types';

interface Paginated<T> {
  results: T[];
}

export function DashboardPage() {
  const { isHr, isEmployee, user } = useAuth();
  const [programs, setPrograms] = useState<Program[]>([]);
  const [instances, setInstances] = useState<InstanceSummary[]>([]);
  const [analytics, setAnalytics] = useState<Analytics | null>(null);

  useEffect(() => {
    api<Paginated<Program>>('/api/v1/programs/').then((d) => setPrograms(d.results));
    api<Paginated<InstanceSummary>>('/api/v1/instances/').then((d) => setInstances(d.results));
    if (isHr) {
      api<Analytics>('/api/v1/analytics/').then(setAnalytics).catch(() => {});
    }
  }, [isHr]);

  const myInstance = instances[0];

  return (
    <div>
      <header className="page-header">
        <h1>Добро пожаловать, {user?.full_name}</h1>
        <p className="muted">
          {isHr ? 'Панель HR-менеджера' : 'Ваш онбординг'}
        </p>
      </header>

      {isHr && analytics && (
        <div className="stats-grid">
          <div className="stat-card">
            <span className="stat-value">{analytics.total_instances}</span>
            <span className="stat-label">Экземпляров</span>
          </div>
          <div className="stat-card accent">
            <span className="stat-value">{analytics.by_status.in_progress}</span>
            <span className="stat-label">В процессе</span>
          </div>
          <div className="stat-card success">
            <span className="stat-value">{analytics.by_status.completed}</span>
            <span className="stat-label">Завершено</span>
          </div>
          <div className="stat-card warn">
            <span className="stat-value">{analytics.by_status.overdue}</span>
            <span className="stat-label">Просрочено</span>
          </div>
        </div>
      )}

      {isEmployee && myInstance && (
        <div className="hero-card">
          <div>
            <h2>Мой онбординг</h2>
            <p>Прогресс: {myInstance.progress_percent}%</p>
            <span className={`badge badge-${myInstance.status}`}>
              {myInstance.status}
            </span>
          </div>
          <Link to={`/onboarding/${myInstance.id}`} className="btn-primary">
            Открыть задачи
          </Link>
        </div>
      )}

      <section className="section">
        <div className="section-head">
          <h2>Программы</h2>
          {isHr && <Link to="/programs">Все программы →</Link>}
        </div>
        <div className="card-grid">
          {programs.slice(0, 4).map((p) => (
            <article key={p.id} className="card">
              <h3>{p.name}</h3>
              <p className="muted">{p.description || 'Без описания'}</p>
              <div className="card-meta">
                <span>{p.stages_count} этапов</span>
                <span>{p.tasks_count} задач</span>
              </div>
            </article>
          ))}
        </div>
      </section>
    </div>
  );
}
