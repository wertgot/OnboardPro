import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { api } from '../api/client';
import { useAuth } from '../context/AuthContext';
import type { InstanceDetail, InstanceSummary } from '../types';

interface Paginated<T> {
  results: T[];
}

const taskTypeLabel: Record<string, string> = {
  document: 'Документ',
  quiz: 'Тест',
  info: 'Информация',
  checklist: 'Чеклист',
};

export function OnboardingPage() {
  const { id } = useParams();
  const { isHr } = useAuth();
  const [instances, setInstances] = useState<InstanceSummary[]>([]);
  const [detail, setDetail] = useState<InstanceDetail | null>(null);
  const [loading, setLoading] = useState(false);

  const instanceId = id ? Number(id) : instances[0]?.id;

  useEffect(() => {
    api<Paginated<InstanceSummary>>('/api/v1/instances/').then((d) =>
      setInstances(d.results),
    );
  }, []);

  useEffect(() => {
    if (!instanceId) return;
    setLoading(true);
    api<InstanceDetail>(`/api/v1/instances/${instanceId}/`)
      .then(setDetail)
      .finally(() => setLoading(false));
  }, [instanceId]);

  const toggleTask = async (taskId: number, completed: boolean) => {
    if (!instanceId) return;
    await api(`/api/v1/instances/${instanceId}/tasks/${taskId}/`, {
      method: 'PATCH',
      body: JSON.stringify({ is_completed: completed }),
    });
    const updated = await api<InstanceDetail>(`/api/v1/instances/${instanceId}/`);
    setDetail(updated);
  };

  if (!instanceId && instances.length === 0) {
    return (
      <div className="empty-state">
        <h2>Нет назначенного онбординга</h2>
        <p className="muted">Обратитесь к HR-менеджеру</p>
      </div>
    );
  }

  return (
    <div>
      <header className="page-header">
        <h1>Онбординг</h1>
        {isHr && instances.length > 1 && (
          <div className="tabs">
            {instances.map((inst) => (
              <Link
                key={inst.id}
                to={`/onboarding/${inst.id}`}
                className={inst.id === instanceId ? 'active' : ''}
              >
                #{inst.id} ({inst.progress_percent}%)
              </Link>
            ))}
          </div>
        )}
      </header>

      {loading && <p className="muted">Загрузка…</p>}

      {detail && (
        <>
          <div className="progress-bar-wrap">
            <div className="progress-bar" style={{ width: `${detail.progress_percent}%` }} />
            <span>{detail.progress_percent}%</span>
          </div>

          <div className="employee-card">
            <div>
              <strong>{detail.employee.full_name}</strong>
              <p className="muted">
                {detail.employee.position} · {detail.employee.department}
              </p>
            </div>
            <div>
              <span className={`badge badge-${detail.status}`}>{detail.status}</span>
              <p className="muted">{detail.program.name}</p>
            </div>
          </div>

          {detail.stages.map((stage) => (
            <section key={stage.id} className="stage-block">
              <h2>
                {stage.order}. {stage.name}
              </h2>
              <ul className="task-list">
                {stage.tasks.map((task) => (
                  <li
                    key={task.id}
                    className={task.is_completed ? 'done' : ''}
                  >
                    <label>
                      <input
                        type="checkbox"
                        checked={task.is_completed}
                        onChange={(e) => toggleTask(task.id, e.target.checked)}
                      />
                      <div>
                        <strong>{task.title}</strong>
                        <span className="task-meta">
                          {taskTypeLabel[task.task_type] || task.task_type}
                          {task.is_required && ' · обязательная'}
                        </span>
                        <span className="task-due">
                          до {new Date(task.due_date).toLocaleDateString('ru-RU')}
                        </span>
                      </div>
                    </label>
                  </li>
                ))}
              </ul>
            </section>
          ))}
        </>
      )}
    </div>
  );
}
