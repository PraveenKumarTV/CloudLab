import React from 'react';

export default function TaskItem({ task, onDelete }) {
  return (
    <li className="task-item">
      <strong>{task.title}</strong>
      <span>{task.summary}</span>
      <br />
      <button onClick={() => onDelete(task.id)}>Delete</button>
    </li>
  );
}
