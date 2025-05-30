import * as Notifications from 'expo-notifications';
import Constants from 'expo-constants';

export async function registerPushToken(apiUrl: string, userId: string) {
  if (!Constants.isDevice) {
    return;
  }
  const { status: existingStatus } = await Notifications.getPermissionsAsync();
  let finalStatus = existingStatus;
  if (existingStatus !== 'granted') {
    const { status } = await Notifications.requestPermissionsAsync();
    finalStatus = status;
  }
  if (finalStatus !== 'granted') {
    return;
  }
  const tokenData = await Notifications.getExpoPushTokenAsync();
  await fetch(`${apiUrl}/users/push-token`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_id: userId, token: tokenData.data }),
  });
}
