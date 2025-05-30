import React, { createContext, useState, useEffect, ReactNode } from 'react';
import * as SecureStore from 'expo-secure-store';

interface AuthContextType {
  token: string | null;
  login: (t: string) => void;
  logout: () => void;
}

export const AuthContext = createContext<AuthContextType>({
  token: null,
  login: () => {},
  logout: () => {},
});

export default function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(null);

  useEffect(() => {
    (async () => {
      const stored = await SecureStore.getItemAsync('jwt');
      if (stored) {
        setToken(stored);
      }
    })();
  }, []);

  useEffect(() => {
    if (token) {
      SecureStore.setItemAsync('jwt', token);
    } else {
      SecureStore.deleteItemAsync('jwt');
    }
  }, [token]);

  const value = {
    token,
    login: (t: string) => setToken(t),
    logout: () => setToken(null),
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
