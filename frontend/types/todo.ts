export interface Todo {
  id: string;
  text: string;
  description?: string;
  status: 'complete' | 'incomplete';
  priority?: 'low' | 'medium' | 'high';
  dueDate?: Date;
  reminderDate?: Date;
  createdAt: Date;
  updatedAt: Date;
}