const API_BASE = '';

type Tokens = { access: string; refresh: string };

function getTokens(): Tokens | null {
  const raw = localStorage.getItem('onboardpro_tokens');
  return raw ? JSON.parse(raw) : null;
}

export function setTokens(tokens: Tokens | null) {
  if (tokens) localStorage.setItem('onboardpro_tokens', JSON.stringify(tokens));
  else localStorage.removeItem('onboardpro_tokens');
}

export function isAuthenticated(): boolean {
  return !!getTokens()?.access;
}

async function refreshAccess(): Promise<string | null> {
  const tokens = getTokens();
  if (!tokens?.refresh) return null;
  const res = await fetch(`${API_BASE}/api/v1/auth/token/refresh/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh: tokens.refresh }),
  });
  if (!res.ok) return null;
  const data = await res.json();
  setTokens({ ...tokens, access: data.access });
  return data.access;
}

export async function api<T>(
  path: string,
  options: RequestInit = {},
): Promise<T> {
  const tokens = getTokens();
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string>),
  };
  if (tokens?.access) headers.Authorization = `Bearer ${tokens.access}`;

  let res = await fetch(`${API_BASE}${path}`, { ...options, headers });

  if (res.status === 401 && tokens?.refresh) {
    const newAccess = await refreshAccess();
    if (newAccess) {
      headers.Authorization = `Bearer ${newAccess}`;
      res = await fetch(`${API_BASE}${path}`, { ...options, headers });
    }
  }

  if (res.status === 401) {
    setTokens(null);
    window.location.href = '/login';
    throw new Error('Unauthorized');
  }

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || res.statusText);
  }

  if (res.status === 204) return undefined as T;
  return res.json();
}

export async function login(username: string, password: string) {
  const res = await fetch(`${API_BASE}/api/v1/auth/token/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  });
  if (!res.ok) throw new Error('Неверный логин или пароль');
  const tokens = await res.json();
  setTokens(tokens);
  return tokens;
}

export function logout() {
  setTokens(null);
  window.location.href = '/login';
}
