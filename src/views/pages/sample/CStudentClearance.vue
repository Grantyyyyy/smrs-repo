<template>
  <div class="clearance-container">
    <!-- Student Selection Interface -->
    <div v-if="!selectedStudent" class="student-selection">
      <h2>Select Student</h2>

      <div class="filter-row">
        <!-- Department Dropdown -->
        <div class="p-field filter-item">
          <span class="p-float-label">
            <Dropdown
              v-model="selectedDepartment"
              :options="departmentOptions"
              optionLabel=""
              placeholder="All Departments"
              class="w-full"
              @change="onDepartmentChange"
              :showClear="true"
            />
          </span>
        </div>

        <!-- Course Dropdown -->
        <div class="p-field filter-item">
          <span class="p-float-label">
            <Dropdown
              v-model="selectedCourse"
              :options="filteredCourseOptions"
              optionLabel=""
              placeholder="All Courses"
              class="w-full"
              @change="onCourseChange"
              :showClear="true"
            />
          </span>
        </div>

        <!-- Year Dropdown -->
        <div class="p-field filter-item">
          <span class="p-float-label">
            <Dropdown
              v-model="selectedYear"
              :options="[1, 2, 3, 4]"
              optionLabel=""
              placeholder="All Years"
              class="w-full"
              @change="filterStudents"
              :showClear="true"
            >
              <template #option="slotProps">
                {{ getYearLabel(slotProps.option) }}
              </template>
            </Dropdown>
          </span>
        </div>

        <!-- Search -->
        <div class="p-field filter-search">
          <span class="p-input-icon-left w-full">
            <InputText 
              v-model="searchQuery"
              @input="filterStudents"
              placeholder="Search"
              class="w-full"
            />
          </span>
        </div>
      </div>

      <div class="student-list">
        <!-- Table Headers -->
        <div class="student-list-header">
          <div class="header-item">Student ID</div>
          <div class="header-item">Last Name</div>
          <div class="header-item">First Name</div>
          <div class="header-item">Course</div>
          <div class="header-item">Year Level</div>
          <div class="header-item">Status</div>
          <div class="header-item">Actions</div>
        </div>
        
        <!-- Student List Items -->
        <div 
          v-for="student in filteredStudents" 
          :key="student.id" 
          @click="selectStudent(student)"
          class="student-item"
        >
          <div class="student-id">{{ student.id }}</div>
          <div class="student-lastname">{{ student.lastName }}</div>
          <div class="student-firstname">{{ student.firstName }}</div>
          <div class="student-course">{{ student.course }}</div>
          <div class="student-year">{{ getYearLabel(student.yearLevel) }}</div>
          <div class="student-status">
            <span :class="'status-badge ' + getStatusClass(student.status)">
              {{ getStatusLabel(student.status) }}
            </span>
          </div>
          <div class="student-actions" @click.stop>
            <Button 
              icon="pi pi-eye" 
              class="p-button-rounded p-button-text p-button-sm" 
              v-tooltip.top="'View Details'"
              @click="viewStudentClearance(student)"
            />
            <Button 
              icon="pi pi-pencil" 
              class="p-button-rounded p-button-text p-button-sm" 
              v-tooltip.top="'Edit Status'"
              @click="editStudentStatus(student)"
            />
          </div>
        </div>
      </div>
      
    </div>
    
    <!-- Clearance Form -->
    <ClearanceForm 
      v-else 
      :student="selectedStudent" 
      @back="clearSelection"
    />
    
    <!-- Clearance Status Dialog -->
    <Dialog 
      v-model:visible="statusDialog.visible" 
      :style="{width: '450px'}" 
      header="Update Clearance Status"
      :modal="true"
      class="p-fluid"
    >
      <div class="p-field">
        <label for="status">Status</label>
        <Dropdown
          id="status"
          v-model="statusDialog.status"
          :options="statusOptions"
          optionLabel="label"
          optionValue="value"
          placeholder="Select a status"
          class="w-full"
        />
      </div>
      <div class="p-field">
        <label for="notes">Notes (Optional)</label>
        <Textarea
          id="notes"
          v-model="statusDialog.notes"
          :autoResize="true"
          rows="3"
          class="w-full"
        />
      </div>
      <template #footer>
        <Button 
          label="Cancel" 
          icon="pi pi-times" 
          class="p-button-text" 
          @click="statusDialog.visible = false" 
        />
        <Button 
          label="Save" 
          icon="pi pi-check" 
          class="p-button-primary" 
          @click="saveStatus" 
        />
      </template>
    </Dialog>
  </div>
</template>

<script>
import ClearanceForm from './ClearanceForm.vue';
import Dropdown from 'primevue/dropdown';
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';
import Tooltip from 'primevue/tooltip';
import Dialog from 'primevue/dialog';
import Textarea from 'primevue/textarea';

export default {
  name: 'StudentClearance',
  directives: {
    'tooltip': Tooltip
  },
  components: {
    ClearanceForm,
    Dropdown,
    InputText,
    Button,
    Dialog,
    Textarea
  },
  data() {
    return {
      searchQuery: '',
      selectedDepartment: '',
      departmentOptions: [
        'College of Computer Studies',
        'College of Engineering',
        'College of Business Administration',
        'College of Education',
        'College of Arts and Sciences'
      ],
      selectedCourse: '',
      courseOptions: [
        { department: 'College of Computer Studies', name: 'Bachelor of Science in Computer Science' },
        { department: 'College of Computer Studies', name: 'Bachelor of Science in Information Technology' },
        // { department: 'College of Engineering', name: 'Bachelor of Science in Civil Engineering' },
        // { department: 'College of Engineering', name: 'Bachelor of Science in Electrical Engineering' },
        // { department: 'College of Business Administration', name: 'Bachelor of Science in Business Administration' },
        // { department: 'College of Education', name: 'Bachelor of Elementary Education' },
        // { department: 'College of Education', name: 'Bachelor of Secondary Education' },
        // { department: 'College of Arts and Sciences', name: 'Bachelor of Arts in Communication' },
        // { department: 'College of Arts and Sciences', name: 'Bachelor of Science in Psychology' }
      ],
      selectedYear: '',
      selectedStudent: null,
      allStudents: [
        // 1st Year
        { id: '2023-10001', firstName: 'Jose', lastName: 'Rizal', course: 'Bachelor of Science in Computer Science', yearLevel: 1, status: 'pending' },
        { id: '2023-10002', firstName: 'Andres', lastName: 'Bonifacio', course: 'Bachelor of Science in Information Technology', yearLevel: 1, status: 'in_review' },
        { id: '2023-10003', firstName: 'Emilio', lastName: 'Aguinaldo', course: 'Bachelor of Science in Computer Science', yearLevel: 1, status: 'approved' },
        { id: '2023-10004', firstName: 'Apolinario', lastName: 'Mabini', course: 'Bachelor of Science in Information Technology', yearLevel: 1, status: 'rejected' },
        { id: '2023-10005', firstName: 'Melchora', lastName: 'Aquino', course: 'Bachelor of Science in Computer Science', yearLevel: 1, status: 'on_hold' },
        { id: '2023-10006', firstName: 'Marcelo', lastName: 'Del Pilar', course: 'Bachelor of Science in Information Technology', yearLevel: 1, status: 'pending' },
        { id: '2023-10007', firstName: 'Gregoria', lastName: 'De Jesus', course: 'Bachelor of Science in Computer Science', yearLevel: 1, status: 'in_review' },
        { id: '2023-10008', firstName: 'Diego', lastName: 'Silang', course: 'Bachelor of Science in Information Technology', yearLevel: 1, status: 'approved' },
        { id: '2023-10009', firstName: 'Gabriela', lastName: 'Silang', course: 'Bachelor of Science in Computer Science', yearLevel: 1, status: 'rejected' },
        { id: '2023-10010', firstName: 'Juan', lastName: 'Luna', course: 'Bachelor of Science in Information Technology', yearLevel: 1, status: 'on_hold' },

        // 2nd Year
        { id: '2022-20001', firstName: 'Antonio', lastName: 'Luna', course: 'Bachelor of Science in Computer Science', yearLevel: 2, status: 'pending' },
        { id: '2022-20002', firstName: 'Trinidad', lastName: 'Tecson', course: 'Bachelor of Science in Information Technology', yearLevel: 2, status: 'in_review' },
        { id: '2022-20003', firstName: 'Manuel', lastName: 'Quezon', course: 'Bachelor of Science in Computer Science', yearLevel: 2, status: 'approved' },
        { id: '2022-20004', firstName: 'Sergio', lastName: 'Osmeña', course: 'Bachelor of Science in Information Technology', yearLevel: 2, status: 'rejected' },
        { id: '2022-20005', firstName: 'Elpidio', lastName: 'Quirino', course: 'Bachelor of Science in Computer Science', yearLevel: 2, status: 'on_hold' },
        { id: '2022-20006', firstName: 'Carlos', lastName: 'P. Garcia', course: 'Bachelor of Science in Information Technology', yearLevel: 2, status: 'pending' },
        { id: '2022-20007', firstName: 'Diosdado', lastName: 'Macapagal', course: 'Bachelor of Science in Computer Science', yearLevel: 2, status: 'in_review' },
        { id: '2022-20008', firstName: 'Corazon', lastName: 'Aquino', course: 'Bachelor of Science in Information Technology', yearLevel: 2, status: 'approved' },
        { id: '2022-20009', firstName: 'Ferdinand', lastName: 'Marcos', course: 'Bachelor of Science in Computer Science', yearLevel: 2, status: 'rejected' },
        { id: '2022-20010', firstName: 'Benigno', lastName: 'Aquino III', course: 'Bachelor of Science in Information Technology', yearLevel: 2, status: 'on_hold' },

        // 3rd Year
        { id: '2021-30001', firstName: 'Lapu-Lapu', lastName: 'Mactan', course: 'Bachelor of Science in Computer Science', yearLevel: 3, status: 'pending' },
        { id: '2021-30002', firstName: 'Rajah', lastName: 'Sulayman', course: 'Bachelor of Science in Information Technology', yearLevel: 3, status: 'in_review' },
        { id: '2021-30003', firstName: 'Miguel', lastName: 'Malvar', course: 'Bachelor of Science in Computer Science', yearLevel: 3, status: 'approved' },
        { id: '2021-30004', firstName: 'Macario', lastName: 'Sakay', course: 'Bachelor of Science in Information Technology', yearLevel: 3, status: 'rejected' },
        { id: '2021-30005', firstName: 'Agueda', lastName: 'Kahabagan', course: 'Bachelor of Science in Computer Science', yearLevel: 3, status: 'on_hold' },
        { id: '2021-30006', firstName: 'Josefa', lastName: 'Llanes Escoda', course: 'Bachelor of Science in Information Technology', yearLevel: 3, status: 'pending' },
        { id: '2021-30007', firstName: 'Vicente', lastName: 'Lim', course: 'Bachelor of Science in Computer Science', yearLevel: 3, status: 'in_review' },
        { id: '2021-30008', firstName: 'Artemio', lastName: 'Ricarte', course: 'Bachelor of Science in Information Technology', yearLevel: 3, status: 'approved' },
        { id: '2021-30009', firstName: 'Pio', lastName: 'Valenzuela', course: 'Bachelor of Science in Computer Science', yearLevel: 3, status: 'rejected' },
        { id: '2021-30010', firstName: 'Leona', lastName: 'Florentino', course: 'Bachelor of Science in Information Technology', yearLevel: 3, status: 'on_hold' },

        // 4th Year
        { id: '2020-40001', firstName: 'Juan', lastName: 'Dela Cruz', course: 'Bachelor of Science in Computer Science', yearLevel: 4, status: 'pending' },
        { id: '2020-40002', firstName: 'Maria', lastName: 'Santos', course: 'Bachelor of Science in Information Technology', yearLevel: 4, status: 'in_review' },
        { id: '2020-40003', firstName: 'Pedro', lastName: 'Penduko', course: 'Bachelor of Science in Computer Science', yearLevel: 4, status: 'approved' },
        { id: '2020-40004', firstName: 'Rosa', lastName: 'Rosales', course: 'Bachelor of Science in Information Technology', yearLevel: 4, status: 'rejected' },
        { id: '2020-40005', firstName: 'Tomas', lastName: 'Bautista', course: 'Bachelor of Science in Computer Science', yearLevel: 4, status: 'on_hold' },
        { id: '2020-40006', firstName: 'Isabel', lastName: 'Reyes', course: 'Bachelor of Science in Information Technology', yearLevel: 4, status: 'pending' },
        { id: '2020-40007', firstName: 'Crisostomo', lastName: 'Ibarra', course: 'Bachelor of Science in Computer Science', yearLevel: 4, status: 'in_review' },
        { id: '2020-40008', firstName: 'Simoun', lastName: 'Espadaña', course: 'Bachelor of Science in Information Technology', yearLevel: 4, status: 'approved' },
        { id: '2020-40009', firstName: 'Elias', lastName: 'Salonga', course: 'Bachelor of Science in Computer Science', yearLevel: 4, status: 'rejected' },
        { id: '2020-40010', firstName: 'Salome', lastName: 'Gomez', course: 'Bachelor of Science in Information Technology', yearLevel: 4, status: 'on_hold' },
      ],
      filteredStudents: [],
      statusDialog: {
        visible: false,
        student: null,
        status: null,
        notes: ''
      },
      statusOptions: [
        { label: 'Pending', value: 'pending' },
        { label: 'In Review', value: 'in_review' },
        { label: 'Approved', value: 'approved' },
        { label: 'Rejected', value: 'rejected' },
        { label: 'On Hold', value: 'on_hold' }
      ],
    }
  },
  computed: {
    filteredCourseOptions() {
      if (!this.selectedDepartment) {
        return [...new Set(this.courseOptions.map(course => course.name))];
      }
      return this.courseOptions
        .filter(course => course.department === this.selectedDepartment)
        .map(course => course.name);
    },
    filteredStudents() {
      const query = this.searchQuery.toLowerCase();
      return this.allStudents
        .filter(student => {
          const matchesDepartment = this.selectedDepartment 
            ? this.courseOptions.find(c => c.name === student.course)?.department === this.selectedDepartment 
            : true;
          const matchesCourse = this.selectedCourse 
            ? student.course === this.selectedCourse 
            : true;
          const matchesYear = this.selectedYear 
            ? student.yearLevel === parseInt(this.selectedYear) 
            : true;
          const matchesSearch = student.lastName.toLowerCase().includes(query) || 
                             student.firstName.toLowerCase().includes(query);
          
          return matchesDepartment && matchesCourse && matchesYear && matchesSearch;
        })
        .sort((a, b) => {
          const lastA = a.lastName.toLowerCase();
          const lastB = b.lastName.toLowerCase();
          if (lastA < lastB) return -1;
          if (lastA > lastB) return 1;
          const firstA = a.firstName.toLowerCase();
          const firstB = b.firstName.toLowerCase();
          if (firstA < firstB) return -1;
          if (firstA > firstB) return 1;
          return 0;
        });
    }
  },
  methods: {
    onDepartmentChange() {
      this.selectedCourse = '';
      this.selectedYear = '';
      this.filterStudents();
    },
    onCourseChange() {
      this.selectedYear = '';
      this.filterStudents();
    },
    filterStudents() {
      // The filtering is now handled by the computed property
    },
    selectStudent(student) {
      this.selectedStudent = student;
    },
    clearSelection() {
      this.selectedStudent = null;
      this.searchQuery = '';
      this.selectedYear = '';
      this.selectedDepartment = '';
      this.selectedCourse = '';
      this.filteredStudents = [...this.allStudents];
    },
    getYearLabel(year) {
      const labels = {
        1: '1st Year',
        2: '2nd Year',
        3: '3rd Year',
        4: '4th Year'
      };
      return labels[year] || year;
    },
    getStatusLabel(status) {
      if (!status) return 'Not Set';
      const statusMap = {
        'pending': 'Pending',
        'in_review': 'In Review',
        'approved': 'Approved',
        'rejected': 'Rejected',
        'on_hold': 'On Hold'
      };
      return statusMap[status] || status;
    },
    getStatusClass(status) {
      if (!status) return 'status-not-set';
      return `status-${status.replace('_', '-')}`;
    },
    viewStudentClearance(student) {
      // Navigate to student clearance details
      console.log('Viewing clearance for:', student.id);
      this.selectedStudent = student;
    },
    editStudentStatus(student) {
      this.statusDialog = {
        visible: true,
        student: { ...student },
        status: student.status || 'pending',
        notes: student.notes || ''
      };
    },
    async saveStatus() {
      try {
        // Here you would typically make an API call to save the status
        // For example:
        // await updateStudentStatus(this.statusDialog.student.id, {
        //   status: this.statusDialog.status,
        //   notes: this.statusDialog.notes
        // });
        
        // Show success message
        this.$toast.add({
          severity: 'success',
          summary: 'Success',
          detail: 'Status updated successfully',
          life: 3000
        });
        
        // Update the student in the local list
        const studentIndex = this.allStudents.findIndex(s => s.id === this.statusDialog.student.id);
        if (studentIndex > -1) {
          this.allStudents[studentIndex] = {
            ...this.allStudents[studentIndex],
            status: this.statusDialog.status,
            notes: this.statusDialog.notes
          };
        }
        
        // Close the dialog
        this.statusDialog.visible = false;
      } catch (error) {
        console.error('Error updating status:', error);
        this.$toast.add({
          severity: 'error',
          summary: 'Error',
          detail: 'Failed to update status. Please try again.',
          life: 5000
        });
      }
    },
  }
}
</script>

<style scoped>
.clearance-container {
  width: 100%;
  margin: 0 auto;
}

.student-selection {
  background: var(--surface-card);
  border-radius: 12px;
  padding: 2rem;
  width: 100%;
  margin: 0 auto;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.filter-row {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  align-items: flex-end;
  flex-wrap: wrap;
}

.filter-item {
  flex: 1;
  min-width: 200px;
}

.filter-search {
  flex: 2;
  min-width: 250px;
}

.student-list {
  margin-top: 1.5rem;
  border: 1px solid var(--surface-border);
  border-radius: 6px;
  overflow: hidden;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.student-list-header {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 2fr 1fr 120px 120px;
  background-color: var(--surface-50);
  font-weight: 600;
  padding: 1rem;
  border-bottom: 1px solid var(--surface-border);
  color: var(--text-color-secondary);
}

.header-item {
  padding: 0.75rem 1rem;
  text-align: left;
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.student-item {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 2fr 1fr 120px 120px;
  padding: 1rem;
  border-bottom: 1px solid var(--surface-border);
  cursor: pointer;
  transition: background-color 0.2s;
  background-color: var(--surface-card);
}

.student-item > div {
  padding: 0.5rem;
  display: flex;
  align-items: center;
  color: var(--text-color);
}

.student-item:hover {
  background-color: var(--surface-hover);
}

.student-item:last-child {
  border-bottom: none;
}

.student-actions {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
  align-items: center;
}

.student-actions .p-button {
  margin: 0;
  padding: 0.5rem;
}

.student-actions .p-button.p-button-sm {
  width: 2rem;
  height: 2rem;
}

/* Status Badge Styles */
.status-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  text-align: center;
  text-transform: capitalize;
  min-width: 80px;
}

.status-pending {
  background-color: #fff3cd;
  color: #856404;
  border: 1px solid #ffeeba;
}

.status-in-review {
  background-color: #e2e3e5;
  color: #383d41;
  border: 1px solid #d6d8db;
}

.status-approved {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.status-rejected {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.status-on-hold {
  background-color: #d1ecf1;
  color: #0c5460;
  border: 1px solid #bee5eb;
}

.status-not-set {
  background-color: #f8f9fa;
  color: #6c757d;
  border: 1px solid #f1f1f1;
  font-style: italic;
}

/* Update responsive styles */
@media (max-width: 992px) {
  .student-list-header,
  .student-item {
    grid-template-columns: 1fr 1fr 1fr 1fr;
  }
  
  .header-item:nth-child(n+6),
  .student-item > div:nth-child(n+6) {
    display: none;
  }
  
  .student-actions {
    grid-column: 4;
  }
}

@media (max-width: 576px) {
  .student-list-header,
  .student-item {
    grid-template-columns: 1fr 1fr;
  }
  
  .header-item:nth-child(n+3),
  .student-item > div:nth-child(n+3) {
    display: none;
  }
  
  .student-actions {
    grid-column: 2;
  }
}

/* Add dialog specific styles */
:deep(.p-dialog .p-dialog-header) {
  background: var(--surface-card);
  border-bottom: 1px solid var(--surface-border);
}

:deep(.p-dialog .p-dialog-content) {
  background: var(--surface-card);
  padding: 1.5rem;
}

:deep(.p-dialog .p-dialog-footer) {
  background: var(--surface-card);
  border-top: 1px solid var(--surface-border);
  padding: 1rem 1.5rem;
  text-align: right;
}

:deep(.p-dialog .p-dialog-header-icons) {
  margin-right: 0.5rem;
}

:deep(.p-dialog .p-dialog-header .p-dialog-header-icon) {
  color: var(--text-color-secondary);
}

:deep(.p-dialog .p-dialog-header .p-dialog-header-icon:hover) {
  color: var(--primary-color);
  background: var(--surface-hover);
}

/* Make sure the dialog is properly centered */
:deep(.p-dialog) {
  border-radius: 12px;
  box-shadow: 0 11px 15px -7px rgba(0, 0, 0, 0.2), 
              0 24px 38px 3px rgba(0, 0, 0, 0.14), 
              0 9px 46px 8px rgba(0, 0, 0, 0.12);
}

/* Responsive adjustments for dialog */
@media (max-width: 640px) {
  :deep(.p-dialog) {
    width: 90% !important;
    max-width: 100%;
  }
}
</style>