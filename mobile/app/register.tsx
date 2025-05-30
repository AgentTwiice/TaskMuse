import React, { useState } from 'react';
import { View, TextInput, Button } from 'react-native';

export default function Register() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleRegister = async () => {
    try {
      await fetch('/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });
    } catch (err) {
      // ignore
    }
  };

  return (
    <View style={{ padding: 16 }}>
      <TextInput placeholder="Username" value={username} onChangeText={setUsername} style={{ marginBottom: 8 }} />
      <TextInput placeholder="Password" value={password} onChangeText={setPassword} secureTextEntry style={{ marginBottom: 16 }} />
      <Button title="Register" onPress={handleRegister} />
    </View>
  );
}
