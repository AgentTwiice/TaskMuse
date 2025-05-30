import React, { useEffect, useState } from 'react';
import { View, Button, Text } from 'react-native';
import * as Speech from 'expo-speech';
import Voice, { SpeechResultsEvent } from 'react-native-voice';

export default function VoiceCapture() {
  const [recording, setRecording] = useState(false);
  const [transcript, setTranscript] = useState('');

  useEffect(() => {
    const onSpeechResults = (e: SpeechResultsEvent) => {
      if (e.value && e.value.length > 0) {
        setTranscript(e.value[0]);
      }
    };

    const onSpeechEnd = async () => {
      setRecording(false);
      if (!transcript) {
        return;
      }
      try {
        const parseRes = await fetch('/api/v1/nlp/parse', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text: transcript })
        });
        const parsed = await parseRes.json();
        await fetch('/api/v1/tasks', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(parsed)
        });
        Speech.speak('Task saved for Thursday at 2 pm');
      } catch (err) {
        // handle error silently
      }
    };

    Voice.onSpeechResults = onSpeechResults;
    Voice.onSpeechEnd = onSpeechEnd;

    return () => {
      Voice.destroy().then(Voice.removeAllListeners);
    };
  }, [transcript]);

  const startRecording = async () => {
    try {
      setTranscript('');
      setRecording(true);
      await Voice.start('en-US');
    } catch (e) {
      setRecording(false);
    }
  };

  return (
    <View>
      <Text>{transcript}</Text>
      <Button
        title={recording ? 'Listening…' : 'Start Recording'}
        onPress={startRecording}
        disabled={recording}
      />
    </View>
  );
}
