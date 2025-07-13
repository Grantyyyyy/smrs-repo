<script setup>
import { useToast } from 'primevue/usetoast';
import { computed, ref } from 'vue';

// PrimeVue Components
import Button from 'primevue/button';
import Column from 'primevue/column';
import DataTable from 'primevue/datatable';
import Dialog from 'primevue/dialog';
import Dropdown from 'primevue/dropdown';
import InputText from 'primevue/inputtext';
import ProgressSpinner from 'primevue/progressspinner';
import Tag from 'primevue/tag';
import Toast from 'primevue/toast';

const toast = useToast();

// ========== SAMPLE DATA ========== //
const departments = ref([
  { code: 'CMAS', name: 'College of Marine and Allied Sciences' },
  { code: 'CBAA', name: 'College of Business Administration' },
  { code: 'CAFES', name: 'College of Agriculture' }
]);

const teachers = ref([
  { id: 101, fullName: 'Dr. Maria Santos', department: 'CMAS', status: 'Full-Time' },
  { id: 102, fullName: 'Prof. Carlos Reyes', department: 'CMAS', status: 'Part-Time' },
  { id: 201, fullName: 'Dr. Juan Dela Cruz', department: 'CBAA', status: 'Full-Time' },
  { id: 202, fullName: 'Prof. Anna Lopez', department: 'CBAA', status: 'Full-Time' },
  { id: 301, fullName: 'Dr. Robert Lim', department: 'CAFES', status: 'Full-Time' },
  { id: 302, fullName: 'Prof. Sofia Garcia', department: 'CAFES', status: 'Part-Time' }
]);

const subjects = ref([
  { id: 1001, code: 'OCEAN101', name: 'Marine Biology', department: 'CMAS', units: 3 },
  { id: 1002, code: 'CHEM201', name: 'Marine Chemistry', department: 'CMAS', units: 4 },
  { id: 2001, code: 'ACCTG101', name: 'Financial Accounting', department: 'CBAA', units: 3 },
  { id: 2002, code: 'MKTG201', name: 'Marketing Principles', department: 'CBAA', units: 3 },
  { id: 3001, code: 'AGRI101', name: 'Crop Science', department: 'CAFES', units: 4 },
  { id: 3002, code: 'ANSC201', name: 'Animal Nutrition', department: 'CAFES', units: 3 }
]);

const courses = ref([
  { code: 'BSMS', name: 'BS Marine Science' },
  { code: 'BSA', name: 'BS Accountancy' },
  { code: 'BSAG', name: 'BS Agriculture' }
]);

const yearLevels = ref([1, 2, 3, 4]);

const teacherAssignments = ref([
  { teacherId: 101, subjectId: 1001, sections: [
    { section: 'A', day: 'MWF', time: '7:30-9:00', room: 'Lab 101', course: 'BSMS', yearLevel: 2 }
  ]},
  { teacherId: 101, subjectId: 1002, sections: [
    { section: 'A', day: 'TTH', time: '9:00-10:30', room: 'Lab 102', course: 'BSMS', yearLevel: 3 },
    { section: 'B', day: 'MWF', time: '1:00-2:30', room: 'Lab 105', course: 'BSMS', yearLevel: 2 }
  ]},
  { teacherId: 201, subjectId: 2001, sections: [
    { section: 'A', day: 'MWF', time: '8:00-9:30', room: 'Room 201', course: 'BSA', yearLevel: 1 }
  ]},
  { teacherId: 301, subjectId: 3001, sections: [
    { section: 'A', day: 'MWF', time: '7:00-8:30', room: 'Farm Lab 1', course: 'BSAG', yearLevel: 1 }
  ]}
]);

// ========== REACTIVE STATES ========== //
const selectedDepartment = ref({});
const selectedTeacher = ref(null);
const selectedTeacherDetails = ref(null);
const showAssignmentDialog = ref(false);
const currentView = ref('teachers');
const isLoading = ref(false);
const showSectionAssignmentDialog = ref(false);

const currentAssignment = ref({
  subjectId: null,
  subjectName: '',
  section: '',
  day: '',
  time: '',
  room: '',
  course: null,
  yearLevel: null
});

const newAssignment = ref({
  subjectId: null,
  section: '',
  day: '',
  time: '',
  room: '',
  course: null,
  yearLevel: null
});

// ========== COMPUTED PROPERTIES ========== //
const filteredTeachers = computed(() => {
  if (!selectedDepartment.value?.code) return [];
  return teachers.value.filter(t => t.department === selectedDepartment.value.code);
});

const teacherSubjects = computed(() => {
  if (!selectedTeacher.value) return [];
  return teacherAssignments.value
    .filter(ta => ta.teacherId === selectedTeacher.value)
    .flatMap(ta => {
      const subject = subjects.value.find(s => s.id === ta.subjectId);
      return ta.sections.map(section => ({
        ...section,
        subjectCode: subject.code,
        subjectName: subject.name,
        units: subject.units
      }));
    });
});

const availableSubjects = computed(() => {
  if (!selectedDepartment.value?.code) return [];
  return subjects.value.filter(s => s.department === selectedDepartment.value.code);
});

// ========== METHODS ========== //
const viewTeacherSubjects = async (teacherId) => {
  isLoading.value = true;
  await new Promise(resolve => setTimeout(resolve, 500));
  selectedTeacher.value = teacherId;
  selectedTeacherDetails.value = teachers.value.find(t => t.id === teacherId);
  currentView.value = 'load';
  isLoading.value = false;
};

const backToTeachers = () => {
  currentView.value = 'teachers';
  selectedTeacher.value = null;
};

const addAssignment = () => {
  if (!newAssignment.value.section) {
    const existingSections = teacherAssignments.value
      .filter(ta => ta.teacherId === selectedTeacher.value && ta.subjectId === newAssignment.value.subjectId)
      .flatMap(ta => ta.sections.map(s => s.section));
    const nextCharCode = 65 + (existingSections.length || 0);
    newAssignment.value.section = String.fromCharCode(nextCharCode);
  }

  let assignment = teacherAssignments.value.find(ta => 
    ta.teacherId === selectedTeacher.value && 
    ta.subjectId === newAssignment.value.subjectId
  );

  if (!assignment) {
    assignment = {
      teacherId: selectedTeacher.value,
      subjectId: newAssignment.value.subjectId,
      sections: []
    };
    teacherAssignments.value.push(assignment);
  }

  assignment.sections.push({ ...newAssignment.value });

  toast.add({
    severity: 'success',
    summary: 'Assignment Added',
    detail: `Added ${newAssignment.value.section} to teacher's schedule`,
    life: 3000
  });

  showAssignmentDialog.value = false;
  newAssignment.value = {
    subjectId: null,
    section: '',
    day: '',
    time: '',
    room: '',
    course: null,
    yearLevel: null
  };
};

const calculateWorkload = (teacherId) => {
  const assignments = teacherAssignments.value.filter(ta => ta.teacherId === teacherId);
  return {
    totalSubjects: assignments.length,
    totalSections: assignments.reduce((sum, ta) => sum + ta.sections.length, 0),
    totalUnits: assignments.reduce((sum, ta) => {
      const subject = subjects.value.find(s => s.id === ta.subjectId);
      return sum + (subject?.units || 0) * ta.sections.length;
    }, 0)
  };
};

const openSectionAssignment = (subjectData) => {
  currentAssignment.value = {
    subjectId: subjectData.subjectId || teacherSubjects.value.find(s => s.subjectCode === subjectData.subjectCode)?.subjectId,
    subjectName: `${subjectData.subjectCode} - ${subjectData.subjectName}`,
    section: subjectData.section || '',
    day: subjectData.day || '',
    time: subjectData.time || '',
    room: subjectData.room || '',
    course: subjectData.course || null,
    yearLevel: subjectData.yearLevel || null
  };
  showSectionAssignmentDialog.value = true;
};

const saveSectionAssignment = () => {
  // Find or create teacher assignment
  let assignment = teacherAssignments.value.find(ta => 
    ta.teacherId === selectedTeacher.value && 
    ta.subjectId === currentAssignment.value.subjectId
  );

  if (!assignment) {
    assignment = {
      teacherId: selectedTeacher.value,
      subjectId: currentAssignment.value.subjectId,
      sections: []
    };
    teacherAssignments.value.push(assignment);
  }

  // Update or add section
  const existingSectionIndex = assignment.sections.findIndex(s => 
    s.section === currentAssignment.value.section
  );
  
  if (existingSectionIndex >= 0) {
    assignment.sections[existingSectionIndex] = { ...currentAssignment.value };
  } else {
    assignment.sections.push({ ...currentAssignment.value });
  }

  toast.add({
    severity: 'success',
    summary: 'Assignment Updated',
    detail: `${currentAssignment.value.subjectName} assigned to ${courses.value.find(c => c.code === currentAssignment.value.course)?.name}`,
    life: 3000
  });

  showSectionAssignmentDialog.value = false;
};
</script>

<template>
  <div class="card">
    <Toast />
    
    <!-- Dynamic Header with Back Button -->
    <div class="header-container">
      <h1 v-if="currentView === 'teachers'">Teachers Workload</h1>
      <h1 v-else>{{ selectedDepartment.name }} Department</h1>
      
      <Button 
        v-if="currentView === 'load'"
        icon="pi pi-arrow-left" 
        label="Back to Teachers" 
        @click="backToTeachers"
        class="p-button-text back-button"
      />
    </div>

    <!-- Loading Overlay -->
    <div v-if="isLoading" class="loading-overlay">
      <ProgressSpinner />
      <span class="loading-text">Loading teaching load...</span>
    </div>

    <!-- Department Selection -->
    <Transition name="fade">
      <div class="p-fluid mb-4" v-if="currentView === 'teachers'">
        <div class="field">
          <label>Select Department : </label>
          <Dropdown 
            v-model="selectedDepartment" 
            :options="departments" 
            optionLabel="name"
            placeholder="Choose department"
            class="mb-3"
          />
        </div>
      </div>
    </Transition>

    <!-- Main Content Area -->
    <Transition name="slide-fade" mode="out-in">
      <!-- Teachers Table View -->
      <div v-if="currentView === 'teachers'" key="teachers-view" class="view-container">
        <DataTable 
          v-if="selectedDepartment.code"
          :value="filteredTeachers" 
          class="p-datatable-sm"
          :paginator="true"
          :rows="5"
          :loading="isLoading"
        >
          <Column field="id" header="ID" sortable></Column>
          <Column field="fullName" header="Teacher Name" sortable></Column>
          <Column field="status" header="Status" sortable></Column>
          <Column header="Workload">
            <template #body="{ data }">
              <Tag 
                :value="`${calculateWorkload(data.id).totalSubjects} subjects`"
                severity="info"
                class="mr-2"
              />
              <Tag 
                :value="`${calculateWorkload(data.id).totalUnits} units`"
                severity="success"
              />
            </template>
          </Column>
          <Column header="Actions">
            <template #body="{ data }">
              <Button 
                icon="pi pi-list"
                label="View Load"
                @click="viewTeacherSubjects(data.id)"
                :loading="isLoading && selectedTeacher === data.id"
              />
            </template>
          </Column>
        </DataTable>
      </div>

      <!-- Teacher Load View -->
      <div v-else key="load-view" class="view-container">
        <div class="flex justify-content-between align-items-center mb-3">
          <h2>
            Teaching Load: {{ selectedTeacherDetails?.fullName }}
            <!-- <Tag :value="selectedDepartment.name" class="ml-2" /> -->
          </h2>
          
          <!-- 
            <Button 
            icon="pi pi-plus" 
            label="Add Assignment" 
            @click="showAssignmentDialog = true"
          /> 
          -->
          
        </div>

        <DataTable :value="teacherSubjects" class="p-datatable-sm">
          <Column field="subjectCode" header="Code" sortable></Column>
          <Column field="subjectName" header="Subject" sortable></Column>
          <Column field="units" header="Units" sortable></Column>
          <Column field="section" header="Section" sortable></Column>
          <Column field="day" header="Day" sortable></Column>
          <Column field="time" header="Time" sortable></Column>
          <Column field="room" header="Room" sortable></Column>
          <Column field="course" header="Course" sortable>
            <template #body="{ data }">
              {{ courses.find(c => c.code === data.course)?.name || data.course }}
            </template>
          </Column>
          <Column field="yearLevel" header="Year" sortable></Column>
          <Column header="Actions">
            <template #body="{ data }">
              <Button 
                icon="pi pi-book" 
                label="Assign" 
                class="p-button-sm"
                @click="openSectionAssignment(data)"
              />
            </template>
          </Column>
        </DataTable>

        <div class="mt-3 p-3 surface-100 border-round">
          <div class="flex grid-cols-3 gap-2">
            <div class="col-4">
              <div class="text-500 font-medium">Total Subjects</div>
              <div class="text-900 font-bold text-xl text-center">
                {{ calculateWorkload(selectedTeacher).totalSubjects }}
              </div>
            </div>
            <div class="col-4">
              <div class="text-500 font-medium">Total Sections</div>
              <div class="text-900 font-bold text-xl text-center">
                {{ calculateWorkload(selectedTeacher).totalSections }}
              </div>
            </div>
            <div class="col-4">
              <div class="text-500 font-medium">Total Units</div>
              <div class="text-900 font-bold text-xl text-center">
                {{ calculateWorkload(selectedTeacher).totalUnits }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </Transition>

    <Dialog 
      v-model:visible="showSectionAssignmentDialog" 
      header="Assign Subject to Course"
      :style="{ width: '30vw' }"
      :modal="true"
    >
      <div class="p-fluid">
        <div class="field">
          <label>Course</label>
          <Dropdown 
            v-model="currentAssignment.course"
            :options="courses"
            optionLabel="name"
            optionValue="code"
            placeholder="Select course"
            class="mb-3"
          />
        </div>
        
        <div class="field">
          <label>Year Level</label>
          <Dropdown 
            v-model="currentAssignment.yearLevel"
            :options="yearLevels"
            placeholder="Select year"
          />
        </div>
      </div>

      <template #footer>
        <Button label="Cancel" icon="pi pi-times" @click="showSectionAssignmentDialog = false" text />
        <Button label="Assign" icon="pi pi-check" @click="saveSectionAssignment" />
      </template>
    </Dialog>

    <!-- Assignment Dialog -->
    <Dialog 
      v-model:visible="showAssignmentDialog" 
      header="New Teaching Assignment"
      :style="{ width: '50vw' }"
      :modal="true"
    >
      <div class="p-fluid">
        <div class="field">
          <label>Subject</label>
          <Dropdown 
            v-model="newAssignment.subjectId"
            :options="availableSubjects"
            optionLabel="name"
            optionValue="id"
            placeholder="Select subject"
            class="mb-3"
          />
        </div>

        <div class="grid">
          <div class="col-6 field">
            <label>Section</label>
            <InputText v-model="newAssignment.section" placeholder="A" />
          </div>
          <div class="col-6 field">
            <label>Day</label>
            <Dropdown 
              v-model="newAssignment.day"
              :options="['MWF', 'TTH', 'M-F', 'M', 'T', 'W', 'TH', 'F']"
              placeholder="Select day"
            />
          </div>
        </div>

        <div class="grid">
          <div class="col-6 field">
            <label>Time</label>
            <Dropdown 
              v-model="newAssignment.time"
              :options="[
                '7:30-9:00', '8:00-9:30', '9:00-10:30', 
                '10:00-11:30', '1:00-2:30', '3:00-4:30'
              ]"
              placeholder="Select time"
            />
          </div>
          <div class="col-6 field">
            <label>Room</label>
            <InputText v-model="newAssignment.room" placeholder="Room/Lab" />
          </div>
        </div>

        <div class="grid">
          <div class="col-6 field">
            <label>Course</label>
            <Dropdown 
              v-model="newAssignment.course"
              :options="courses"
              optionLabel="name"
              optionValue="code"
              placeholder="Select course"
            />
          </div>
          <div class="col-6 field">
            <label>Year Level</label>
            <Dropdown 
              v-model="newAssignment.yearLevel"
              :options="yearLevels"
              placeholder="Select year"
            />
          </div>
        </div>
      </div>

      <template #footer>
        <Button label="Cancel" icon="pi pi-times" @click="showAssignmentDialog = false" text />
        <Button label="Assign" icon="pi pi-check" @click="addAssignment" />
      </template>
    </Dialog>
  </div>
</template>

<style scoped>
/* Header Styles */
.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.back-button {
  margin-left: auto;
}

/* Loading Overlay */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.8);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  gap: 1rem;
}

.loading-text {
  font-size: 1.2rem;
  color: var(--primary-color);
}

/* Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.3s cubic-bezier(1, 0.5, 0.8, 1);
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateX(20px);
  opacity: 0;
}

/* View Containers */
.view-container {
  min-height: 300px;
}

/* Table Styles */
.p-datatable {
  font-size: 0.9rem;
}

.p-datatable .p-column-header-content {
  font-weight: 600;
}

/* Responsive Adjustments */
@media screen and (max-width: 768px) {
  .header-container {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .back-button {
    align-self: flex-end;
  }
  
  .grid > div {
    width: 100% !important;
  }
  
  .p-dialog {
    width: 95vw !important;
  }
}
</style>