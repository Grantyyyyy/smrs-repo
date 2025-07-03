<template>
  <div class="office-portal">
    <!-- Office Selection (for admin view) -->
    <div v-if="!selectedOffice" class="office-selection">
      <h2>Select Office</h2>
      <div class="office-list">
        <div 
          v-for="office in offices" 
          :key="office.id"
          @click="selectOffice(office.id)"
          class="office-item"
        >
          <i :class="office.icon" class="mr-2"></i>
          {{ office.name }}
        </div>
      </div>
    </div>

    <!-- Student Search (for the selected office) -->
    <div v-else class="office-clearance-view">
      <button class="back-btn" @click="selectedOffice = null">
        <i class="pi pi-arrow-left mr-2"></i> Back to Office Selection
      </button>
      
      <div class="student-search">
        <span class="p-input-icon-left w-full">
          <i class="pi pi-search" />
          <InputText 
            v-model="searchQuery" 
            placeholder="Search by student name or ID"
            @input="searchStudents"
            class="w-full"
          />
        </span>
      </div>

      <div class="student-list">
        <div 
          v-for="student in filteredStudents" 
          :key="student.id"
          @click="selectStudent(student)"
          class="student-item"
        >
          <div class="student-info">
            <div class="student-name">{{ student.lastName }}, {{ student.firstName }}</div>
            <div class="student-id">{{ student.id }}</div>
          </div>
          <div class="student-status" :class="getStatusClass(student.clearanceStatus)">
            {{ student.clearanceStatus || 'Not Started' }}
          </div>
        </div>
      </div>

      <!-- Office Clearance Form for Selected Student -->
      <OfficeClearance 
        v-if="selectedStudent"
        :student="selectedStudent"
        :office-type="selectedOffice"
        @approved="onClearanceApproved"
      />
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue';
import { useToast } from 'primevue/usetoast';
import OfficeClearance from './OfficeClearance.vue';
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';

export default {
  name: 'OfficePortal',
  components: {
    OfficeClearance,
    InputText,
    Button
  },
  setup() {
    const toast = useToast();
    const selectedOffice = ref(null);
    const selectedStudent = ref(null);
    const searchQuery = ref('');
    
    const offices = [
      { id: 'cashier', name: 'Cashier Office', icon: 'pi pi-money-bill' },
      { id: 'library', name: 'Library', icon: 'pi pi-book' },
      { id: 'clinic', name: 'Clinic', icon: 'pi pi-heart' },
      { id: 'guidance', name: 'Guidance Office', icon: 'pi pi-users' },
      { id: 'canteen', name: 'Canteen', icon: 'pi pi-utensils' },
      { id: 'student-council', name: 'Student Council', icon: 'pi pi-users' },
      { id: 'osas-staff', name: 'OSAS Staff', icon: 'pi pi-user' },
      { id: 'osas-director', name: 'OSAS Director', icon: 'pi pi-user-tie' }
    ];

    // Mock data - in a real app, this would come from an API
    const students = ref([
      {
        id: '2023-1001',
        firstName: 'Juan',
        lastName: 'Dela Cruz',
        course: 'BS Computer Science',
        yearLevel: 3,
        clearanceStatus: 'Pending'
      },
      {
        id: '2023-1002',
        firstName: 'Maria',
        lastName: 'Santos',
        course: 'BS Information Technology',
        yearLevel: 2,
        clearanceStatus: 'Cleared'
      },
      {
        id: '2023-1003',
        firstName: 'Pedro',
        lastName: 'Reyes',
        course: 'BS Information Systems',
        yearLevel: 4,
        clearanceStatus: 'Not Started'
      }
    ]);

    const filteredStudents = computed(() => {
      if (!searchQuery.value) {
        return students.value;
      }
      const query = searchQuery.value.toLowerCase();
      return students.value.filter(student => 
        student.firstName.toLowerCase().includes(query) ||
        student.lastName.toLowerCase().includes(query) ||
        student.id.toLowerCase().includes(query)
      );
    });

    const selectOffice = (officeId) => {
      selectedOffice.value = officeId;
      selectedStudent.value = null;
      searchQuery.value = '';
    };

    const selectStudent = (student) => {
      selectedStudent.value = student;
    };

    const onClearanceApproved = () => {
      // Update the student's status in the list
      const studentIndex = students.value.findIndex(s => s.id === selectedStudent.value.id);
      if (studentIndex !== -1) {
        students.value[studentIndex].clearanceStatus = 'Cleared';
      }
      
      toast.add({
        severity: 'success',
        summary: 'Success',
        detail: 'Clearance approved successfully',
        life: 3000
      });
      
      // Deselect the student
      selectedStudent.value = null;
    };

    const getStatusClass = (status) => {
      return {
        'status-pending': status === 'Pending',
        'status-cleared': status === 'Cleared',
        'status-not-started': !status || status === 'Not Started'
      };
    };

    return {
      offices,
      selectedOffice,
      selectedStudent,
      searchQuery,
      filteredStudents,
      selectOffice,
      selectStudent,
      onClearanceApproved,
      getStatusClass
    };
  }
};
</script>

<style scoped>
.office-portal {
  padding: 1.5rem;
  max-width: 1200px;
  margin: 0 auto;
}

.office-selection {
  text-align: center;
}

.office-selection h2 {
  margin-bottom: 2rem;
  color: #2c3e50;
}

.office-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.office-item {
  padding: 1.5rem;
  background-color: #ffffff;
  border-radius: 0.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #e5e7eb;
}

.office-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-color: #3b82f6;
}

.office-item i {
  font-size: 1.25rem;
  color: #3b82f6;
}

.student-search {
  margin: 1.5rem 0;
  max-width: 500px;
}

.student-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
  margin-top: 1.5rem;
}

.student-item {
  padding: 1rem;
  background-color: #ffffff;
  border-radius: 0.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.student-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-color: #3b82f6;
}

.student-info {
  flex: 1;
}

.student-name {
  font-weight: 600;
  color: #1f2937;
}

.student-id {
  font-size: 0.875rem;
  color: #6b7280;
}

.student-status {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: capitalize;
}

.status-pending {
  background-color: #fef3c7;
  color: #92400e;
}

.status-cleared {
  background-color: #dcfce7;
  color: #166534;
}

.status-not-started {
  background-color: #f3f4f6;
  color: #4b5563;
}

.back-btn {
  display: inline-flex;
  align-items: center;
  padding: 0.5rem 1rem;
  background-color: #f3f4f6;
  color: #4b5563;
  border: 1px solid #e5e7eb;
  border-radius: 0.375rem;
  cursor: pointer;
  font-weight: 500;
  margin-bottom: 1.5rem;
  transition: all 0.2s;
}

.back-btn:hover {
  background-color: #e5e7eb;
}

.back-btn i {
  margin-right: 0.5rem;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .office-list {
    grid-template-columns: 1fr;
  }
  
  .student-list {
    grid-template-columns: 1fr;
  }
}
</style>