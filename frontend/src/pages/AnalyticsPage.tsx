import { useEffect, useState } from 'react';
import { api } from '../api/client';
import type { Analytics } from '../types';

export function AnalyticsPage() {
  const [data, setData] = useState<Analytics | null>(null);

  useEffect(() => {
    api<Analytics>('/api/v1/analytics/').then(setData);
  }, []);

  if (!data) return <p className="muted">Загрузка…</p>;

  return (
    <div>
      <header className="page-header">
        <h1>Аналитика</h1>
        <p className="muted">Сводка по онбордингам компании</p>
      </header>

      <div className="stats-grid">
        <div className="stat-card">
          <span className="stat-value">{data.total_instances}</span>
          <span className="stat-label">Всего экземпляров</span>
        </div>
        <div className="stat-card accent">
          <span className="stat-value">{Math.round(data.average_progress)}%</span>
          <span className="stat-label">Средний прогресс</span>
        </div>
        <div className="stat-card">
          <span className="stat-value">{data.employees_in_onboarding}</span>
          <span className="stat-label">Сотрудников в онбординге</span>
        </div>
      </div>

      <section className="section">
        <h2>По программам</h2>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Программа</th>
                <th>Экземпляров</th>
                <th>Активных</th>
              </tr>
            </thead>
            <tbody>
              {data.programs.map((p) => (
                <tr key={p.id}>
                  <td>{p.name}</td>
                  <td>{p.instance_count}</td>
                  <td>{p.active_count}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
