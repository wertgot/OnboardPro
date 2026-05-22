import { FormEvent, useEffect, useState } from 'react';
import { api } from '../api/client';
import type { Program } from '../types';

interface Paginated<T> {
  results: T[];
}

export function ProgramsPage() {
  const [programs, setPrograms] = useState<Program[]>([]);
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [error, setError] = useState('');

  const load = () =>
    api<Paginated<Program>>('/api/v1/programs/').then((d) => setPrograms(d.results));

  useEffect(() => {
    load();
  }, []);

  const handleCreate = async (e: FormEvent) => {
    e.preventDefault();
    setError('');
    try {
      await api('/api/v1/programs/', {
        method: 'POST',
        body: JSON.stringify({ name, description, is_active: true }),
      });
      setName('');
      setDescription('');
      await load();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Ошибка');
    }
  };

  return (
    <div>
      <header className="page-header">
        <h1>Программы онбординга</h1>
      </header>

      <form className="form-card" onSubmit={handleCreate}>
        <h2>Новая программа</h2>
        {error && <div className="alert-error">{error}</div>}
        <label>
          Название
          <input value={name} onChange={(e) => setName(e.target.value)} required />
        </label>
        <label>
          Описание
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={3}
          />
        </label>
        <button type="submit" className="btn-primary">
          Создать
        </button>
      </form>

      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Название</th>
              <th>Этапы</th>
              <th>Задачи</th>
              <th>Статус</th>
            </tr>
          </thead>
          <tbody>
            {programs.map((p) => (
              <tr key={p.id}>
                <td>{p.id}</td>
                <td>{p.name}</td>
                <td>{p.stages_count}</td>
                <td>{p.tasks_count}</td>
                <td>
                  <span className={p.is_active ? 'badge badge-in_progress' : 'badge'}>
                    {p.is_active ? 'Активна' : 'Неактивна'}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
