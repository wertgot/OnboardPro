import { createContext, useContext, useEffect, useState, type ReactNode } from 'react';
import { api, isAuthenticated, logout } from '../api/client';
import type { UserMe } from '../types';

interface AuthState {
  user: UserMe | null;
  loading: boolean;
  isHr: boolean;
  isEmployee: boolean;
  logout: () => void;
  refresh: () => Promise<void>;
}

const AuthContext = createContext<AuthState | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<UserMe | null>(null);
  const [loading, setLoading] = useState(true);

  const refresh = async () => {
    if (!isAuthenticated()) {
      setUser(null);
      setLoading(false);
      return;
    }
    try {
      const me = await api<UserMe>('/api/v1/users/me/');
      setUser(me);
    } catch {
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    refresh();
  }, []);

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        isHr: user?.role === 'hr' || user?.role === 'admin',
        isEmployee: user?.role === 'employee',
        logout,
        refresh,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth outside AuthProvider');
  return ctx;
}
