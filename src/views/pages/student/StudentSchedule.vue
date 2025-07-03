<template>
  <div class="schedule-container">
    <div class="schedule-header">
      <div class="header-row">
        <h2>My Schedules</h2>
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
          <div class="schedule-item-container">
            <div v-if="shouldShowClass(day, timeSlot)" class="schedule-item"
              :class="{ 'break': getClassAtHour(day, timeSlot).isBreak }" :style="{
                backgroundColor: getClassAtHour(day, timeSlot).isBreak
                  ? '#f8f9fa'
                  : getClassAtHour(day, timeSlot).timeColor,
                height: calculateHeight(day, timeSlot),
                top: calculateTopOffset(day, timeSlot)
              }">
              <div v-if="!getClassAtHour(day, timeSlot).isBreak" class="schedule-item-content">
                <h4>{{ getClassAtHour(day, timeSlot).subject }}</h4>
                <p class="room">Room: {{ getClassAtHour(day, timeSlot).room }}</p>
                <p class="time">{{ getClassAtHour(day, timeSlot).time }}</p>
                <p class="instructor">Instructor: {{ getClassAtHour(day, timeSlot).instructor }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { jsPDF } from 'jspdf';
import html2canvas from 'html2canvas';

export default {
  name: 'StudentSchedule',
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
        // Monday
        {
          id: 1,
          subject: 'Calculus',
          day: 'Monday',
          time: '8:00-9:30 AM',
          room: 'IT-101',
          instructor: 'Prof. Santos',
          duration: 4, // 1.5 hours = 3 slots (30 min each)
          startHour: 8,
          endHour: 9.5,
          timeColor: '#4CAF50'
        },
        {
          id: 3,
          subject: 'Data Structures',
          day: 'Monday',
          time: '2:00-4:00 PM',
          room: 'IT-303',
          instructor: 'Prof. Martinez',
          duration: 5, // 2 hours = 4 slots
          startHour: 14,
          endHour: 16,
          timeColor: '#FFC107'
        },

        // Tuesday
        {
          id: 4,
          subject: 'Network Security',
          day: 'Tuesday',
          time: '7:00-8:30 AM',
          room: 'IT-401',
          instructor: 'Prof. Angheles',
          duration: 4, // 1.5 hours
          startHour: 7,
          endHour: 8.5,
          timeColor: '#9C27B0'
        },
        {
          id: 6,
          subject: 'Web Systems and Technologies',
          day: 'Tuesday',
          time: '1:00-2:30 PM',
          room: 'IT-603',
          instructor: 'Prof. Cruz',
          duration: 4, // 1.5 hours
          startHour: 13,
          endHour: 14.5,
          timeColor: '#00BCD4'
        },

        // Wednesday
        {
          id: 7,
          subject: 'Fundamentals of Computing',
          day: 'Wednesday',
          time: '9:00-10:00 AM',
          room: 'IT-102',
          instructor: 'Prof. Ramos',
          duration: 3, // 1.5 hours
          startHour: 9,
          endHour: 10,
          timeColor: '#E91E63'
        },
        {
          id: 9,
          subject: 'Data Structures',
          day: 'Wednesday',
          time: '3:00-5:00 PM',
          room: 'IT-304',
          instructor: 'Prof. Martinez',
          duration: 5, // 2.5 hours
          startHour: 15,
          endHour: 17,
          timeColor: '#FFC107'
        },

        // Thursday
        {
          id: 10,
          subject: 'Application Development',
          day: 'Thursday',
          time: '10:00-12:30 PM',
          room: 'IT-402',
          instructor: 'Prof. Angheles',
          duration: 6, // 2.5 hours
          startHour: 10,
          endHour: 12.5,
          timeColor: '#4CAF50'
        },

        // Saturday
        {
          id: 11,
          subject: 'Special Topics',
          day: 'Saturday',
          time: '9:00-10:30 AM',
          room: 'IT-201',
          instructor: 'Prof. Rodriguez',
          duration: 4, // 1.5 hours
          startHour: 9,
          endHour: 10.5,
          timeColor: '#FF5722'
        },
        {
          id: 12,
          subject: 'Web Systems and Technologies',
          day: 'Saturday',
          time: '2:00-3:30 PM',
          room: 'IT-403',
          instructor: 'Prof. Cruz',
          duration: 4, // 1.5 hours
          startHour: 14,
          endHour: 15.5,
          timeColor: '#00BCD4'
        },

        // Sunday
        {
          id: 13,
          subject: 'Data Structures',
          day: 'Sunday',
          time: '7:00-9:00 AM',
          room: 'IT-304',
          instructor: 'Prof. Martinez',
          duration: 5, // 2 hours
          startHour: 7,
          endHour: 9,
          timeColor: '#FFC107'
        },
        {
          id: 14,
          subject: 'Application Development',
          day: 'Sunday',
          time: '5:30-7:30 PM',
          room: 'IT-502',
          instructor: 'Prof. Angheles',
          duration: 5, // 2 hours
          startHour: 17.5,
          endHour: 19,
          timeColor: '#4CAF50'
        },
      ]
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
    }
  },
  methods: {
    getClassAtHour(day, timeSlot) {
      const classItem = this.schedule.find(item =>
        item.day === day &&
        timeSlot >= item.startHour &&
        timeSlot < item.endHour
      );

      if (classItem && !classItem.timeColor && !classItem.isBreak) {
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
        filename: 'my-schedule.pdf',
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
          detail: 'Schedule downloaded successfully!',
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
  },
  created() {
    this.schedule.forEach(item => {
      if (!item.timeColor && !item.isBreak) {
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
  padding: 24px;
  box-shadow: 0 4px 6px rgba(125, 69, 69, 0.05);
}

.header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
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

.schedule-grid>.schedule-row.header-row {
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

.time-column {
  padding: 6px;
  border-right: 1px solid #eee;
  font-weight: 500;
  display: flex;
  align-items: center;
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
  display: flex;
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
  font-size: 0.75rem;
  box-sizing: border-box;
  transition: transform 0.2s;
  z-index: 1;
  /* column line */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  overflow: hidden;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.schedule-item-content {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 2px 0;
  gap: 5px;
}

.schedule-item h4 {
  margin: 0;
  font-size: 0.80rem;
  font-weight: 650;
  line-height: 1.1;
}

.schedule-item p {
  margin: 0;
  font-size: 0.75rem;
  line-height: 1.1;
  opacity: 0.9;
}

.schedule-item .time {
  font-style: italic;
  font-size: 0.75rem;
}

.schedule-item .room {
  font-weight: 500;
}

.schedule-item .instructor {
  font-weight: 500;
}
</style>