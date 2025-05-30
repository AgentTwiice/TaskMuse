import React, { useEffect, useState } from 'react';
import { View, Text, FlatList, StyleSheet } from 'react-native';
import { useTheme } from '../ui';
import Calendar from 'react-native-big-calendar';
import { getTasks, getEvents, Task, CalendarEvent } from '../api/apiClient';

interface CombinedEvent {
  title: string;
  start: Date;
  end: Date;
  color?: string;
}

const priorityColor = (priority: Task['priority']): string => {
  switch (priority) {
    case 'high':
      return '#e57373';
    case 'medium':
      return '#ffb74d';
    default:
      return '#81c784';
  }
};

export default function Home() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [events, setEvents] = useState<CombinedEvent[]>([]);
  const { colors } = useTheme();

  useEffect(() => {
    async function loadData() {
      try {
        const [taskData, eventData] = await Promise.all([getTasks(), getEvents()]);
        setTasks(taskData);
        const calendarEvents: CombinedEvent[] = [
          ...eventData.map((ev: CalendarEvent) => ({
            title: ev.title,
            start: new Date(ev.start),
            end: new Date(ev.end),
          })),
          ...taskData.map((task) => ({
            title: task.title,
            start: new Date(task.dueDate),
            end: new Date(task.dueDate),
            color: priorityColor(task.priority),
          })),
        ];
        setEvents(calendarEvents);
      } catch (err) {
        console.warn(err);
      }
    }
    loadData();
  }, []);

  const renderTask = ({ item }: { item: Task }) => (
    <View style={[styles.taskItem, { borderColor: colors.card }]}>
      <Text style={[styles.taskTitle, { color: priorityColor(item.priority) }]}>{item.title}</Text>
      <Text style={[styles.date, { color: colors.text }]}>{new Date(item.dueDate).toLocaleDateString()}</Text>
    </View>
  );

  return (
    <View style={{ flex: 1, backgroundColor: colors.background }}>
      <Calendar events={events} height={400} />
      <FlatList
        data={tasks}
        keyExtractor={(item) => String(item.id)}
        renderItem={renderTask}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  taskItem: {
    padding: 8,
    borderBottomWidth: StyleSheet.hairlineWidth,
  },
  taskTitle: {
    fontSize: 16,
    fontWeight: 'bold',
  },
  date: {
    fontSize: 12,
  },
});
