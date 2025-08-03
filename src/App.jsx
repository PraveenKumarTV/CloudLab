import React, { useState, useEffect } from 'react';
import { onAuthStateChanged, signOut } from 'firebase/auth';
import { auth } from './firebaseConfig';
import TaskItem from './components/TaskItem';
import { generatePDF } from './pdfUtils';
import Login from './pages/Login';

export default function App() {
  const [user, setUser] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState('');
  const [summary, setSummary] = useState('');

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, setUser);
    return () => unsubscribe();
  }, []);

  const handleLogout = () => {
    signOut(auth);
    setUser(null);
  };

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

  if (!user) return <Login onLogin={setUser} />;

  return (
    <div className="app-container">
      <h1>To-Do List</h1>
      <p>Welcome, {user.displayName}</p>
      <button onClick={handleLogout} style={{ marginBottom: '1rem' }}>Sign Out</button>

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
