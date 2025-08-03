import jsPDF from 'jspdf';

export const generatePDF = (tasks) => {
  const doc = new jsPDF();
  doc.setFontSize(16);
  doc.text("To-Do List Summary", 20, 20);

  doc.setFontSize(12);
  let y = 30;
  tasks.forEach((task, index) => {
    doc.text(`${index + 1}. ${task.title}: ${task.summary}`, 20, y);
    y += 10;
    if (y > 280) {
      doc.addPage();
      y = 20;
    }
  });

  doc.save("todo-summary.pdf");
};
