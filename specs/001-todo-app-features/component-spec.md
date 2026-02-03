# Component Specification: Modern Interactive Todo Application

## 1. Component Architecture Overview

The Todo application follows a component-based architecture with clear separation of concerns. The components are organized in a hierarchy that promotes reusability and maintainability.

```
App
├── ThemeProvider
├── TodoProvider
└── Layout
    ├── Header
    │   ├── Title
    │   └── ThemeToggle
    └── Main
        ├── TodoInput
        ├── TodoFilters
        ├── TodoList
        │   └── TodoItem (multiple)
        ├── ProgressBar
        └── ToastContainer
```

## 2. Core Components

### 2.1 TodoProvider

**Purpose**: Manages global todo state and provides context to child components.

**Props Interface**:
```typescript
interface TodoProviderProps {
  children: React.ReactNode;
  initialTodos?: TodoItem[];
}
```

**State Structure**:
```typescript
interface TodoContextType {
  todos: TodoItem[];
  addTodo: (text: string) => void;
  toggleTodo: (id: string) => void;
  deleteTodo: (id: string) => void;
  updateTodo: (id: string, text: string) => void;
  reorderTodos: (activeId: string, overId: string) => void;
  clearCompleted: () => void;
  filteredTodos: TodoItem[];
  setFilter: (filter: 'all' | 'active' | 'completed') => void;
  activeFilter: 'all' | 'active' | 'completed';
  completedCount: number;
  totalCount: number;
}
```

**Methods**:
- `addTodo(text: string)`: Creates a new todo with unique ID
- `toggleTodo(id: string)`: Toggles completion status
- `deleteTodo(id: string)`: Removes todo with animation trigger
- `updateTodo(id: string, text: string)`: Updates todo text
- `reorderTodos(activeId: string, overId: string)`: Reorders todos after drag operation
- `clearCompleted()`: Removes all completed todos
- `setFilter(filter: 'all' | 'active | 'completed')`: Sets current filter

**Persistence**: Automatically saves to localStorage on state changes

### 2.2 TodoItem

**Purpose**: Represents an individual todo item with interactive elements.

**Props Interface**:
```typescript
interface TodoItemProps {
  id: string;
  text: string;
  completed: boolean;
  createdAt: Date;
  updatedAt: Date;
  onToggle: () => void;
  onDelete: () => void;
  onEdit: (text: string) => void;
}
```

**Features**:
- Animated checkbox with completion effect
- Strike-through text animation on completion
- Editable text field with save/cancel
- Delete button with confirmation animation
- Drag handle for reordering
- Timestamp display (created/updated)

**Animation Sequence**:
1. On completion: Checkbox fill → Text strike-through → Color change
2. On deletion: Slide out → Height collapse → Remove from DOM
3. On reorder: Lift → Move → Drop with bounce

### 2.3 TodoList

**Purpose**: Container for displaying and managing multiple TodoItems.

**Props Interface**:
```typescript
interface TodoListProps {
  todos: TodoItem[];
  onReorder?: (activeId: string, overId: string) => void;
}
```

**Features**:
- Draggable container using @dnd-kit
- Separation of active and completed todos
- Empty state display
- Progress indicator
- Animation triggers for item additions/removals

**Drag & Drop Behavior**:
- Vertical reordering only
- Collision detection with rectangular sensors
- Accessibility support for keyboard navigation
- Visual indicators during drag operations

## 3. UI Components

### 3.1 ThemeToggle

**Purpose**: Toggles between light and dark mode themes.

**Props Interface**:
```typescript
interface ThemeToggleProps {
  className?: string;
}
```

**Features**:
- Sun/moon icon animation on toggle
- Smooth transition between themes
- Persists selection in localStorage
- System preference detection

**Animation Details**:
- Rotation animation on icon swap
- Theme transition with 200ms duration
- SVG path morphing (if applicable)

### 3.2 Button

**Purpose**: Reusable button component with consistent styling and animations.

**Props Interface**:
```typescript
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  ripple?: boolean;
  children: React.ReactNode;
}
```

**Animation Behaviors**:
- Hover: Scale 1.05x with shadow increase
- Click: Scale 0.95x with spring return
- Ripple effect on click (when enabled)
- Loading spinner with rotation animation

### 3.3 Input

**Purpose**: Form input with validation and animation feedback.

**Props Interface**:
```typescript
interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helperText?: string;
  animated?: boolean;
}
```

**Features**:
- Animated focus border
- Error state animations
- Character counter
- Auto-grow functionality

### 3.4 Card

**Purpose**: Container component with shadow and rounded corners.

**Props Interface**:
```typescript
interface CardProps {
  children: React.ReactNode;
  className?: string;
  variant?: 'default' | 'elevated' | 'outline';
  animated?: boolean;
}
```

**Animation Properties**:
- Entrance animation on mount
- Hover lift effect
- Border transition on state changes

## 4. Layout Components

### 4.1 Header

**Purpose**: Application header containing title and theme controls.

**Props Interface**:
```typescript
interface HeaderProps {
  title: string;
  subtitle?: string;
  actions?: React.ReactNode;
}
```

**Features**:
- Sticky positioning
- Responsive design
- Theme toggle integration
- Animation on page load

### 4.2 TodoInput

**Purpose**: Input field for creating new todos with submit button.

**Props Interface**:
```typescript
interface TodoInputProps {
  onSubmit: (text: string) => void;
  placeholder?: string;
}
```

**Features**:
- Auto-focus on mount
- Submit on Enter key
- Validation feedback
- Add button with animation
- Character limit indicator

## 5. Animation Components

### 5.1 AnimatedWrapper

**Purpose**: Generic wrapper for applying consistent animations to any component.

**Props Interface**:
```typescript
interface AnimatedWrapperProps {
  children: React.ReactNode;
  animationType: 'fadeIn' | 'slideIn' | 'bounce' | 'scaleIn' | 'stagger';
  delay?: number;
  duration?: number;
  easing?: string;
  trigger?: boolean;
}
```

**Animation Types**:
- `fadeIn`: Opacity from 0 to 1
- `slideIn`: Translation with opacity
- `bounce`: Elastic scale animation
- `scaleIn`: Scale from 0.8 to 1
- `stagger`: Delayed sequence of child animations

### 5.2 ConfettiEffect

**Purpose**: Visual celebration for task completion.

**Props Interface**:
```typescript
interface ConfettiEffectProps {
  isActive: boolean;
  particleCount?: number;
  spread?: number;
  gravity?: number;
  colors?: string[];
}
```

**Behavior**:
- Particle explosion animation
- Configurable intensity
- Automatic cleanup after animation
- Performance optimization for mobile

### 5.3 ProgressBar

**Purpose**: Visual indicator of completion percentage.

**Props Interface**:
```typescript
interface ProgressBarProps {
  completed: number;
  total: number;
  animated?: boolean;
  className?: string;
}
```

**Features**:
- Animated progress fill
- Percentage text display
- Color gradient based on completion
- Smooth transitions on value changes

## 6. Notification Components

### 6.1 Toast

**Purpose**: Temporary notification display for user actions.

**Props Interface**:
```typescript
interface ToastProps {
  id: string;
  message: string;
  type: 'success' | 'error' | 'warning' | 'info';
  duration?: number;
  onClose: () => void;
}
```

**Animation Sequence**:
1. Slide in from top-right
2. Auto-dismiss after duration
3. Manual dismiss with close button
4. Slide out with fade

### 6.2 ToastContainer

**Purpose**: Container for managing multiple toast notifications.

**Props Interface**:
```typescript
interface ToastContainerProps {
  toasts: Toast[];
  onRemove: (id: string) => void;
}
```

**Features**:
- Stacking of multiple toasts
- Z-index management
- Animation coordination
- Swipe-to-dismiss on mobile

## 7. Utility Components

### 7.1 LoadingSpinner

**Purpose**: Visual indicator for loading states.

**Props Interface**:
```typescript
interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  color?: string;
  className?: string;
}
```

**Animation**:
- Continuous rotation
- Stroke dash animation
- Smooth acceleration/deceleration

### 7.2 EmptyState

**Purpose**: Display when no todos exist.

**Props Interface**:
```typescript
interface EmptyStateProps {
  title: string;
  description?: string;
  icon?: React.ReactNode;
  action?: React.ReactNode;
}
```

**Features**:
- Illustration or icon display
- Call-to-action button
- Gentle animation to draw attention
- Responsive layout

## 8. Accessibility Components

### 8.1 FocusTrap

**Purpose**: Restricts focus to contained elements (for modals).

**Props Interface**:
```typescript
interface FocusTrapProps {
  children: React.ReactNode;
  active?: boolean;
}
```

**Behavior**:
- Traps keyboard focus within container
- Returns focus to trigger element on deactivation
- Supports nested traps

### 8.2 SkipLink

**Purpose**: Allows keyboard users to skip to main content.

**Props Interface**:
```typescript
interface SkipLinkProps {
  target: string;
  children: string;
}
```

**Features**:
- Hidden until focused
- Smooth scroll to target
- Accessible positioning

## 9. Animation Specifications per Component

### 9.1 TodoItem Animation Details
- **Mount**: Slide in from right (300ms, ease-out)
- **Completion**: Checkmark draw (200ms) + text strike-through (300ms)
- **Deletion**: Slide out left (200ms) + height collapse (150ms)
- **Drag Start**: Lift effect (scale 1.02, shadow increase)
- **Drag End**: Drop bounce (spring physics)

### 9.2 Button Animation Details
- **Hover**: Scale(1.05) + boxShadow(increase) (150ms, ease)
- **Active**: Scale(0.95) + spring return (100ms)
- **Loading**: Spinner rotate(2s, infinite) + opacity transition

### 9.3 Theme Transition
- **Duration**: 200ms
- **Property**: Background-color, color, box-shadow
- **Easing**: Ease-in-out
- **Fallback**: Class swap with instant transition

## 10. Component Composition Guidelines

### 10.1 Styling Approach
- Use Tailwind utility classes primarily
- Create custom components for complex styling
- Maintain consistent spacing with theme variables
- Apply dark mode variants using `dark:` prefix

### 10.2 Animation Best Practices
- Limit simultaneous animations to prevent jank
- Use hardware-accelerated properties (transform, opacity)
- Implement animation disabling for reduced-motion preferences
- Optimize for 60fps performance

### 10.3 Performance Considerations
- Memoize components with React.memo
- Use useCallback for event handlers
- Implement virtualization for large lists
- Lazy load non-critical components