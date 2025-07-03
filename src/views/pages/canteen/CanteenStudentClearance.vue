<template>
  <div class="clearance-container">
    <!-- Student Selection Interface -->
    <div v-if="!selectedStudent" class="student-selection">
      <!-- Stats Cards -->
      <div class="stats-container">
        <div class="stat-card total" @click="filterByStatus('')" style="cursor: pointer">
          <div class="stat-icon"><i class="pi pi-users"></i></div>
          <div class="stat-content">
            <div class="stat-value">{{ totalAllStudents }}</div>
            <div class="stat-label">Total Students</div>
          </div>
        </div>
        <div class="stat-card cleared" @click="filterByStatus('Cleared')" style="cursor: pointer">
          <div class="stat-icon"><i class="pi pi-check-circle"></i></div>
          <div class="stat-content">
            <div class="stat-value">{{ totalClearedCount }}</div>
            <div class="stat-label">Cleared</div>
          </div>
        </div>
        <div class="stat-card pending" @click="filterByStatus('Pending')" style="cursor: pointer">
          <div class="stat-icon"><i class="pi pi-clock"></i></div>
          <div class="stat-content">
            <div class="stat-value">{{ totalPendingCount }}</div>
            <div class="stat-label">Pending</div>
          </div>
        </div>
      </div>

      <div class="header-section">
      </div>

      <div class="filter-section card">
        <div class="filter-content">
          <!-- Academic Year -->
          <div class="filter-group">
            <label>Academic Year</label>
            <Dropdown v-model="selectedAcademicYear" :options="academicYearOptions" @change="filterStudents"
              placeholder="Academic Year" class="w-full" />
          </div>

          <!-- Department Dropdown -->
          <div class="filter-group">
            <label>Department</label>
            <Dropdown v-model="selectedDepartment" :options="['', ...new Set(departmentOptions)]"
              @change="onDepartmentChange" placeholder="Department" class="w-full" />
          </div>

          <!-- Course Dropdown -->
          <div class="filter-group">
            <label>Course</label>
            <Dropdown v-model="selectedCourse" :options="filteredCourseOptions" optionLabel="" placeholder="Course"
              class="w-full" @change="onCourseChange" />
          </div>

          <!-- Year Level Dropdown -->
          <div class="filter-group">
            <label>Year Level</label>
            <Dropdown v-model="selectedYear" :options="['', 1, 2, 3, 4]" optionLabel="value" optionValue="value"
              @change="filterStudents" placeholder="Year Level" class="w-full">
              <template #value="slotProps">
                <div v-if="slotProps.value">{{ formatYearLevel(slotProps.value) }}</div>
                <span v-else>{{ slotProps.placeholder }}</span>
              </template>
              <template #option="slotProps">
                <div>{{ formatYearLevel(slotProps.option) }}</div>
              </template>
            </Dropdown>
          </div>

          <!-- Semester Dropdown -->
          <div class="filter-group">
            <label>Semester</label>
            <Dropdown v-model="selectedSemester" :options="semesterOptions" @change="filterStudents"
              placeholder="Semester" class="w-full" />
          </div>

          <!-- Status Dropdown -->
          <div class="filter-group">
            <label>Status</label>
            <Dropdown v-model="selectedStatus" :options="statusOptions" @change="filterStudents" placeholder="Status"
              class="w-full" />
          </div>

          <!-- Search -->
          <div class="filter-search">
            <InputText v-model="searchQuery" @input="filterStudents" placeholder="Search" class="w-full" />
          </div>


          <!-- Clear Filters Button -->
          <div class="filter-group">
            <Button label="Clear Filters" icon="pi pi-filter-slash" class="p-button-text p-button-sm"
              @click="clearFilters" />
          </div>

        </div>
      </div>

      <!-- studdent list -->
      <div class="card table-card">
        <DataTable :value="filteredStudents" :paginator="true" :rows="10" :rowsPerPageOptions="[10, 25, 50]"
          paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
          currentPageReportTemplate="Showing {first} to {last} of {totalRecords} students" responsiveLayout="scroll"
          class="p-datatable-sm">
          <Column field="id" header="Student ID" :sortable="true"></Column>
          <Column field="name" header="Student Name" :sortable="true">
            <template #body="{ data }">
              {{ data.lastName }}, {{ data.firstName }}
            </template>
          </Column>
          <Column field="course" header="Course" :sortable="true"></Column>
          <Column field="yearLevel" header="Year Level" :sortable="true">
            <template #body="{ data }">
              {{ formatYearLevel(data.yearLevel) }}
            </template>
          </Column>
          <Column field="semester" header="Semester" :sortable="true">
            <template #body="{ data }">
              {{ data.semester }}
            </template>
          </Column>
          <Column field="clearanceStatus" header="Status" :sortable="true">
            <template #body="{ data }">
              <Tag :value="data.clearanceStatus" :severity="getStatusSeverity(data.clearanceStatus)"
                :class="{ 'status-pending': data.clearanceStatus === 'Pending', 'status-cleared': data.clearanceStatus === 'Cleared' }" />
            </template>
          </Column>
          <Column field="dateCleared" header="Date Cleared" :sortable="true" style="width: 120px">
            <template #body="{ data }">
              <span v-if="data.clearanceStatus === 'Cleared'" class="date-cell">
                {{ data.updatedAt ? formatDate(data.updatedAt) : formatDate(new Date().toISOString()) }}
              </span>
              <span v-else class="text-500">
                Not cleared yet
              </span>
            </template>
          </Column>
          <Column field="remarks" header="Remarks" :sortable="true" style="min-width: 100px; max-width: 200px" class="remarks-column">
            <template #body="{ data }">
              <span class="remarks-cell" :title="data.remarks || (data.clearanceStatus === 'Cleared' ? 'All Cleared' : 'No remarks')">
                {{ data.remarks 
                    ? (data.remarks.length > 25 ? data.remarks.substring(0, 25) + '...' : data.remarks) 
                    : (data.clearanceStatus === 'Cleared' ? 'All Cleared' : 'No remarks') }}
              </span>
            </template>
          </Column>
          <Column header="Actions">
            <template #body="{ data }">
              <Button icon="pi pi-eye" class="p-button-rounded p-button-text p-button-sm"
                @click="viewStudentDetails(data)" v-tooltip.top="'View Details'" />
              
            </template>
          </Column>
        </DataTable>
      </div>
    </div>

    <!-- Canteen Clearance Form Dialog -->
    <Dialog v-model:visible="showClearanceDialog" :modal="true" :style="{ width: '50vw' }" @hide="onDialogHide">
      <template #header>
        <div class="dialog-header">
        </div>
      </template>
      <CanteenClearanceForm 
        v-if="selectedStudent" 
        :key="selectedStudent.id" 
        :student="selectedStudent"
        @clearance-updated="handleClearanceUpdate"
        @close-dialog="closeDialog"
      />
    </Dialog>
  </div>
</template>

<script>
import { ref, computed } from 'vue';
import Dropdown from 'primevue/dropdown';
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';
import Dialog from 'primevue/dialog';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Tag from 'primevue/tag';
import Tooltip from 'primevue/tooltip';
import CanteenClearanceForm from './CanteenClearanceForm.vue';

export default {
  name: 'CanteenStudentClearance',
  components: {
    CanteenClearanceForm,
    Dropdown,
    InputText,
    Button,
    Dialog,
    DataTable,
    Column,
    Tag
  },
  directives: {
    'tooltip': Tooltip
  },
  data() {
    return {
      showClearanceDialog: false,
      searchQuery: '',
      selectedAcademicYear: '',
      academicYearOptions: ['', '2023-2024', '2024-2025', '2025-2026'],
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
        { department: 'College of Engineering', name: 'Bachelor of Science in Civil Engineering' },
        { department: 'College of Engineering', name: 'Bachelor of Science in Electrical Engineering' },
        { department: 'College of Business Administration', name: 'Bachelor of Science in Business Administration' },
        { department: 'College of Education', name: 'Bachelor of Elementary Education' },
        { department: 'College of Education', name: 'Bachelor of Secondary Education' },
        { department: 'College of Arts and Sciences', name: 'Bachelor of Arts in Communication' },
        { department: 'College of Arts and Sciences', name: 'Bachelor of Science in Psychology' }
      ],
      selectedYear: '',
      selectedSemester: '',
      semesterOptions: ['', '1st Semester', '2nd Semester', 'Summer'],
      selectedStatus: '',
      statusOptions: ['', 'Cleared', 'Pending'],
      selectedStudent: null,
      showClearanceDialog: false,
      allStudents: [
        {
          id: '2023-10001', firstName: 'Jose', lastName: 'Rizal', course: 'Bachelor of Science in Computer Science',
          yearLevel: 1, clearanceStatus: 'Pending', updatedAt: null, academicYear: '2023-2024', semester: '1st Semester', remarks: ''
        },
        {
          id: '2023-10002', firstName: 'Andres', lastName: 'Bonifacio',
          course: 'Bachelor of Science in Information Technology', yearLevel: 1,
          clearanceStatus: 'Cleared', updatedAt: '2025-05-20T14:30:00.000Z', academicYear: '2023-2024', semester: '1st Semester', remarks: 'Paid in full'
        },
        {
          id: '2023-10003', firstName: 'Juan', lastName: 'Dela Cruz',
          course: 'Bachelor of Science in Civil Engineering', yearLevel: 2,
          clearanceStatus: 'Pending', updatedAt: null, academicYear: '2023-2024', semester: '1st Semester', remarks: ''
        },
        {
          id: '2023-10004', firstName: 'Maria', lastName: 'Clara',
          course: 'Bachelor of Science in Business Administration', yearLevel: 3,
          clearanceStatus: 'Cleared', updatedAt: '2025-05-21T10:15:00.000Z', academicYear: '2023-2024', semester: '1st Semester', remarks: ''
        },
        {
          id: '2023-10005', firstName: 'Pedro', lastName: 'Penduko',
          course: 'Bachelor of Elementary Education', yearLevel: 4,
          clearanceStatus: 'Pending', updatedAt: null, academicYear: '2023-2024', semester: '1st Semester', remarks: ''
        },
        {
          id: '2023-10006', firstName: 'Neneng', lastName: 'Santos',
          course: 'Bachelor of Secondary Education', yearLevel: 2,
          clearanceStatus: 'Cleared', updatedAt: '2025-05-22T09:30:00.000Z', academicYear: '2023-2024', semester: '1st Semester', remarks: ''
        },
        {
          id: '2023-10007', firstName: 'Juan', lastName: 'Tamad',
          course: 'Bachelor of Arts in Communication', yearLevel: 1,
          clearanceStatus: 'Pending', updatedAt: null, academicYear: '2024-2025', semester: '1st Semester', remarks: ''
        },
        {
          id: '2023-10008', firstName: 'Darna', lastName: 'Reyes',
          course: 'Bachelor of Science in Psychology', yearLevel: 3,
          clearanceStatus: 'Cleared', updatedAt: '2025-05-19T16:45:00.000Z', academicYear: '2024-2025', semester: '1st Semester', remarks: ''
        },
        {
          id: '2023-10009', firstName: 'Cardo', lastName: 'Dalisay',
          course: 'Bachelor of Science in Computer Science', yearLevel: 2,
          clearanceStatus: 'Pending', updatedAt: null, academicYear: '2024-2025', semester: '2nd Semester', remarks: ''
        },
        {
          id: '2023-10010', firstName: 'Mara', lastName: 'Clara',
          course: 'Bachelor of Science in Information Technology', yearLevel: 4,
          clearanceStatus: 'Cleared', updatedAt: '2025-05-18T11:20:00.000Z', academicYear: '2024-2025', semester: '2nd Semester', remarks: ''
        },
        {
          id: '2023-10011', firstName: 'Jose', lastName: 'Garcia',
          course: 'Bachelor of Science in Electrical Engineering', yearLevel: 1,
          clearanceStatus: 'Pending', updatedAt: null, academicYear: '2024-2025', semester: '2nd Semester', remarks: ''
        },
        {
          id: '2023-10012', firstName: 'Maria', lastName: 'Santos',
          course: 'Bachelor of Science in Business Administration', yearLevel: 2,
          clearanceStatus: 'Cleared', updatedAt: '2025-05-17T14:10:00.000Z', academicYear: '2024-2025', semester: '2nd Semester', remarks: ''
        },
        {
          id: '2023-10013', firstName: 'Antonio', lastName: 'Luna',
          course: 'Bachelor of Elementary Education', yearLevel: 3,
          clearanceStatus: 'Pending', updatedAt: null, academicYear: '2024-2025', semester: '2nd Semester', remarks: ''
        },
        {
          id: '2023-10014', firstName: 'Gabriela', lastName: 'Silang',
          course: 'Bachelor of Secondary Education', yearLevel: 4,
          clearanceStatus: 'Cleared', updatedAt: '2025-05-16T10:30:00.000Z', academicYear: '2024-2025', semester: '2nd Semester', remarks: ''
        },
        {
          id: '2023-10015', firstName: 'Emilio', lastName: 'Aguinaldo',
          course: 'Bachelor of Arts in Communication', yearLevel: 1,
          clearanceStatus: 'Pending', updatedAt: null, academicYear: '2025-2026', semester: '1st Semester', remarks: ''
        },
        {
          id: '2023-10016', firstName: 'Gregorio', lastName: 'Del Pilar',
          course: 'Bachelor of Science in Computer Science', yearLevel: 2,
          clearanceStatus: 'Pending', updatedAt: null, academicYear: '2024-2025', semester: 'Summer', remarks: ''
        }
      ],
      filteredStudents: []
    }
  },
  computed: {
    totalStudents() {
      return this.filteredStudents.length;
    },

    totalAllStudents() {
      return this.allStudents.length;
    },

    clearedCount() {
      return this.filteredStudents.filter(s => s.clearanceStatus === 'Cleared').length;
    },

    totalClearedCount() {
      return this.allStudents.filter(s => s.clearanceStatus === 'Cleared').length;
    },

    pendingCount() {
      return this.filteredStudents.filter(s => s.clearanceStatus === 'Pending').length;
    },

    totalPendingCount() {
      return this.allStudents.filter(s => s.clearanceStatus === 'Pending').length;
    },

    filteredCourseOptions() {
      if (!this.selectedDepartment) {
        return [];
      }
      return this.courseOptions
        .filter(course => course.department === this.selectedDepartment)
        .map(course => course.name);
    },

    filteredStudents() {
      const query = this.searchQuery ? this.searchQuery.toLowerCase() : '';

      return this.allStudents
        .filter(student => {
          const matchesAcademicYear = this.selectedAcademicYear
            ? student.academicYear === this.selectedAcademicYear
            : true;

          const matchesDepartment = this.selectedDepartment
            ? student.department === this.selectedDepartment
            : true;

          const matchesCourse = this.selectedCourse
            ? student.course === this.selectedCourse
            : true;

          const matchesYear = this.selectedYear
            ? student.yearLevel === parseInt(this.selectedYear)
            : true;

          const matchesSemester = this.selectedSemester
            ? student.semester === this.selectedSemester
            : true;

          const matchesStatus = this.selectedStatus
            ? student.clearanceStatus === this.selectedStatus
            : true;

          const matchesSearch = student.lastName.toLowerCase().includes(query) ||
            student.firstName.toLowerCase().includes(query) ||
            student.id.toLowerCase().includes(query);

          return matchesAcademicYear && matchesDepartment && matchesCourse &&
            matchesYear && matchesSemester && matchesStatus && matchesSearch;
        })
        .sort((a, b) => {
          const lastA = a.lastName.toLowerCase();
          const lastB = b.lastName.toLowerCase();
          if (lastA < lastB) return -1;
          if (lastA > lastB) return 1;
          return 0;
        });
    }
  },

  methods: {
    onDialogHide() {
      this.showClearanceDialog = false;
      this.selectedStudent = null;
    },
    closeDialog() {
      this.showClearanceDialog = false;
      this.selectedStudent = null;
    },
    formatDate(dateString) {
      if (!dateString) return 'N/A';
      const options = { year: 'numeric', month: 'short', day: 'numeric' };
      return new Date(dateString).toLocaleDateString(undefined, options);
    },

    formatYearLevel(level) {
      const levels = ['1st Year', '2nd Year', '3rd Year', '4th Year'];
      return levels[level - 1] || level;
    },

    getStatusSeverity(status) {
      switch (status) {
        case 'Cleared': return 'success';
        case 'Pending': return 'warning';
        default: return null;
      }
    },

    viewStudentDetails(student) {
      console.log('Viewing student:', student.id); // Debug log
      this.selectedStudent = student;
      this.showClearanceDialog = true;
    },

    handleClearanceUpdate(updatedData) {
      const studentIndex = this.allStudents.findIndex(s => s.id === updatedData.studentId);
      if (studentIndex !== -1) {
        const student = this.allStudents[studentIndex];
        student.clearanceStatus = updatedData.cleared ? 'Cleared' : 'Pending';
        student.updatedAt = new Date().toISOString();
        student.remarks = updatedData.remarks || '';
        
        // Close the dialog after a short delay to show the success message
        setTimeout(() => {
          this.showClearanceDialog = false;
          this.selectedStudent = null;
        }, 500);
      }
    },

    filterByStatus(status) {
      this.selectedStatus = status;
    },

    clearFilters() {
      this.selectedAcademicYear = '';
      this.selectedDepartment = '';
      this.selectedCourse = '';
      this.selectedYear = '';
      this.selectedSemester = '';
      this.selectedStatus = '';
      this.searchQuery = '';
    }
  },

  mounted() {
    this.filteredStudents = [...this.allStudents];
  },
}
</script>

<style scoped>
.clearance-container {
  background-color: #fff;
  padding: 1rem;
  border-radius: 12px;
}

.student-selection {
  background: #fff;
  border-radius: 8px;
  width: 100%;
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

/* Filter section */
.filter-section {
  display: flex;
  margin: 1.5rem;
  padding: 1.25rem;
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.filter-content {
  display: flex;
  flex-wrap: wrap;
  gap: 1.25rem;
  align-items: flex-end;
}

.filter-group {
  display: flex;
  flex-direction: column;
  min-width: 160px;
  flex: 1;
}

.filter-group label {
  font-size: 0.875rem;
  font-weight: 500;
  margin-bottom: 0.5rem;
  color: var(--text-color-secondary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.filter-search {
  flex: 3.5;
  min-width: 200px;
}

.card {
  display: flex;
  flex-direction: column;
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  margin: 1.5rem;
  overflow: hidden;
  height: calc(100% - 3rem);
  width: calc(100% - 3rem);
}

.table-card {
  display: flex;
  flex-direction: column;
  flex: 1;
  overflow: hidden;
}

:deep(.p-datatable) {
  display: flex;
  flex-direction: column;
  flex: 1;
  height: 100%;
}

:deep(.p-datatable-wrapper) {
  flex: 1;
  overflow: auto;
}

:deep(.p-datatable-table) {
  width: 100%;
}

/* Status badges */
:deep(.p-tag) {
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  border: 1px solid;
}

:deep(.p-tag.status-pending) {
  background-color: #fff3cd;
  color: #856404;
  border-color: #fcefc2;
}

:deep(.p-tag.status-cleared) {
  background-color: #d4edda;
  color: #155724;
  border-color: #c3e6cb;
}

/* Dialog styles */
:deep(.p-dialog .p-dialog-header) {
  padding: 1.25rem 1.5rem;
  background: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
  border-top-left-radius: 6px;
  border-top-right-radius: 6px;
}

:deep(.p-dialog .p-dialog-content) {
  padding: 0;
  background: #fff;
}


:deep(.p-dialog .p-dialog-header .p-dialog-title) {
  font-size: 1.25rem;
  font-weight: 600;
  color: #343a40;
}

/* Responsive adjustments */
@media (max-width: 1200px) {
  .filter-group {
    min-width: 140px;
  }
}

@media (max-width: 992px) {
  .filter-group {
    flex: 1 0 calc(50% - 0.625rem);
  }

  .filter-search {
    flex: 1 0 100%;
    margin-top: 0.5rem;
  }
}

@media (max-width: 576px) {
  .filter-group {
    flex: 1 0 100%;
  }

  .filter-section {
    padding: 1rem;
    margin: 1rem 0;
  }
}

.stats-container {
  display: flex;
  gap: 1rem;
  margin: 1rem;
}

.stat-card {
  flex: auto;
  border-radius: 10px;
  padding: 1.25rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  display: flex;
  align-items: center;
  transition: transform 0.2s, box-shadow 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

.stat-icon {
  font-size: 1.75rem;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 1rem;
  color: white;
}

.stat-icon i {
  font-size: 1.25rem;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 600;
  line-height: 1.2;
}

.stat-label {
  font-size: 0.875rem;
  color: var(--text-secondary-color);
  margin-top: 0.25rem;
}

/* Card specific colors */
.stat-card.total {
  border-left: 4px solid #2563eb;
}

.stat-card.total .stat-icon {
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
}

.stat-card.cleared {
  border-left: 4px solid #10B981;
}

.stat-card.cleared .stat-icon {
  background: linear-gradient(135deg, #10B981 0%, #059669 100%);
}

.stat-card.pending {
  border-left: 4px solid #F59E0B;
}

.stat-card.pending .stat-icon {
  background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .stats-container {
    flex-direction: column;
  }

  .stat-card {
    width: 100%;
  }
}

.remarks-text {
  max-width: 200px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: block;
}

.remarks-text:hover {
  white-space: normal;
  overflow: visible;
  text-overflow: unset;
  position: absolute;
  background: var(--surface-card);
  padding: 0.5rem;
  border: 1px solid var(--surface-border);
  border-radius: 4px;
  z-index: 1000;
  max-width: 300px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  padding-right: 1rem;
}

.dialog-header span {
  font-weight: 600;
  font-size: 1.25rem;
}
</style>