import React, { createContext, useContext } from 'react';
import { useColorScheme } from 'react-native';
import { getTheme } from './theme';

type Theme = ReturnType<typeof getTheme>;

const ThemeContext = createContext<Theme>(getTheme());

export const useTheme = () => useContext(ThemeContext);

export default function ThemeProvider({ children }: { children: React.ReactNode }) {
  const scheme = useColorScheme() ?? 'light';
  const theme = getTheme(scheme);
  return <ThemeContext.Provider value={theme}>{children}</ThemeContext.Provider>;
}
