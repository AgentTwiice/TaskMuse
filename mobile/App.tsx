import { registerRootComponent } from 'expo';
import { ExpoRoot } from 'expo-router';
import React from 'react';
import AuthProvider from './AuthContext';

export function App() {
  const ctx = require('./app/_layout').default;
  return (
    <AuthProvider>
      <ExpoRoot Component={ctx} />
    </AuthProvider>
  );
}

registerRootComponent(App);
