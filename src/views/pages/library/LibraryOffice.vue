<template>
  <div class="library-office">
    <office-student-list 
      :office-name="officeName"
      :clearance-component="clearanceComponent"
      :students="students"
      :is-read-only="isReadOnly"
    />
  </div>
</template>

<script>
import { ref, defineAsyncComponent } from 'vue';
import OfficeStudentList from '../clearance/OfficeStudentList.vue';

// Lazy load the LibraryClearance component
const LibraryClearance = defineAsyncComponent(() => 
  import('../clearance/LibraryClearance.vue')
);

export default {
  name: 'LibraryOffice',
  components: {
    OfficeStudentList
  },
  setup() {
    const officeName = 'Library';
    const clearanceComponent = LibraryClearance;
    const isReadOnly = false;

    // Mock data for development
    const students = ref([
      {
        id: '2023-1001',
        firstName: 'Juan',
        lastName: 'Dela Cruz',
        course: 'Bachelor of Science in Computer Science',
        yearLevel: 3,
        clearanceStatus: 'Pending',
        requirements: [
          { description: 'Returned all borrowed books', cleared: true },
          { description: 'Paid all library fines', cleared: true },
          { description: 'Cleared library card', cleared: false },
          { description: 'No pending book reservations', cleared: false }
        ]
      },
      {
        id: '2023-1002',
        firstName: 'Maria',
        lastName: 'Santos',
        course: 'Bachelor of Science in Information Technology',
        yearLevel: 2,
        clearanceStatus: 'Cleared',
        requirements: [
          { description: 'Returned all borrowed books', cleared: true },
          { description: 'Paid all library fines', cleared: true },
          { description: 'Cleared library card', cleared: true },
          { description: 'No pending book reservations', cleared: true }
        ]
      },
      {
        id: '2023-1003',
        firstName: 'Pedro',
        lastName: 'Reyes',
        course: 'Bachelor of Science in Information Systems',
        yearLevel: 4,
        clearanceStatus: 'Not Started',
        requirements: [
          { description: 'Returned all borrowed books', cleared: false },
          { description: 'Paid all library fines', cleared: false },
          { description: 'Cleared library card', cleared: false },
          { description: 'No pending book reservations', cleared: false }
        ]
      },
      {
        id: '2023-1004',
        firstName: 'Ana',
        lastName: 'Gonzales',
        course: 'Bachelor of Science in Computer Engineering',
        yearLevel: 1,
        clearanceStatus: 'Pending',
        requirements: [
          { description: 'Returned all borrowed books', cleared: true },
          { description: 'Paid all library fines', cleared: true },
          { description: 'Cleared library card', cleared: false },
          { description: 'No pending book reservations', cleared: false }
        ]
      },
      {
        id: '2023-1005',
        firstName: 'Jose',
        lastName: 'Ramos',
        course: 'Bachelor of Science in Computer Science',
        yearLevel: 3,
        clearanceStatus: 'Pending',
        requirements: [
          { description: 'Returned all borrowed books', cleared: true },
          { description: 'Paid all library fines', cleared: false },
          { description: 'Cleared library card', cleared: false },
          { description: 'No pending book reservations', cleared: false }
        ]
      }
    ]);

    return {
      officeName,
      clearanceComponent,
      students,
      isReadOnly
    };
  }
};
</script>

<style scoped>

</style>
