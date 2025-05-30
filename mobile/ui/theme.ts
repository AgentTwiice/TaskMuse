import { Appearance } from 'react-native';

export const palette = {
  light: {
    background: '#ffffff',
    text: '#111111',
    primary: '#6200ee',
    card: '#f2f2f2',
  },
  dark: {
    background: '#000000',
    text: '#ffffff',
    primary: '#bb86fc',
    card: '#222222',
  },
};

export const spacing = {
  s: 4,
  m: 8,
  l: 16,
  xl: 24,
};

export const typography = {
  h1: 32,
  h2: 24,
  body: 16,
};

export function getTheme(scheme: 'light' | 'dark' = Appearance.getColorScheme() || 'light') {
  return {
    colors: palette[scheme],
    spacing,
    typography,
  } as const;
}
