import React from 'react';
import { View, Text } from 'react-native';
import { Button, useTheme } from '../../ui';
import { useLocalSearchParams } from 'expo-router';

export default function TaskDetails() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const { colors } = useTheme();
  return (
    <View style={{ padding: 16, backgroundColor: colors.background, flex: 1 }}>
      <Text style={{ color: colors.text }}>Task ID: {id}</Text>
      <Button title="Complete" onPress={() => {}} />
    </View>
  );
}
