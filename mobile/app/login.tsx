import React, { useState, useContext } from 'react';
import { View, TextInput, Button } from 'react-native';
import { AuthContext } from '../AuthContext';

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const { login } = useContext(AuthContext);

  const handleLogin = async () => {
    try {
      const res = await fetch('/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });
      const data = await res.json();
      if (data.token) {
        login(data.token);
      }
    } catch (err) {
      // ignore
    }
  };

  return (
    <View style={{ padding: 16 }}>
      <TextInput placeholder="Username" value={username} onChangeText={setUsername} style={{ marginBottom: 8 }} />
      <TextInput placeholder="Password" value={password} onChangeText={setPassword} secureTextEntry style={{ marginBottom: 16 }} />
      <Button title="Login" onPress={handleLogin} />
    </View>
  );
}
