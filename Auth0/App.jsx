// src/App.jsx
import React, { useState } from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import TaskItem from './components/TaskItem';
import { generatePDF } from './pdfUtils';

export default function App() {
  const { user, isAuthenticated, isLoading, loginWithRedirect, logout } = useAuth0();

  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState('');
  const [summary, setSummary] = useState('');

  const addTask = () => {
    if (title.trim() && summary.trim()) {
      const newTask = { id: Date.now(), title, summary };
      setTasks([newTask, ...tasks]);
      setTitle('');
      setSummary('');
    }
  };

  const deleteTask = (id) => {
    setTasks(tasks.filter(task => task.id !== id));
  };

  const downloadPDF = () => {
    generatePDF(tasks);
  };

  if (isLoading) return <div>Loading...</div>;

  if (!isAuthenticated) {
    return (
      <div className="login-container">
        <h2>Please log in to use the app</h2>
        <button onClick={() => loginWithRedirect()}>Log In</button>
      </div>
    );
  }

  return (
    <div className="app-container">
      <h1>To-Do List</h1>
      <p>Welcome, {user.name}</p>
      {user.picture && (
        <img
          src={user.picture}
          alt={user.name}
          style={{ borderRadius: '50%', width: 50, height: 50 }}
        />
      )}
      <button
        onClick={() => logout({ returnTo: window.location.origin })}
        style={{ marginBottom: '1rem' }}
      >
        Log Out
      </button>

      <input
        type="text"
        placeholder="Task Title"
        value={title}
        onChange={e => setTitle(e.target.value)}
      />
      <textarea
        placeholder="Summary"
        value={summary}
        onChange={e => setSummary(e.target.value)}
        rows={3}
      />
      <div>
        <button onClick={addTask}>Add Task</button>
        <button onClick={downloadPDF}>Download PDF</button>
      </div>
      <ul>
        {tasks.map(task => (
          <TaskItem key={task.id} task={task} onDelete={deleteTask} />
        ))}
      </ul>
    </div>
  );
}
