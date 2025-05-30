import { Slot, useRouter, useSegments } from 'expo-router';
import { useEffect } from 'react';
import { useAuth } from '../src/context/AuthContext';

export default function RootLayout() {
  const { token } = useAuth();
  const segments = useSegments();
  const router = useRouter();

  useEffect(() => {
    const inAuthGroup = segments[0] === '(auth)';
    if (!token && !inAuthGroup) {
      router.replace('/(auth)/login');
    } else if (token && inAuthGroup) {
      router.replace('/');
    }
  }, [token, segments]);

  return <Slot />;
}
