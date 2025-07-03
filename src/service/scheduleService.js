import { ref } from 'vue';

export const useScheduleService = () => {
  const scheduleData = ref({
    instructor: [
      // Professor Johnson's schedule
      { 
        id: 1, 
        subject: 'Network Security', 
        day: 'Tuesday', 
        time: '8:00-10:00 AM', 
        room: 'IT-401', 
        class: 'BSIT-4A',
        studentCount: 32,
        duration: 2,
        startHour: 8,
        endHour: 10
      },
      // Add other instructor schedules
    ],
    student: {
      // Student schedules will be dynamically populated
      schedules: {}
    }
  });

  const getInstructorSchedule = () => scheduleData.value.instructor;
  const getStudentSchedule = (studentId) => scheduleData.value.student.schedules[studentId];

  const addInstructorClass = (classData) => {
    scheduleData.value.instructor.push(classData);
  };

  const addStudentSchedule = (studentId, schedule) => {
    if (!scheduleData.value.student.schedules[studentId]) {
      scheduleData.value.student.schedules[studentId] = [];
    }
    scheduleData.value.student.schedules[studentId].push(schedule);
  };

  return {
    getInstructorSchedule,
    getStudentSchedule,
    addInstructorClass,
    addStudentSchedule
  };
};