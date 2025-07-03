<template>
  <div class="dsa-container">
    <!-- Stats Cards -->
    <div class="stats-container">
      <div class="stat-card total" @click="filterByStatus('')" style="cursor: pointer">
        <div class="stat-icon"><i class="pi pi-users"></i></div>
        <div class="stat-content">
          <div class="stat-value">{{ totalStudents }}</div>
          <div class="stat-label">Total Students</div>

        </div>
      </div>
      <div class="stat-card cleared" @click="filterByStatus('Cleared')" style="cursor: pointer">
        <div class="stat-icon"><i class="pi pi-check-circle"></i></div>
        <div class="stat-content">
          <div class="stat-value">{{ clearedCount }}</div>
          <div class="stat-label">Cleared</div>
        </div>
      </div>
      <div class="stat-card pending" @click="filterByStatus('Pending')" style="cursor: pointer">
        <div class="stat-icon"><i class="pi pi-clock"></i></div>
        <div class="stat-content">
          <div class="stat-value">{{ pendingCount }}</div>
          <div class="stat-label">Pending</div>
        </div>
      </div>
      <div class="stat-card enrolled" @click="filterByStatus('Enrolled')" style="cursor: pointer">
        <div class="stat-icon"><i class="pi pi-bookmark"></i></div>
        <div class="stat-content">
          <div class="stat-value">{{ enrolledCount }}</div>
          <div class="stat-label">Enrolled</div>
        </div>
      </div>

            <!-- 10/10 Totl Students with percentage -->
      <!-- <div class="stat-card pending" @click="filterByStatus('Pending')" style="cursor: pointer">
        <div class="stat-icon"><i class="pi pi-clock"></i></div>
        <div class="stat-content">
          <div class="stat-value">{{ pendingCount }} <span class="stat-total">/ {{ totalPendingCount }}</span></div>
          <div class="stat-label">Pending</div>
          <div class="stat-percentage">
            {{ totalStudents > 0 ? Math.round((pendingCount / totalStudents) * 100) : 0 }}% of filtered
            <span v-if="totalStudents !== totalAllStudents">
              ({{ Math.round((totalPendingCount / totalAllStudents) * 100) }}% of all)
            </span>
          </div>
        </div>
      </div> -->

    </div>

    <!-- Filter Section -->
    <div class="filter-section card">
      <div class="filter-content">
        <div class="filter-group">
          <label>Academic Year</label>
          <Dropdown 
            v-model="selectedAcademicYear" 
            :options="academicYears" 
            placeholder="Academic Year"
            class="p-column-filter"
          />
        </div>
        
        <div class="filter-group">
          <label>Department</label>
          <Dropdown 
            v-model="selectedDepartment" 
            :options="departmentOptions"
            placeholder="Department"
            class="p-column-filter"
            @change="onDepartmentChange"
          />
        </div>
        
        <div class="filter-group">
          <label>Course</label>
          <Dropdown 
            v-model="selectedCourse" 
            :options="filteredCourseOptions"
            placeholder="Course"
            class="p-column-filter"
            @change="onCourseChange"
          />
        </div>
        
        <div class="filter-group">
          <label>Year Level</label>
          <Dropdown 
            v-model="selectedYearLevel" 
            :options="yearLevelOptions"
            optionLabel="name" 
            optionValue="value"
            placeholder="Year Level"
            class="p-column-filter"
          />
        </div>
        
        <div class="filter-group">
          <label>Semester</label>
          <Dropdown 
            v-model="selectedSemester" 
            :options="semesterOptions"
            optionLabel="name" 
            optionValue="value"
            placeholder="Semester"
            class="p-column-filter"
          />
        </div>
        
        <div class="filter-group">
          <label>Status</label>
          <Dropdown 
            v-model="selectedStatus" 
            :options="statusOptions" 
            optionLabel="name" 
            optionValue="value"
            placeholder="Status"
            class="p-column-filter"
          />
        </div>
        
        <div class="filter-search">
            <InputText 
              v-model="searchQuery"
              @input="filterStudents"
              placeholder="Search"
              class="w-full"
            />
        </div>
        <div class="filter-group">
          <Button 
            label="Clear Filters" 
            icon="pi pi-filter-slash" 
            class="p-button-text" 
            @click="clearFilters"
          />
        </div>

      </div>
    </div>

    <!-- Student Clearance Table -->
    <div class="card table-card">
      <DataTable 
        :value="filteredStudents" 
        :paginator="true" 
        :rows="10"
        :rowsPerPageOptions="[10,25,50]"
        paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
        currentPageReportTemplate="Showing {first} to {last} of {totalRecords} students"
        responsiveLayout="scroll"
        :loading="loading"
        class="p-datatable-sm compact-table"
        scrollable
        scrollHeight="flex"
      >
        <Column field="id" header="ID" :sortable="true" style="width: 100px"></Column>
        <Column field="name" header="Student Name" :sortable="true" style="min-width: 150px">
          <template #body="{data}">
            {{ data.lastName }}, {{ data.firstName }}
          </template>
        </Column>
        <Column field="course" header="Course" :sortable="true" style="min-width: 120px"></Column>
        <Column field="yearLevel" header="Yr. Lvl" :sortable="true" style="width: 80px">
          <template #body="{data}">
            {{ formatYearLevel(data.yearLevel) }}
          </template>
        </Column>
        <Column field="clearanceStatus" header="Status" :sortable="true" style="width: 100px">
          <template #body="{data}">
            <Tag :value="data.clearanceStatus" 
                 :severity="getStatusSeverity(data.clearanceStatus)" 
                 :class="`status-${data.clearanceStatus.toLowerCase()}`" />
          </template>
        </Column>
        <Column field="dateCleared" header="Date Cleared" :sortable="true" style="width: 120px">
          <template #body="{data}">
            <span v-if="data.clearanceStatus === 'Cleared'" class="date-cell">
              {{ data.dateCleared ? formatDate(data.dateCleared) : formatDate(new Date().toISOString()) }}
            </span>
            <span v-else class="text-500">
              Not cleared yet
            </span>
          </template>
        </Column>
        <Column field="remarks" header="Remarks" :sortable="true" style="min-width: 100px; max-width: 200px" class="remarks-column">
          <template #body="{data}">
            <span class="remarks-cell" :title="data.remarks || (data.clearanceStatus === 'Cleared' ? 'All Cleared' : 'No remarks')">
              {{ data.remarks 
                  ? (data.remarks.length > 25 ? data.remarks.substring(0, 25) + '...' : data.remarks) 
                  : (data.clearanceStatus === 'Cleared' ? 'All Cleared' : 'No Remarks') }}
            </span>
          </template>
        </Column>
        <Column field="enrollmentStatus" header="Enrollment" :sortable="true" style="width: 100px">
          <template #body="{data}">
            <Tag :value="data.enrollmentStatus" 
                 :severity="getEnrollmentSeverity(data.enrollmentStatus)" 
                 :class="`status-${data.enrollmentStatus.toLowerCase()}`" />
          </template>
        </Column>
        <Column header="Actions" style="width: 100px" :exportable="false">
          <template #body="{data}">
            <Button 
              icon="pi pi-eye" 
              class="p-button-rounded p-button-text p-button-sm"
              @click="viewStudentDetails(data)"
              v-tooltip.top="'View Details'"
            />
            <Button 
              v-if="data.clearanceStatus === 'Cleared' && data.enrollmentStatus !== 'Enrolled'"
              icon="pi pi-check" 
              class="p-button-rounded p-button-text p-button-success p-button-sm"
              @click="markAsEnrolled(data)"
              v-tooltip.top="'Mark as Enrolled'"
            />
          </template>
        </Column>
      </DataTable>
    </div>

    <!-- Student Details Dialog -->
    <Dialog 
      v-model:visible="displayDialog" 
      :modal="true"
      :style="{width: '800px'}"
      :dismissableMask="true"
    >
      <template #header>
        <div class="dialog-header">
        </div>
      </template>
      <ClearanceForm 
        v-if="selectedStudent" 
        :student="{
          id: selectedStudent.id,
          firstName: selectedStudent.firstName,
          lastName: selectedStudent.lastName,
          department: selectedStudent.department,
          course: selectedStudent.course,
          yearLevel: selectedStudent.yearLevel
        }"
        @status-updated="handleStatusUpdated"
        @clearance-updated="handleStatusUpdated"
        @clearance-submitted="handleClearanceSubmitted"
        @close-dialog="closeDialog"
      />
    </Dialog>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useToast } from 'primevue/usetoast';
import Dropdown from 'primevue/dropdown';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Tag from 'primevue/tag';
import Button from 'primevue/button';
import Dialog from 'primevue/dialog';
import Divider from 'primevue/divider';
import InputText from 'primevue/inputtext';
import ClearanceForm from './DSAClearanceForm.vue';

export default {
  components: {
    Dropdown,
    DataTable,
    Column,
    Tag,
    Button,
    Dialog,
    Divider,
    InputText,
    ClearanceForm
  },
  setup() {
    const toast = useToast();
    const loading = ref(false);
    const displayDialog = ref(false);
    const searchQuery = ref('');
    const selectedAcademicYear = ref('');
    const selectedDepartment = ref('');
    const selectedCourse = ref('');
    const selectedYearLevel = ref('');
    const selectedSemester = ref('');
    const selectedStatus = ref('');
    const selectedEnrollmentStatus = ref('');
    const selectedStudent = ref(null);
    
    // Sample data - replace with API calls in production
    const students = ref([
      {
        id: '2023-10001',
        firstName: 'Jose',
        lastName: 'Rizal',
        email: 'jose.rizal@student.edu.ph',
        department: 'College of Computer Studies',
        course: 'Bachelor of Science in Computer Science',
        yearLevel: 1,
        academicYear: '2023-2024',
        semester: '1st Semester',
        clearanceStatus: 'Pending',
        enrollmentStatus: 'Pending',
        dateCleared: null,
        departmentClearances: []
      },
      {
        id: '2023-10002',
        firstName: 'Andres',
        lastName: 'Bonifacio',
        email: 'andres.bonifacio@student.edu.ph',
        department: 'College of Computer Studies',
        course: 'Bachelor of Science in Information Technology',
        yearLevel: 1,
        academicYear: '2023-2024',
        semester: '1st Semester',
        clearanceStatus: 'Cleared',
        enrollmentStatus: 'Enrolled',
        dateCleared: '2025-05-20T14:30:00.000Z',
        departmentClearances: []
      },
      {
        id: '2023-10003',
        firstName: 'Juan',
        lastName: 'Dela Cruz',
        email: 'juan.delacruz@student.edu.ph',
        department: 'College of Engineering',
        course: 'Bachelor of Science in Civil Engineering',
        yearLevel: 2,
        academicYear: '2023-2024',
        semester: '1st Semester',
        clearanceStatus: 'Pending',
        enrollmentStatus: 'Pending',
        dateCleared: null,
        departmentClearances: []
      },
      {
        id: '2023-10004',
        firstName: 'Maria',
        lastName: 'Clara',
        email: 'maria.clara@student.edu.ph',
        department: 'College of Business Administration',
        course: 'Bachelor of Science in Business Administration',
        yearLevel: 3,
        academicYear: '2023-2024',
        semester: '1st Semester',
        clearanceStatus: 'Cleared',
        enrollmentStatus: 'Enrolled',
        dateCleared: '2025-05-21T10:15:00.000Z',
        departmentClearances: []
      },
      {
        id: '2023-10005',
        firstName: 'Pedro',
        lastName: 'Penduko',
        email: 'pedro.penduko@student.edu.ph',
        department: 'College of Education',
        course: 'Bachelor of Elementary Education',
        yearLevel: 4,
        academicYear: '2023-2024',
        semester: '1st Semester',
        clearanceStatus: 'Pending',
        enrollmentStatus: 'Pending',
        dateCleared: null,
        departmentClearances: []
      },
      {
        id: '2023-10006',
        firstName: 'Neneng',
        lastName: 'Santos',
        email: 'neneng.santos@student.edu.ph',
        department: 'College of Education',
        course: 'Bachelor of Secondary Education',
        yearLevel: 2,
        academicYear: '2023-2024',
        semester: '1st Semester',
        clearanceStatus: 'Cleared',
        enrollmentStatus: 'Enrolled',
        dateCleared: '2025-05-22T09:30:00.000Z',
        departmentClearances: []
      },
      {
        id: '2023-10007',
        firstName: 'Juan',
        lastName: 'Tamad',
        email: 'juan.tamad@student.edu.ph',
        department: 'College of Arts and Sciences',
        course: 'Bachelor of Arts in Communication',
        yearLevel: 1,
        academicYear: '2024-2025',
        semester: '1st Semester',
        clearanceStatus: 'Pending',
        enrollmentStatus: 'Pending',
        dateCleared: null,
        departmentClearances: []
      },
      {
        id: '2023-10008',
        firstName: 'Darna',
        lastName: 'Reyes',
        email: 'darna.reyes@student.edu.ph',
        department: 'College of Arts and Sciences',
        course: 'Bachelor of Science in Psychology',
        yearLevel: 3,
        academicYear: '2024-2025',
        semester: '1st Semester',
        clearanceStatus: 'Cleared',
        enrollmentStatus: 'Enrolled',
        dateCleared: '2025-05-19T16:45:00.000Z',
        departmentClearances: []
      },
      {
        id: '2023-10009',
        firstName: 'Cardo',
        lastName: 'Dalisay',
        email: 'cardo.dalisay@student.edu.ph',
        department: 'College of Computer Studies',
        course: 'Bachelor of Science in Computer Science',
        yearLevel: 2,
        academicYear: '2024-2025',
        semester: '2nd Semester',
        clearanceStatus: 'Pending',
        enrollmentStatus: 'Pending',
        dateCleared: null,
        departmentClearances: []
      },
      {
        id: '2023-10010',
        firstName: 'Mara',
        lastName: 'Clara',
        email: 'mara.clara@student.edu.ph',
        department: 'College of Computer Studies',
        course: 'Bachelor of Science in Information Technology',
        yearLevel: 4,
        academicYear: '2024-2025',
        semester: '2nd Semester',
        clearanceStatus: 'Cleared',
        enrollmentStatus: 'Enrolled',
        dateCleared: '2025-05-18T11:20:00.000Z',
        departmentClearances: []
      }
    ]);
    
    const academicYears = ref([
      '2023-2024', '2024-2025'
    ]);
    
    const semesterOptions = ref([
      { name: '1st Semester', value: '1' },
      { name: '2nd Semester', value: '2' },
      { name: 'Summer', value: '3' }
    ]);
    
    const statusOptions = ref([
      { name: 'Cleared', value: 'Cleared' },
      { name: 'Pending', value: 'Pending' },
      { name: 'Enrolled', value: 'Enrolled' }
    ]);
    
    const departmentOptions = computed(() => {
      const departments = new Set();
      students.value.forEach(student => {
        if (student.department) departments.add(student.department);
      });
      return Array.from(departments).sort();
    });
    
    const courseOptions = computed(() => {
      const courses = new Set();
      students.value
        .filter(student => !selectedDepartment.value || student.department === selectedDepartment.value)
        .forEach(student => {
          if (student.course) courses.add(student.course);
        });
      return Array.from(courses).sort();
    });
    
    const filteredCourseOptions = computed(() => {
      if (!selectedDepartment.value) {
        return [...new Set(courseOptions.value.map(course => course))];
      }
      return courseOptions.value
        .filter(course => {
          const student = students.value.find(s => s.course === course);
          return student && student.department === selectedDepartment.value;
        })
        .map(course => course);
    });
    
    const yearLevelOptions = ref([
      { name: '1st Year', value: 1 },
      { name: '2nd Year', value: 2 },
      { name: '3rd Year', value: 3 },
      { name: '4th Year', value: 4 },
      { name: '5th Year', value: 5 }
    ]);
    
    // Computed properties
    const filteredStudents = computed(() => {
      const query = searchQuery.value ? searchQuery.value.toLowerCase() : '';
      
      return students.value.filter(student => {
        // Academic Year filter
        const matchesAcademicYear = !selectedAcademicYear.value || 
                                student.academicYear === selectedAcademicYear.value;
        
        // Department filter
        const matchesDepartment = !selectedDepartment.value || 
                               student.department === selectedDepartment.value;
        
        // Course filter
        const matchesCourse = !selectedCourse.value || 
                           student.course === selectedCourse.value;
        
        // Year Level filter
        const matchesYearLevel = !selectedYearLevel.value || 
                              student.yearLevel === parseInt(selectedYearLevel.value);
        
        // Semester filter
        const matchesSemester = !selectedSemester.value || 
                             student.semester === selectedSemester.value;
        
        // Status filter - check both clearanceStatus and enrollmentStatus
        const matchesStatus = !selectedStatus.value || 
                           student.clearanceStatus === selectedStatus.value;
        
        // Enrollment status filter
        const matchesEnrollmentStatus = !selectedEnrollmentStatus.value ||
                                     student.enrollmentStatus === selectedEnrollmentStatus.value;
        
        // Search query
        const matchesSearch = !query || 
                          student.lastName.toLowerCase().includes(query) || 
                          student.firstName.toLowerCase().includes(query) ||
                          student.id.toLowerCase().includes(query);
        
        return matchesAcademicYear && matchesDepartment && matchesCourse && 
               matchesYearLevel && matchesSemester && matchesStatus && 
               matchesEnrollmentStatus && matchesSearch;
      }).sort((a, b) => {
        // Sort by last name, then first name
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
    });
    
    const totalStudents = computed(() => filteredStudents.value.length);
    
    const totalAllStudents = computed(() => students.value.length);
    
    const clearedCount = computed(() => 
      filteredStudents.value.filter(s => s.clearanceStatus === 'Cleared').length
    );
    
    const totalClearedCount = computed(() => 
      students.value.filter(s => s.clearanceStatus === 'Cleared').length
    );
    
    const pendingCount = computed(() => 
      filteredStudents.value.filter(s => s.clearanceStatus === 'Pending').length
    );
    
    const totalPendingCount = computed(() => 
      students.value.filter(s => s.clearanceStatus === 'Pending').length
    );
    
    const enrolledCount = computed(() => 
      filteredStudents.value.filter(s => s.enrollmentStatus === 'Enrolled').length
    );
    
    const totalEnrolledCount = computed(() => 
      students.value.filter(s => s.enrollmentStatus === 'Enrolled').length
    );
    
    // Methods
    const formatDate = (dateString) => {
      if (!dateString) return 'N/A';
      const options = { year: 'numeric', month: 'short', day: 'numeric' };
      return new Date(dateString).toLocaleDateString('en-US', options);
    };
    
    const formatYearLevel = (level) => {
      const levels = ['1st Year', '2nd Year', '3rd Year', '4th Year'];
      return levels[level - 1] || level;
    };
    
    const getStatusSeverity = (status) => {
      switch (status) {
        case 'Cleared': return 'success';
        case 'Pending': return 'warning';
        default: return null;
      }
    };
    
    const getEnrollmentSeverity = (status) => {
      return status === 'Enrolled' ? 'success' : 'info';
    };
    
    const viewStudentDetails = (student) => {
      selectedStudent.value = student;
      displayDialog.value = true;
    };
    
    const markAsEnrolled = (student) => {
      // In a real app, this would be an API call
      const index = students.value.findIndex(s => s.id === student.id);
      if (index !== -1) {
        students.value[index].enrollmentStatus = 'Enrolled';
        // Update the filtered list if needed
        filterStudents();
      }
    };
    
    const clearFilters = () => {
      selectedAcademicYear.value = '';
      selectedDepartment.value = '';
      selectedCourse.value = '';
      selectedYearLevel.value = '';
      selectedSemester.value = '';
      selectedStatus.value = '';
      selectedEnrollmentStatus.value = '';
      searchQuery.value = '';
    };
    
    const exportClearanceData = () => {
      // Export functionality here
      toast.add({
        severity: 'info',
        summary: 'Export',
        detail: 'Exporting clearance data...',
        life: 3000
      });
    };
    
    const handleStatusUpdated = (data) => {
      // Update the student's status and remarks in the local state
      const studentIndex = students.value.findIndex(s => s.id === data.studentId);
      if (studentIndex !== -1) {
        students.value[studentIndex].clearanceStatus = data.cleared ? 'Cleared' : 'Pending';
        if (data.remarks) {
          students.value[studentIndex].remarks = data.remarks;
        }
        // Update the filtered list if needed
        filterStudents();
        
        // Show success message
        toast.add({
          severity: 'success',
          summary: 'Success',
          detail: 'Status updated successfully',
          life: 3000
        });
        
        // Close the dialog after a short delay
        setTimeout(() => {
          displayDialog.value = false;
        }, 500);
      }
    };

    const handleClearanceSubmitted = (data) => {
      // Update the student's clearance date and remarks in the local state
      const studentIndex = students.value.findIndex(s => s.id === data.studentId);
      if (studentIndex !== -1) {
        students.value[studentIndex].dateCleared = new Date().toISOString();
        students.value[studentIndex].clearanceStatus = 'Cleared';
        if (data.requirements && data.requirements.length > 0) {
          students.value[studentIndex].remarks = data.requirements[0]?.remarks || '';
        }
        // Update the filtered list if needed
        filterStudents();
        
        // Show success message
        toast.add({
          severity: 'success',
          summary: 'Success',
          detail: 'Clearance submitted successfully',
          life: 3000
        });
        
        // Close the dialog after a short delay
        setTimeout(() => {
          displayDialog.value = false;
        }, 500);
      }
    };
    
    const onDepartmentChange = () => {
      selectedCourse.value = '';
    };

    const onCourseChange = () => {
      // Additional logic if needed when course changes
    };
    
    const filterByStatus = (status) => {
      if (status === 'Enrolled') {
        selectedStatus.value = ''; // Clear any status filter
        selectedEnrollmentStatus.value = 'Enrolled';
      } else {
        selectedStatus.value = status;
        selectedEnrollmentStatus.value = ''; // Clear enrollment filter when filtering by status
      }
    };
    
    // Simulate API call on component mount
    onMounted(() => {
      loading.value = true;
      // In a real app, fetch data from API
      setTimeout(() => {
        // Mock data loading
        loading.value = false;
      }, 1000);
    });
    
    const closeDialog = () => {
      displayDialog.value = false;
    };
    
    return {
      loading,
      displayDialog,
      searchQuery,
      selectedAcademicYear,
      selectedDepartment,
      selectedCourse,
      selectedYearLevel,
      selectedSemester,
      selectedStatus,
      selectedEnrollmentStatus,
      selectedStudent,
      students,
      academicYears,
      departmentOptions,
      courseOptions,
      filteredCourseOptions,
      yearLevelOptions,
      semesterOptions,
      statusOptions,
      filteredStudents,
      totalStudents,
      totalAllStudents,
      clearedCount,
      totalClearedCount,
      pendingCount,
      totalPendingCount,
      enrolledCount,
      totalEnrolledCount,
      formatDate,
      formatYearLevel,
      getStatusSeverity,
      getEnrollmentSeverity,
      viewStudentDetails,
      markAsEnrolled,
      clearFilters,
      exportClearanceData,
      handleStatusUpdated,
      handleClearanceSubmitted,
      onDepartmentChange,
      onCourseChange,
      filterByStatus,
      closeDialog
    };
  }
};
</script>

<style scoped>
.dsa-container {
  background-color: #fff;
  padding: 1rem;
  border-radius: 12px;
}

/* Stats Cards */
.stats-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin: 1rem 0;
  padding: 0 1rem;
}

.stat-card {
  background: #fff;
  border-radius: 10px;
  padding: 1.25rem;
  display: flex;
  align-items: center;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  transition: transform 0.2s, box-shadow 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

.stat-icon {
  font-size: 1.75rem;
  min-width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 1rem;
  color: white;
  background: var(--primary-color);
}

.stat-icon i {
  font-size: 1.25rem;
}

.stat-content {
  min-width: 0; /* Prevents flex item from overflowing */
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 600;
  line-height: 1.2;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.stat-label {
  font-size: 0.875rem;
  color: var(--text-color-secondary);
  margin-top: 0.25rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.stat-total {
  font-size: 0.8em;
  opacity: 0.8;
  font-weight: normal;
}

.stat-percentage {
  font-size: 0.75rem;
  color: var(--text-secondary-color);
  margin-top: 0.25rem;
}

/* Specific styles for enrolled card */
.stat-card.enrolled .stat-icon {
  background: #4CAF50; /* Green color for enrolled */
}

/* Card styles */
.card {
  display: flex;
  flex-direction: column;
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
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

/* Filter section */
.filter-section {
  display: flex;
  padding: 1.25rem;
  margin: 1.5rem;
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
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
}

.filter-search {
  flex: 3.5;
  min-width: 200px;
}

/* Table styles */
:deep(.p-datatable) {
  font-size: 0.875rem;
}

:deep(.p-datatable .p-datatable-thead > tr > th) {
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.8rem;
  letter-spacing: 0.5px;
  color: var(--text-color-secondary);
  border: none;
  padding: 0.5rem 0.75rem;
  white-space: nowrap;
  text-align: left;
}

:deep(.p-datatable .p-datatable-tbody > tr) {
  transition: background-color 0.2s;
}

:deep(.p-datatable .p-datatable-tbody > tr > td) {
  padding: 0.5rem 0.75rem;
  border: none;
  border-bottom: 1px solid #e9ecef;
  font-size: 1rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 200px;
}

:deep(.p-datatable .p-datatable-tbody > tr:last-child > td) {
  border-bottom: none;
}

:deep(.p-datatable .p-datatable-tbody > tr:hover) {
  background-color: #f8f9fa;
}

/* Status tags */
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

:deep(.p-tag.status-enrolled) {
  background-color: #cbb6fa;
  color: #32254f;
  border-color: #ab86fc;
}

/* Color themes for status cards */
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

.stat-card.enrolled {
  border-left: 4px solid #7c3aed;
}

.stat-card.enrolled .stat-icon {
  background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%);
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
  
  .stats-container {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 576px) {
  .stats-container {
    grid-template-columns: 1fr;
  }
  
  .filter-group {
    flex: 1 0 100%;
  }
  
  .filter-section {
    padding: 1rem;
    margin: 1rem 0;
  }
}

.p-dropdown {
  width: 100%;
}

/* Compact table styles */
:deep(.compact-table) {
  font-size: 0.85rem;
}

:deep(.compact-table .p-datatable-thead > tr > th),
:deep(.compact-table .p-datatable-tbody > tr > td) {
  padding: 0.3rem 0.5rem;
}

:deep(.compact-table .p-tag) {
  font-size: 0.8rem;
  padding: 0.15rem 0.4rem;
}

:deep(.compact-table .p-datatable-wrapper) {
  overflow-x: auto;
  max-width: 100%;
}
</style>