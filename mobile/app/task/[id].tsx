import React from 'react';
import { View, Text } from 'react-native';
import { useLocalSearchParams } from 'expo-router';

export default function TaskDetails() {
  const { id } = useLocalSearchParams<{ id: string }>();
  return (
    <View style={{ padding: 16 }}>
      <Text>Task ID: {id}</Text>
    </View>
  );
}
