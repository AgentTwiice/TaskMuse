import { Stack } from 'expo-router';
import React from 'react';

export default function OnboardingLayout() {
  return (
    <Stack>
      <Stack.Screen name="first" options={{ headerShown: false }} />
      <Stack.Screen name="second" options={{ headerShown: false }} />
      <Stack.Screen name="third" options={{ headerShown: false }} />
    </Stack>
  );
}
