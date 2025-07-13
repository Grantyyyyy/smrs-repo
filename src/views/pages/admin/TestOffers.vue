<script setup>
import Button from 'primevue/button';
import Column from 'primevue/column';
import DataTable from 'primevue/datatable';
import Dialog from 'primevue/dialog';
import Dropdown from 'primevue/dropdown';
import InputText from 'primevue/inputtext';
import { useToast } from 'primevue/usetoast';
import { computed, ref, watch } from 'vue';

const toast = useToast();

// Data
const departments = ref([
  { name: 'CMAS (College of Marine and Allied Sciences)', code: 'CMAS' },
  { name: 'CBAA (College of Business Administration & Accountancy)', code: 'CBAA' },
  { name: 'CAFES (College of Agriculture, Forestry, and Environmental Sciences)', code: 'CAFES' }
]);

const selectedDepartment = ref(null);
const selectedSubject = ref(null);
const showSubjectTable = ref(true);
const showAddSubjectDialog = ref(false);
const showAddInstructorDialog = ref(false);

// Dynamic Data Stores
const subjects = ref([]);
const schedules = ref([]);

const newSchedule = ref({ day: '', time: '', room: '', section: '' });
const newInstructor = ref({ name: '', scheduleId: null });

const availableSubjects = ref([
  { name: 'English' }, { name: 'Science' }, { name: 'Math' },
  { name: 'History' }, { name: 'Literature' }, { name: 'Philosophy' }
]);

const dayOptions = ref([
  'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday',
  'Monday-Thursday', 'Monday-Wednesday-Friday', 'Tuesday-Thursday', 
  'Tuesday-Thursday-Friday', 'Wednesday-Saturday'
]);

const timeOptions = ref([
  '7:30am - 9:00am',
  '9:00am - 11:30am',
  '1:00pm - 3:00pm',
  '3:00pm - 5:00pm',
  '5:00pm - 7:00pm'
]);

// Computed
const filteredSubjects = computed(() => {
  if (!selectedDepartment.value) return [];
  return subjects.value.filter(s => s.department === selectedDepartment.value.code);
});

const filteredSchedules = computed(() => {
  if (!selectedSubject.value) return [];
  return schedules.value.filter(s => s.subjectId === selectedSubject.value.id);
});

// Watchers
watch(selectedDepartment, () => {
  selectedSubject.value = null;
  showSubjectTable.value = true;
});

// Methods
const openSchedules = (subject) => {
  selectedSubject.value = subject;
  showSubjectTable.value = false;
};

const backToSubjects = () => {
  selectedSubject.value = null;
  showSubjectTable.value = true;
};

const addSubject = (subjectName) => {
  if (!selectedDepartment.value) {
    toast.add({ severity: 'warn', summary: 'Select Department', detail: 'Please select a department first.', life: 3000 });
    return;
  }

  const newId = subjects.value.length + 1;
  const newCode = subjectName.substring(0, 3).toUpperCase() + newId;
  const departmentCode = selectedDepartment.value.code;

  subjects.value.push({
    id: newId,
    code: newCode,
    name: subjectName,
    department: departmentCode
  });

  showAddSubjectDialog.value = false;
  toast.add({ severity: 'success', summary: 'Success', detail: 'Subject added', life: 3000 });
};

const addSchedule = () => {
  if (!newSchedule.value.day || !newSchedule.value.time || !newSchedule.value.room || !newSchedule.value.section) {
    toast.add({ severity: 'error', summary: 'Error', detail: 'All schedule fields are required', life: 3000 });
    return;
  }

  schedules.value.push({
    id: schedules.value.length + 1,
    subjectId: selectedSubject.value.id,
    ...newSchedule.value,
    instructor: ''
  });

  newSchedule.value = { day: '', time: '', room: '', section: '' };
  toast.add({ severity: 'success', summary: 'Success', detail: 'Schedule added', life: 3000 });
};

const addInstructor = (scheduleId) => {
  if (!newInstructor.value.name) {
    toast.add({ severity: 'error', summary: 'Error', detail: 'Instructor name is required', life: 3000 });
    return;
  }

  const schedule = schedules.value.find(s => s.id === scheduleId);
  if (schedule) {
    schedule.instructor = newInstructor.value.name;
    newInstructor.value = { name: '', scheduleId: null };
    showAddInstructorDialog.value = false;
    toast.add({ severity: 'success', summary: 'Success', detail: 'Instructor added', life: 3000 });
  }
};

const deleteSchedule = (schedule) => {
  schedules.value = schedules.value.filter(s => s.id !== schedule.id);
  toast.add({ severity: 'success', summary: 'Deleted', detail: 'Schedule deleted', life: 3000 });
};

const deleteSubject = (subject) => {
  subjects.value = subjects.value.filter(s => s.id !== subject.id);
  schedules.value = schedules.value.filter(s => s.subjectId !== subject.id);
  toast.add({ severity: 'success', summary: 'Deleted', detail: 'Subject deleted', life: 3000 });
};
</script>

<template>
  <div class="card">
    <h1>Academic Year: 2025-2026 || 2nd Semester</h1>
    
    <!-- Department Selector -->
    <div class="mb-6">
      <div class="flex items-center gap-4 mb-4">
        <h2>Department:</h2>
        <Dropdown 
          v-model="selectedDepartment" 
          :options="departments" 
          optionLabel="name" 
          placeholder="Select Department" 
          class="w-100 md:w-14rem" 
        />
      </div>
      
      <!-- Table Title and Add Button -->
      <div class="flex justify-between items-center mb-4">
        <h2 v-if="showSubjectTable" class="text-xl font-semibold">Subject List</h2>
        <h2 v-else class="text-xl font-semibold">Schedules for {{ selectedSubject?.name }}</h2>
        
        <Button 
          v-if="showSubjectTable"
          label="Add Subject" 
          icon="pi pi-plus" 
          @click="showAddSubjectDialog = true" 
          class="ml-auto"
        />
        <Button 
          v-else
          label="Back to Subjects" 
          icon="pi pi-arrow-left" 
          @click="backToSubjects" 
          class="ml-auto"
        />
      </div>
      
      <!-- Subject Table (shown when showSubjectTable is true) -->
      <DataTable 
        v-if="showSubjectTable"
        :value="filteredSubjects" 
        :paginator="true" 
        :rows="5" 
        :rowsPerPageOptions="[5, 10, 25]"
        paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink RowsPerPageDropdown"
      >
        <Column field="code" header="Subject Code" sortable></Column>
        <Column field="name" header="Descriptive Title" sortable></Column>
        <Column header="Actions" style="min-width: 10rem">
          <template #body="{ data }">
            <Button 
              icon="pi pi-eye" 
              outlined 
              rounded 
              class="mr-2" 
              @click="openSchedules(data)" 
              severity="info"
              v-tooltip.top="'View Schedules'"
            />
            <Button 
              icon="pi pi-trash" 
              outlined 
              rounded 
              severity="danger"
              @click="deleteSubject(data)" 
              v-tooltip.top="'Delete Subject'"
            />
          </template>
        </Column>
      </DataTable>
      
      <!-- Schedule Table (shown when showSubjectTable is false) -->
      <div v-else>
        <DataTable 
          :value="filteredSchedules" 
          :paginator="true" 
          :rows="5" 
          :rowsPerPageOptions="[5, 10, 25]"
          paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink RowsPerPageDropdown"
        >
          <Column field="day" header="Day" sortable></Column>
          <Column field="time" header="Time" sortable></Column>
          <Column field="room" header="Room" sortable></Column>
          <Column field="section" header="Section" sortable></Column>
          <Column field="instructor" header="Instructor" sortable>
            <template #body="{ data }">
              <span v-if="data.instructor">{{ data.instructor }}</span>
              <Button 
                v-else
                icon="pi pi-user-plus" 
                label="Add" 
                outlined
                @click="showAddInstructorDialog = true; newInstructor.scheduleId = data.id" 
              />
            </template>
          </Column>
          <Column header="Actions" style="min-width: 8rem">
            <template #body="{ data }">
              <Button 
                icon="pi pi-trash" 
                outlined 
                rounded 
                severity="danger"
                @click="deleteSchedule(data)" 
              />
            </template>
          </Column>
        </DataTable>

        
        <div class="p-4 border-round border-1 surface-border mt-4">
          <h3 class="mb-3">Add New Schedule</h3>
          <div class="grid">
            <!-- Day Field with Dropdown -->
            <div class="col-12 md:col-3">
              <label class="block font-bold mb-2">Day</label>
              <Dropdown 
                v-model="newSchedule.day"
                :options="dayOptions"
                placeholder="Select or type day"
                editable
                class="w-full"
              />
            </div>
            
            <!-- Time Field with Dropdown -->
            <div class="col-12 md:col-3">
              <label class="block font-bold mb-2">Time</label>
              <Dropdown 
                v-model="newSchedule.time"
                :options="timeOptions"
                placeholder="Select or type time"
                editable
                class="w-full"
              />
            </div>
            
            <!-- Room Field (regular input) -->
            <div class="col-12 md:col-3">
              <label class="block font-bold mb-2">Room</label>
              <InputText 
                v-model="newSchedule.room" 
                placeholder="Room 101" 
                class="w-full" 
              />
            </div>
            
            <!-- Section Field (regular input) -->
            <div class="col-12 md:col-3">
              <label class="block font-bold mb-2">Section</label>
              <InputText 
                v-model="newSchedule.section" 
                placeholder="Section A" 
                class="w-full" 
              />
            </div>
          </div>
          <Button 
            label="Add Schedule" 
            icon="pi pi-plus" 
            @click="addSchedule" 
            class="mt-3" 
            :disabled="!newSchedule.day || !newSchedule.time || !newSchedule.room || !newSchedule.section"
          />
        </div>
      </div>
    </div>

    <!-- Add Subject Dialog -->
    <Dialog 
      v-model:visible="showAddSubjectDialog" 
      header="Add New Subject" 
      :style="{ width: '450px' }" 
      :modal="true"
    >
      <div class="grid">
        <div v-for="(subject, index) in availableSubjects" :key="index" class="col-6">
          <Button 
            :label="subject.name" 
            @click="addSubject(subject.name)"
            class="w-full mb-2" 
            outlined
          />
        </div>
      </div>
      <template #footer>
        <Button label="Cancel" icon="pi pi-times" text @click="showAddSubjectDialog = false" />
      </template>
    </Dialog>

    <!-- Add Instructor Dialog -->
    <Dialog 
      v-model:visible="showAddInstructorDialog" 
      header="Add Instructor" 
      :style="{ width: '450px' }" 
      :modal="true"
    >
      <div class="field">
        <label class="block font-bold mb-2">Instructor Name</label>
        <InputText v-model="newInstructor.name" placeholder="Enter instructor name" class="w-full" />
      </div>
      <template #footer>
        <Button label="Cancel" icon="pi pi-times" text @click="showAddInstructorDialog = false" />
        <Button 
          label="Add" 
          icon="pi pi-check" 
          @click="addInstructor(newInstructor.scheduleId)" 
          :disabled="!newInstructor.name"
        />
      </template>
    </Dialog>
  </div>
</template>

<style scoped>
.card {
  padding: 2rem;
}

h1 {
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  color: var(--text-color);
}

h2 {
  font-size: 1.25rem;
  color: var(--text-color);
}

h3 {
  font-size: 1.1rem;
  color: var(--text-color-secondary);
}

.grid {
  margin: 0 -0.5rem;
}

.col-6, .col-4, .col-12 {
  padding: 0.5rem;
}

.border-round {
  border-radius: 6px;
}

.surface-border {
  border-color: var(--surface-border);
}

.p-datatable {
  font-size: 0.9rem;
}

.p-datatable .p-column-header-content {
  font-weight: 600;
}

.p-dropdown {
  width: 100;
}

.text-xl {
  font-size: 1.25rem;
}

.font-semibold {
  font-weight: 600;
}
</style>