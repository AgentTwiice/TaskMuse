export interface Task {
  id: number;
  title: string;
  dueDate: string;
  priority: 'low' | 'medium' | 'high';
}

export interface CalendarEvent {
  id: string | number;
  title: string;
  start: string;
  end: string;
}

const BASE_URL = '';

export async function getTasks(): Promise<Task[]> {
  const response = await fetch(`${BASE_URL}/api/v1/tasks`);
  if (!response.ok) {
    throw new Error('Failed to fetch tasks');
  }
  return response.json();
}

export async function getEvents(): Promise<CalendarEvent[]> {
  const response = await fetch(`${BASE_URL}/api/v1/google-calendar-sync`);
  if (!response.ok) {
    throw new Error('Failed to fetch events');
  }
  return response.json();
}
