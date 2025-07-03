<template>
  <div class="schedule-container">
    <div class="schedule-header">
      <div class="header-row">
        <h2>My Classes</h2>
        <Button label="Download as PDF" icon="pi pi-download" @click="exportToPdf"
          class="p-button-outlined p-button-sm" />
      </div>
      <div class="schedule-legend">
        <div v-for="(color, subject) in subjectColors" :key="subject" class="legend-item">
          <div class="color-square" :style="{ backgroundColor: color }"></div>
          <span>{{ subject }}</span>
        </div>
      </div>
    </div>

    <div class="schedule-grid">
      <div class="schedule-row header-row">
        <div class="time-column">Time</div>
        <div class="day-column" v-for="day in daysOfWeek" :key="day">{{ day }}</div>
      </div>

      <div v-for="(timeSlot, index) in timeSlots" :key="index" class="schedule-row">
        <div class="time-column">{{ formatTime(timeSlot) }}</div>
        <div v-for="day in daysOfWeek" :key="day + timeSlot" class="day-column">
          <div class="schedule-item-container" @click="showScheduleDetails(getClassAtHour(day, timeSlot))">
            <div v-if="shouldShowClass(day, timeSlot)" class="schedule-item clickable" :style="{
              backgroundColor: getClassAtHour(day, timeSlot).timeColor,
              height: calculateHeight(day, timeSlot),
              top: calculateTopOffset(day, timeSlot)
            }">
              <div class="schedule-item-content">
                <h4>{{ getClassAtHour(day, timeSlot).subject }}</h4>
                <p class="room">Room: {{ getClassAtHour(day, timeSlot).room }}</p>
                <p class="time">{{ getClassAtHour(day, timeSlot).time }}</p>
                <p class="class-info">{{ getClassAtHour(day, timeSlot).class }} ({{ getClassAtHour(day,
                  timeSlot).studentCount }} students)</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Schedule Details Modal -->
    <div v-if="selectedClass" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>My Class Details</h2>
          <button class="close-btn" @click="closeModal">&times;</button>
        </div>
        <div class="modal-body">
          <div class="schedule-info">
            <p><strong>Subject Code:</strong> {{ selectedClass.subjectCode }}</p>
            <p><strong>Descriptive Title:</strong> {{ selectedClass.subject }}</p>
            <p><strong>Day:</strong> {{ selectedClass.day }}</p>
            <p><strong>Time:</strong> {{ selectedClass.time }}</p>
            <p><strong>Room:</strong> {{ selectedClass.room }}</p>
            <p><strong>Class:</strong> {{ selectedClass.class }}</p>
            <p><strong>Students:</strong> {{ selectedClass.studentCount }}</p>
          </div>
          <div class="actions">
            <button class="view-class-list-btn" @click="showClassList(selectedClass)">View Class List</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Class List Modal -->
    <div v-if="showClassListModal" class="modal-overlay" @click="closeClassListModal">
      <div class="modal-content class-list-modal" @click.stop>
        <div style="position: relative;">
          <button class="close-btn" @click="closeClassListModal" style="position: absolute; right: 0; top: 0;">&times;</button>
        </div>
        <div class="modal-body">
          <div class="class-info-header">
            <div class="info-grid">
              <div class="info-item">
                <p><strong>Descriptive Title:</strong> {{ selectedClass.subject }}</p>
                <p><strong>Class:</strong> {{ selectedClass.class }}</p>
                <p><strong>Room:</strong> {{ selectedClass.room }}</p>
              </div>
              <div class="info-item">
                <p><strong>Subject Code:</strong> {{ selectedClass.subjectCode }}</p>
                <p><strong>School Year:</strong> {{ selectedClass.schoolYear || '2024-2025' }}</p>
                <p><strong>Schedule:</strong> {{ selectedClass.day }} {{ selectedClass.time }}</p>
              </div>
            </div>
          </div>
          <div class="actions">
            <div class="search-container">
              <input type="text" v-model="searchQuery" placeholder="Search" class="search-input">
            </div>
            <div class="export-container">
              <select v-model="selectedExportFormat" class="export-format-select">
                <option value="csv">Export as CSV</option>
                <option value="docx">Export as DOCX</option>
              </select>
              <button class="export-btn" @click="exportClassList">Export</button>
            </div>
          </div>
          <div class="student-list">
            <table class="student-table">
              <thead>
                <tr>
                  <th>Student ID</th>
                  <th>Last Name</th>
                  <th>First Name</th>
                  <th>Email</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="student in filteredStudents" :key="student.id">
                  <td>{{ student.id }}</td>
                  <td>{{ student.lastName }}</td>
                  <td>{{ student.firstName }}</td>
                  <td>{{ student.email }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { jsPDF } from 'jspdf';
import html2canvas from 'html2canvas';

const filipinoNames = [
  { lastName: "Dela Cruz", firstName: "Juan" },
  { lastName: "Reyes", firstName: "Maria" },
  { lastName: "Santos", firstName: "Jose" },
  { lastName: "Garcia", firstName: "Ana" },
  { lastName: "Bautista", firstName: "Antonio" },
  { lastName: "Fernandez", firstName: "Carmen" },
  { lastName: "Aquino", firstName: "Manuel" },
  { lastName: "Cruz", firstName: "Rosa" },
  { lastName: "Gonzales", firstName: "Pedro" },
  { lastName: "Lopez", firstName: "Teresa" },
  { lastName: "Martinez", firstName: "Francisco" },
  { lastName: "Torres", firstName: "Sofia" },
  { lastName: "Romero", firstName: "Carlos" },
  { lastName: "Villanueva", firstName: "Isabel" },
  { lastName: "Rivera", firstName: "Miguel" },
  { lastName: "Castillo", firstName: "Elena" },
  { lastName: "Ocampo", firstName: "Ramon" },
  { lastName: "Salazar", firstName: "Lourdes" },
  { lastName: "Mendoza", firstName: "Alfredo" },
  { lastName: "Ramos", firstName: "Consuelo" },
  { lastName: "Alvarez", firstName: "Ricardo" },
  { lastName: "Chavez", firstName: "Patricia" },
  { lastName: "Dizon", firstName: "Fernando" },
  { lastName: "Espino", firstName: "Guadalupe" },
  { lastName: "Flores", firstName: "Eduardo" },
  { lastName: "Gutierrez", firstName: "Rosario" },
  { lastName: "Hernandez", firstName: "Roberto" },
  { lastName: "Ignacio", firstName: "Amparo" },
  { lastName: "Jimenez", firstName: "Arturo" },
  { lastName: "Katigbak", firstName: "Beatriz" },
  { lastName: "Lim", firstName: "Ernesto" },
  { lastName: "Navarro", firstName: "Dolores" },
  { lastName: "Ortega", firstName: "Felipe" },
  { lastName: "Panganiban", firstName: "Rebecca" },
  { lastName: "Quizon", firstName: "Gregorio" },
  { lastName: "Rubio", firstName: "Victoria" }
];
export default {
  name: 'InstructorSchedule',
  data() {
    return {
      daysOfWeek: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
      subjectColors: {
        'Calculus': '#4CAF50',
        'Advance Databases': '#2196F3',
        'Network Security': '#9C27B0',
        'Special Topics': '#FF5722',
        'Web Systems and Technologies': '#00BCD4',
        'Fundamentals of Computing': '#E91E63',
        'Application Development': '#4CAF50',
        'Data Structures': '#FFC107'
      },
      schedule: [
        // Professor Johnson's schedule
        {
          id: 1,
          subject: 'Network Security',
          subjectCode: 'NETSEC-101',
          day: 'Tuesday',
          time: '8:00-10:00 AM',
          room: 'IT-401',
          class: 'BSIT-4A',
          studentCount: 32,
          duration: 5, // 2 hours = 4 slots (30 min each)
          startHour: 8,
          endHour: 10,
          timeColor: '#9C27B0',
          schoolYear: '2023-2024'
        },
        {
          id: 2,
          subject: 'Application Development',
          subjectCode: 'APPDEV-201',
          day: 'Thursday',
          time: '8:00-10:00 AM',
          room: 'IT-402',
          class: 'BSCS-3B',
          studentCount: 28,
          duration: 5, // 2 hours
          startHour: 8,
          endHour: 10,
          timeColor: '#4CAF50',
          schoolYear: '2023-2024'
        },
        {
          id: 3,
          subject: 'Application Development',
          subjectCode: 'APPDEV-201',
          day: 'Sunday',
          time: '1:00-3:00 PM',
          room: 'IT-502',
          class: 'BSCS-3A',
          studentCount: 30,
          duration: 5, // 2 hours
          startHour: 13,
          endHour: 15,
          timeColor: '#4CAF50',
          schoolYear: '2023-2024'
        },

        // Professor Martinez's schedule
        {
          id: 5,
          subject: 'Data Structures',
          subjectCode: 'DS-101',
          day: 'Monday',
          time: '1:00-3:00 PM',
          room: 'IT-303',
          class: 'BSIT-2C',
          studentCount: 35,
          duration: 5, // 2 hours
          startHour: 13,
          endHour: 15,
          timeColor: '#FFC107',
          schoolYear: '2023-2024'
        },
        {
          id: 6,
          subject: 'Data Structures',
          subjectCode: 'DS-101',
          day: 'Wednesday',
          time: '1:00-3:00 PM',
          room: 'IT-304',
          class: 'BSIT-2D',
          studentCount: 33,
          duration: 5, // 2 hours
          startHour: 13,
          endHour: 15,
          timeColor: '#FFC107',
          schoolYear: '2023-2024'
        },
        {
          id: 7,
          subject: 'Data Structures',
          subjectCode: 'DS-101',
          day: 'Sunday',
          time: '9:00-11:00 AM',
          room: 'IT-304',
          class: 'BSIT-2A',
          studentCount: 36,
          duration: 5, // 2 hours
          startHour: 9,
          endHour: 11,
          timeColor: '#FFC107',
          schoolYear: '2023-2024'
        },
      ],
      selectedClass: null,
      showClassListModal: false,
      studentsList: [],
      selectedExportFormat: 'csv'
    }
  },
  computed: {
    timeSlots() {
      const slots = [];
      // Create time slots from 7:00 AM to 7:00 PM in 30-minute increments
      for (let hour = 7; hour <= 19; hour++) {
        slots.push(hour + 0.0); // :00
        slots.push(hour + 0.5); // :30
      }
      return slots;
    },
    filteredStudents() {
      if (!this.searchQuery) return this.studentsList;

      const query = this.searchQuery.toLowerCase();
      return this.studentsList.filter(student =>
        student.lastName.toLowerCase().includes(query) ||
        student.firstName.toLowerCase().includes(query) ||
        student.id.toLowerCase().includes(query)
      );
    }
  },

  methods: {
    getClassAtHour(day, timeSlot) {
      const classItem = this.schedule.find(item =>
        item.day === day &&
        timeSlot >= item.startHour &&
        timeSlot < item.endHour
      );

      if (classItem && !classItem.timeColor) {
        classItem.timeColor = this.subjectColors[classItem.subject] || '#6c757d';
      }

      return classItem;
    },
    shouldShowClass(day, timeSlot) {
      const classItem = this.getClassAtHour(day, timeSlot);
      if (!classItem) return false;

      return timeSlot === classItem.startHour;
    },
    calculateHeight(day, timeSlot) {
      const classItem = this.getClassAtHour(day, timeSlot);
      if (!classItem) return '0px';

      // Each 30-minute slot is 30px tall
      return `${classItem.duration * 30}px`;
    },
    calculateTopOffset(day, timeSlot) {
      return '0px';
    },
    formatTime(timeSlot) {
      const hour = Math.floor(timeSlot);
      const minute = (timeSlot % 1) * 60;
      const isPM = hour >= 12;
      const formattedHour = hour % 12 || 12;
      return `${formattedHour}:${minute === 0 ? '00' : '30'} ${isPM ? 'PM' : 'AM'}`;
    },
    showScheduleDetails(classItem) {
      if (!classItem) return;
      this.selectedClass = classItem;
    },

    closeModal() {
      this.selectedClass = null;
    },

    showClassList(classItem) {
      if (!classItem) return;
      this.selectedClass = classItem;
      this.studentsList = this.generateStudentList(classItem.studentCount);
      this.showClassListModal = true;
    },

    closeClassListModal() {
      this.showClassListModal = false;
      this.studentsList = [];
    },

    exportClassList() {
      switch (this.selectedExportFormat) {
        case 'csv':
          this.exportAsCSV();
          break;
        case 'docx':
          this.exportAsDOCX();
          break;
      }
    },

    generateStudentList(count) {
      const students = [];
      // Use the Filipino names array and cycle through it if needed
      for (let i = 1; i <= count; i++) {
        const nameIndex = (i - 1) % filipinoNames.length;
        const name = filipinoNames[nameIndex];

        students.push({
          id: `21-${(1760 + i).toString().padStart(4, '0')}`,
          lastName: name.lastName,
          firstName: name.firstName,
          email: `${name.firstName.toLowerCase()}.${name.lastName.toLowerCase().replace(/\s+/g, '')}@example.com`
        });
      }
      return students;
    },

    exportToPdf() {
      // Show loading toast
      this.$toast.add({
        severity: 'info',
        summary: 'Generating PDF',
        detail: 'Please wait while we generate your schedule',
        life: 3000
      });

      const element = document.querySelector('.schedule-grid');
      const opt = {
        margin: 10,
        filename: 'teaching-schedule.pdf',
        image: {
          type: 'jpeg',
          quality: 0.98
        },
        html2canvas: {
          scale: 2,
          useCORS: true,
          logging: true,
          allowTaint: true
        },
        jsPDF: {
          unit: 'mm',
          format: 'a3',
          orientation: 'landscape'
        }
      };

      // Generate PDF
      html2canvas(element, {
        scale: opt.html2canvas.scale,
        useCORS: opt.html2canvas.useCORS,
        allowTaint: opt.html2canvas.allowTaint,
        logging: opt.html2canvas.logging
      }).then(canvas => {
        const imgData = canvas.toDataURL('image/jpeg', opt.image.quality);
        const pdf = new jsPDF({
          orientation: opt.jsPDF.orientation,
          unit: opt.jsPDF.unit,
          format: opt.jsPDF.format
        });

        const imgProps = pdf.getImageProperties(imgData);
        const pdfWidth = pdf.internal.pageSize.getWidth();
        const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width;

        pdf.addImage(imgData, 'JPEG', 0, 0, pdfWidth, pdfHeight);
        pdf.save(opt.filename);

        this.$toast.add({
          severity: 'success',
          summary: 'Success',
          detail: 'Teaching schedule downloaded successfully!',
          life: 3000
        });
      }).catch(err => {
        console.error('Error generating PDF:', err);
        this.$toast.add({
          severity: 'error',
          summary: 'Error',
          detail: 'Failed to generate PDF. Please try again.',
          life: 5000
        });
      });
    },

    exportAsCSV() {
      const classInfo = {
        subjectCode: this.selectedClass.subjectCode,
        subjectName: this.selectedClass.subject,
        course: this.selectedClass.class || 'N/A',
        schoolYear: this.selectedClass.schoolYear || '2024-2025',
        year: 'N/A',
        section: 'N/A'
      };

      const csvContent = [
        ['Subject Code', 'Subject Name', 'Course', 'School Year', 'Year', 'Section', '', '', ''],
        [classInfo.subjectCode, classInfo.subjectName, classInfo.course, classInfo.schoolYear, classInfo.year, classInfo.section, '', '', ''],
        [''],
        ['Student ID', 'Last Name', 'First Name', 'Email'],
        ...this.studentsList.map(student => [
          student.id,
          student.lastName,
          student.firstName,
          student.email
        ])
      ].map(row => row.join(',')).join('\n');

      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
      const link = document.createElement('a');
      const url = URL.createObjectURL(blob);

      link.setAttribute('href', url);
      link.setAttribute('download', `${classInfo.subjectCode}_${classInfo.course}_classlist.csv`);

      link.style.visibility = 'hidden';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    },

    exportAsDOCX() {
      import('docx').then(docx => {
        const { Packer, Document, Paragraph, Table, TableCell, TableRow } = docx;

        const classInfo = {
          subjectCode: this.selectedClass.subjectCode,
          subjectName: this.selectedClass.subject,
          course: this.selectedClass.class || 'N/A',
          schoolYear: this.selectedClass.schoolYear || '2024-2025',
          year: 'N/A',
          section: 'N/A'
        };

        const doc = new Document({
          sections: [{
            children: [
              new Paragraph(`Subject Code: ${classInfo.subjectCode}`),
              new Paragraph(`Subject Name: ${classInfo.subjectName}`),
              new Paragraph(`Course: ${classInfo.course}`),
              new Paragraph(`School Year: ${classInfo.schoolYear}`),
              new Paragraph(`Year: ${classInfo.year}`),
              new Paragraph(`Section: ${classInfo.section}`),
              new Paragraph(''),
              new Table({
                rows: [
                  new TableRow({
                    children: [
                      new TableCell({ children: [new Paragraph('Student ID')] }),
                      new TableCell({ children: [new Paragraph('Last Name')] }),
                      new TableCell({ children: [new Paragraph('First Name')] }),
                      new TableCell({ children: [new Paragraph('Email')] })
                    ]
                  }),
                  ...this.studentsList.map(student =>
                    new TableRow({
                      children: [
                        new TableCell({ children: [new Paragraph(student.id)] }),
                        new TableCell({ children: [new Paragraph(student.lastName)] }),
                        new TableCell({ children: [new Paragraph(student.firstName)] }),
                        new TableCell({ children: [new Paragraph(student.email)] })
                      ]
                    })
                  )
                ]
              })
            ]
          }]
        });

        Packer.toBlob(doc).then(blob => {
          const link = document.createElement('a');
          const url = URL.createObjectURL(blob);

          link.setAttribute('href', url);
          link.setAttribute('download', `${classInfo.subjectCode}_${classInfo.course}_classlist.docx`);

          link.style.visibility = 'hidden';
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
        });
      });
    },
  },
  created() {
    this.schedule.forEach(item => {
      if (!item.timeColor) {
        item.timeColor = this.subjectColors[item.subject] || '#6c757d';
      }
    });
  }
}
</script>

<style scoped>
.schedule-container {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 6px rgba(125, 69, 69, 0.05);
}

.schedule-header {
  margin-bottom: 24px;
}

.schedule-header h2 {
  margin: 0 0 16px 0;
  color: #333;
}

.schedule-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 24px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.9rem;
}

.color-square {
  width: 12px;
  height: 12px;
  border-radius: 4px;
}

.schedule-grid {
  border: 1px solid #eee;
  min-height: 500px;
  position: relative;
}

.schedule-row {
  display: grid;
  grid-template-columns: 100px repeat(7, 1fr);
  border-bottom: 1px solid #eee;
  min-height: 30px;
  position: relative;
}

.header-row {
  font-weight: 600;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.time-column {
  padding: 6px;
  border-right: 1px solid #eee;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
}

.day-column {
  position: relative;
  min-height: 30px;
  overflow: visible;
  text-align: center;
  justify-content: center;
  align-items: center;
}

.schedule-item-container {
  position: relative;
  height: 100%;
  padding: 2px;
}

.schedule-item {
  position: absolute;
  top: 2px;
  bottom: 2px;
  left: 2px;
  right: 2px;
  border-radius: 4px;
  color: white;
  padding: 6px;
  box-sizing: border-box;
  transition: transform 0.2s;
  z-index: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  background-clip: padding-box;
  text-align: center;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.schedule-item-content {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 2px 0;
}

.schedule-item h4 {
  margin: 0 0 4px 0;
  font-size: 0.85rem;
  font-weight: 650;
  text-align: center;
}

.schedule-item p {
  margin: 2px 0;
  font-size: 0.75rem;
  opacity: 0.9;
  text-align: center;
}

.schedule-item .time {
  font-style: italic;
}

.schedule-item .room {
  font-weight: 500;
}

.class-info {
  font-size: 0.75rem !important;
  margin-top: 4px !important;
}

.schedule-item.clickable {
  cursor: pointer;
  transition: transform 0.2s;
}

.schedule-item.clickable:hover {
  transform: scale(1.02);
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: #fff;
  padding: 20px;
  border-radius: 10px;
  width: 30%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 15px;
  margin-bottom: 15px;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.8rem;
}

.close-btn {
  display: flex;
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  padding: 8px;
  color: #666;
  z-index: 1;
}

.close-btn:hover {
  color: #333;
}

.modal-body {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.schedule-info {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.schedule-info p {
  margin: 0;
}

.schedule-info strong {
  color: #333;
}

.actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
}

.view-class-list-btn {
  background-color: #10b981;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
  align-items: center;
  justify-content: center;
}

.view-class-list-btn:hover {
  background-color: #0d9f6e;
}

.class-info-header {
  margin-bottom: 1.5rem;
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.info-item p {
  margin: 0;
  padding: 0.25rem 0;
}

.student-list {
  margin-bottom: 20px;
}

.student-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

.student-table th,
.student-table td {
  border: 1px solid #dee2e6;
  padding: 8px;
  text-align: left;
  border-bottom: 1px solid #e0e0e0;
  white-space: nowrap;
}

.student-table th {
  background-color: #f8f9fa;
  font-weight: 600;
}

.actions {
  display: flex;
  justify-content: center;
  gap: 10px;
}

.export-format-select {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.export-btn {
  background-color: #10b981;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.export-btn:hover {
  background-color: #0d9f6e;
}

.class-list-modal {
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
}

.search-container {
  flex: 1;
  width: 80%;
}

.search-input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.export-container {
  display: flex;
  align-items: center;
  gap: 10px;
}

.student-table th,
.student-table td {
  padding: 10px 12px;
}

.student-list {
  max-height: 60vh;
  overflow-y: auto;
  margin-bottom: 0;
}

.schedule-grid>.schedule-row.header-row {
  display: grid;
  grid-template-columns: 100px repeat(7, 1fr);
  background-color: #f8f9fa;
  font-weight: 600;
  height: 40px;
  margin: 0;
  padding: 0;
  border-bottom: 2px solid #dee2e6;
}

.schedule-grid>.schedule-row.header-row>.time-column,
.schedule-grid>.schedule-row.header-row>.day-column {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 8px 4px;
  border-right: 1px solid #eee;
  font-size: 0.85rem;
}

.schedule-grid>.schedule-row.header-row>.day-column:last-child {
  border-right: none;
}

.header-row:not(.schedule-grid .header-row) {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>