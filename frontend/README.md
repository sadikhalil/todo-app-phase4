# Modern Interactive Todo Application

A beautifully designed, highly interactive Todo application built with Next.js, Tailwind CSS, and Framer Motion. Features include smooth animations, drag-and-drop reordering, dark/light mode, and toast notifications.

## 🚀 Features

### UI/UX Features
- **Modern Design**: Contemporary UI with gradient accents and card-based layout
- **Color Scheme**: Vibrant, accessible color palette with seamless dark/light mode toggle
- **Animations**:
  - Task entry/deletion with slide and fade effects
  - Checkbox interactions with smooth checkmark animations
  - Button hover and click states with scale effects
  - Page transitions and loading states
  - Confetti celebration on task completion

### Interactive Elements
- Animated buttons with hover and ripple effects
- Smooth drag-and-drop to reorder tasks using @dnd-kit
- Toast notifications for user actions (add, delete, complete)
- Micro-interactions for enhanced UX
- Progress bar showing completion percentage

### Technical Features
- Responsive design (mobile-first approach)
- Full accessibility support (ARIA labels, keyboard navigation)
- Local storage persistence
- Component-based architecture
- TypeScript type safety

## 🛠 Tech Stack

- **Framework**: Next.js 14+
- **Styling**: Tailwind CSS v3+
- **Animation**: Framer Motion
- **Drag & Drop**: @dnd-kit/core, @dnd-kit/sortable, @dnd-kit/utilities
- **Icons**: Lucide React
- **Notifications**: React Hot Toast
- **State Management**: React Context API with useReducer

## 📁 Project Structure

```
frontend/
├── components/                 # Reusable UI components
│   ├── ui/                     # Basic UI elements (Button, Card, Input)
│   ├── Todo/                   # Todo-specific components
│   ├── ThemeToggle.tsx         # Dark/light mode toggle
│   ├── Layout.tsx              # Main layout component
│   └── ...                     # Other UI components
├── contexts/                   # React Context providers
│   └── TodoContext.tsx         # Todo state management
├── hooks/                      # Custom React hooks
│   └── useTheme.ts             # Theme management hook
├── types/                      # TypeScript type definitions
│   └── todo.ts                 # Todo interface
├── pages/                      # Next.js pages
│   └── todo.js                 # Main Todo application page
└── public/                     # Static assets
```

## 🎨 Color Palette

### Light Mode
- Primary: `#3B82F6` (Blue-500)
- Secondary: `#10B981` (Emerald-500)
- Accent: `#8B5CF6` (Violet-500)
- Background: `#F9FAFB` (Gray-50)
- Surface: `#FFFFFF` (White)
- Text: `#1F2937` (Gray-800)

### Dark Mode
- Primary: `#60A5FA` (Blue-400)
- Secondary: `#34D399` (Emerald-400)
- Accent: `#A78BFA` (Violet-400)
- Background: `#111827` (Gray-900)
- Surface: `#1F2937` (Gray-800)
- Text: `#F9FAFB` (Gray-50)

## 🎯 Animation Specifications

### Task Entry Animation
- **Trigger**: New task creation
- **Effect**: Slide in from right with fade
- **Duration**: 300ms
- **Easing**: ease-out

### Task Completion Animation
- **Trigger**: Checkbox toggle
- **Effects**:
  - Checkbox fills with color (stroke animation)
  - Text strikes through with slide effect
  - Optional confetti burst on completion
  - Smooth transition with color change
- **Duration**: 200ms for check, 300ms for movement
- **Easing**: ease-in-out

### Task Deletion Animation
- **Trigger**: Delete button click
- **Effects**:
  - Slide out to left with fade
  - Collapse height smoothly
  - Fade out completely
- **Duration**: 200ms
- **Easing**: ease-in

### Button Interaction Animations
- **Hover State**:
  - Scale up to 1.05x
  - Increase shadow depth
  - Smooth transition (150ms)
- **Click State**:
  - Scale down to 0.95x
  - Spring animation for bounce-back

### List Reordering Animation
- **Drag State**:
  - Elevate dragged item with increased shadow
  - Visual indicator for drop zones
  - Ghost element during drag
- **Drop State**:
  - Bounce animation on placement
  - Spring physics for neighboring items

## 📱 Responsive Design

### Breakpoints
- **Mobile**: 320px - 639px
- **Tablet**: 640px - 767px
- **Desktop**: 768px+

### Responsive Features
- Stacked layout on mobile
- Side-by-side sections on tablet+
- Adaptive card sizes
- Touch-friendly targets (44px minimum)

## ♿ Accessibility Features

### ARIA Labels
- Proper labeling for all interactive elements
- Role definitions for custom components
- Live regions for toast notifications
- Keyboard navigation support

### Keyboard Navigation
- Tab order follows logical sequence
- Focus indicators for interactive elements
- Shortcut keys (Enter, Space, Delete)
- Escape key for closing modals

## 🔧 How to Run

1. Install dependencies:
```bash
npm install
```

2. Run the development server:
```bash
npm run dev
```

3. Open [http://localhost:3000](http://localhost:3000) in your browser

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.