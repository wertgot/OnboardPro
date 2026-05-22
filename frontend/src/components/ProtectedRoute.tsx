import { Navigate } from 'react-router-dom';
import { isAuthenticated } from '../api/client';
import { useAuth } from '../context/AuthContext';

export function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { loading } = useAuth();

  if (!isAuthenticated()) return <Navigate to="/login" replace />;
  if (loading) return <div className="loading-screen">Загрузка…</div>;
  return <>{children}</>;
}
