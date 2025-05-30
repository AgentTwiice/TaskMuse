import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react';

interface AuthContextType {
  token: string | null;
  signIn: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  signOut: () => void;
}

const AuthContext = createContext<AuthContextType>({
  token: null,
  signIn: async () => {},
  register: async () => {},
  signOut: () => {},
});

const API_URL = process.env.EXPO_PUBLIC_API_URL ?? 'http://localhost:8000';

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [token, setToken] = useState<string | null>(null);

  const signIn = async (email: string, password: string) => {
    const res = await fetch(`${API_URL}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });
    if (res.ok) {
      const data = await res.json();
      setToken(data.access_token);
    }
  };

  const register = async (email: string, password: string) => {
    const res = await fetch(`${API_URL}/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });
    if (res.ok) {
      const data = await res.json();
      setToken(data.access_token);
    }
  };

  const refresh = async () => {
    if (!token) return;
    const res = await fetch(`${API_URL}/refresh`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}` },
    });
    if (res.ok) {
      const data = await res.json();
      setToken(data.access_token);
    }
  };

  useEffect(() => {
    const id = setInterval(refresh, 10 * 60 * 1000);
    return () => clearInterval(id);
  }, [token]);

  const signOut = () => setToken(null);

  return (
    <AuthContext.Provider value={{ token, signIn, register, signOut }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
