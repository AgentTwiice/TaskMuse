import { registerRootComponent } from 'expo';
import { ExpoRoot } from 'expo-router';
import React from 'react';
import AuthProvider from './AuthContext';
import { ThemeProvider } from './ui';

export function App() {
  const ctx = require('./app/_layout').default;
  return (
    <AuthProvider>
      <ThemeProvider>
        <ExpoRoot Component={ctx} />
      </ThemeProvider>
    </AuthProvider>
  );
}

registerRootComponent(App);
