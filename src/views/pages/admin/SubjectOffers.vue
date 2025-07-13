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
        <h2 v-if="subjectOffering" class="text-xl font-semibold">Subject List</h2>
        <h2 v-else class="text-xl font-semibold">
          Schedules for {{ subjectSchedules[0]?.subject_offering?.name || 'this subject' }}
        </h2>

        
        <Button 
          v-if="subjectOffering"
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
      
      <!-- Subject Table  -->
      <DataTable 
        v-if="subjectOffering"
        :value="subjectOffering" 
        :paginator="true" 
        :rows="5" 
        :rowsPerPageOptions="[5, 10, 25]"
        paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink RowsPerPageDropdown"
      >
        <Column field="subject.code" header="Subject Code" sortable></Column>
        <Column field="subject.name" header="Descriptive Title" sortable></Column>
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
              @click="confirmDeleteOfferedSubject(data)" 
              v-tooltip.top="'Delete Subject'"
            />
          </template>
        </Column>
      </DataTable>
      
      <!-- Schedule Table -->
      <div v-else>
        <DataTable 
          :value="subjectSchedules" 
          :paginator="true" 
          :rows="5" 
          :rowsPerPageOptions="[5, 10, 25]"
          paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink RowsPerPageDropdown"
        >
          <Column field="day" header="Day" sortable></Column>
          <Column field="time" header="Time" sortable></Column>
          <!-- <Column field="room" header="Room" sortable></Column> -->
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
                @click="confirmDeleteSchedule(data)" 
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
                v-model="scheduleForm.day"
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
                v-model="scheduleForm.time"
                :options="timeOptions"
                placeholder="Select or type time"
                editable
                class="w-full"
              />
            </div>
            
            <!-- Room Field (regular input) -->
            <!-- <div class="col-12 md:col-3">
              <label class="block font-bold mb-2">Room</label>
              <InputText 
                v-model="newSchedule.room" 
                placeholder="Room 101" 
                class="w-full" 
              />
            </div> -->
            
            <!-- Section Field (regular input) -->
            <div class="col-12 md:col-3">
              <label class="block font-bold mb-2">Section</label>
              <InputText 
                v-model="scheduleForm.section" 
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
            :disabled="!scheduleForm.day || !scheduleForm.time  || !scheduleForm.section"
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
        <div v-for="(subject, index) in connectedSubjects" :key="index" class="col-6">
          <Button 
            :label="subject.name" 
            :disabled="subject.is_offered"
            @click="addSubjectOffer(subject)"
            class="w-full mb-2" 
            outlined
            :style="subject.is_offered ? 'cursor:not-allowed' : ''"
          />
        </div>
      </div>
      <template #footer>
        <Button label="Cancel" 
        icon="pi pi-times" text 
        @click="showAddSubjectDialog = false" />
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

    <Dialog 
      v-model:visible="deleteOfferedSubjectDialog" 
      :style="{ width: '450px' }" 
      header="Confirm" 
      :modal="true"
      :closable="!loading"
    >
      <div class="flex items-center gap-4">
        <i class="pi pi-exclamation-triangle text-red-500 text-2xl" />
        <span v-if="subjectToDelete">Are you sure you want to delete <b>{{ subjectToDelete.subject.code }} {{ subjectToDelete.subject.name }}</b> ?</span>
      </div>
      <template #footer>
        <Button 
          label="No" 
          icon="pi pi-times" 
          class="p-button-text" 
          @click="deleteOfferedSubjectDialog = false" 
          :disabled="loading" 
        />
        <Button 
          label="Yes" 
          icon="pi pi-check" 
          class="p-button-danger" 
          @click="confirmDeleteOfferedSubject" 
          :loading="loading" 
        />
      </template>
    </Dialog>

    <Dialog 
      v-model:visible="deleteScheduleDialog"
      :style="{ width: '450px' }" 
      header="Confirm" 
      :modal="true"
      :closable="!loading"
    >
      <div class="flex items-center gap-4">
        <i class="pi pi-exclamation-triangle text-red-500 text-2xl" />
        <span v-if="scheduleToDelete">Are you sure you want to delete <b>{{ scheduleToDelete.day }} {{ scheduleToDelete.time }} </b> ?</span>
      </div>
      <template #footer>
        <Button 
          label="No" 
          icon="pi pi-times" 
          class="p-button-text" 
          @click="deleteScheduleDialog = false" 
          :disabled="loading" 
        />
        <Button 
          label="Yes" 
          icon="pi pi-check" 
          class="p-button-danger" 
          @click="deleteSchedule(scheduleToDelete.id)" 
          :loading="loading" 
        />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { Department, Schedule, Subject, SubjectOffering } from '@/service/academicService';
import Button from 'primevue/button';
import Column from 'primevue/column';
import DataTable from 'primevue/datatable';
import Dialog from 'primevue/dialog';
import Dropdown from 'primevue/dropdown';
import InputText from 'primevue/inputtext';
import { useToast } from 'primevue/usetoast';
import { onMounted, reactive, ref, watch } from 'vue';

const toast = useToast();
const departments = ref([]);
const loading = ref(false);

const submitted = ref(false);


const showSubjectTable = ref(true);
const showAddSubjectDialog = ref(false);
const showAddInstructorDialog = ref(false);
const subjects = ref([]);
const newInstructor = ref({ 
  name: '', 
  scheduleId: null 
});

const deleteOfferedSubjectDialog = ref(false);
const deleteScheduleDialog = ref(false);

const selectedDepartment = ref(null);
const subjectOffering = ref([]);
const connectedSubjects = ref([]);

const selectedSubject = ref(null);
const subjectSchedules = ref([]);

const subjectToDelete = ref(null);
const scheduleToDelete = ref(null);

const offerForm = reactive({
  subject: null,
  department: null
})
const scheduleForm = reactive({
  day:'',
  time: '',
  section: ''
})
const newInstructorForm = reactive({
  name: '',
})

onMounted(async () => {
  loading.value = true
  try {
    const [departmentsRes, subjectsRes] = await Promise.all([
      Department.getAll(),
      Subject.getAll(),
    ]);
    departments.value = departmentsRes.data;
    subjects.value = subjectsRes.data;
    console.log('Departments loaded:', departments.value);
    console.log('Subjects loaded:', subjects.value);
  } catch (error) {
    console.error('Failed to load departments and subjects:', error);
  } finally {
    loading.value = false
  }
});

watch(selectedDepartment, async (newDepartment) => {
  if (newDepartment) {
    try {
      const [subjectsOfferingRes, connectedSubjectsRes] = await Promise.all([
        SubjectOffering.getBydeparment(newDepartment.id),
        Department.getConnectedSubjects(newDepartment.id)
      ]);
      subjectOffering.value = subjectsOfferingRes.data;
      connectedSubjects.value = connectedSubjectsRes.data;
      console.log('Subject offerings loaded:', subjectOffering.value);
      console.log('Connected subjects loaded:', connectedSubjects.value);
    }catch (error) {
      console.error('Failed to load subjects:', error);
    }
  } else {
    subjectOffering.value = [];
  }
})

const openSchedules = async (offering) => {
  selectedSubject.value = offering;
  subjectOffering.value = false;

  try {
    const res = await SubjectOffering.getBySubjectOffers(offering.id);
    subjectSchedules.value = res.data;
  }catch (error) {
    console.error('Failed to load schedules:', error);
    toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to load schedules', life: 3000 });
  }

};

const backToSubjects = async () => {
  showSubjectTable.value = true;
  selectedSubject.value = null;
  subjectSchedules.value = [];

  try {
    if (selectedDepartment.value) {
      const res = await SubjectOffering.getBydeparment(selectedDepartment.value.id);
      subjectOffering.value = res.data;
    }
  } catch (error) {
    console.error('Failed to reload subject offerings:', error);
  }
};

const timeOptions = ref([
  '7:00-9:00 AM',
  '9:00-11:30 AM',
  '1:00-3:00 PM',
  '3:00-5:00 PM',
  '5:00-7:00 PM'
]);

const dayOptions = ref([
  'Monday',
  'Tuesday',
  'Wednesday',
  'Thursday',
  'Friday',
  'Saturday'
]);


const addSubjectOffer = async (subject) => {
  submitted.value = true;
  loading.value = true;

  offerForm.subject = subject;
  offerForm.department = selectedDepartment.value;

  if (!offerForm.subject?.id || !offerForm.department?.id) {
    toast.add({ severity: 'error', summary: 'Error', detail: 'Please fill in all required fields', life: 3000
    });
    loading.value = false;
    return;
  }

  try {
    const payload = {
      subject_id: offerForm.subject.id,
      department_id: offerForm.department.id
    };

    await SubjectOffering.create(payload);
    toast.add({
      severity: 'success', summary: 'Success', detail: 'Subject added successfully', life: 3000
    });

    const res = await SubjectOffering.getBydeparment(offerForm.department.id);
    subjectOffering.value = res.data;

    showAddSubjectDialog.value = false;

  } catch (error) {
    console.error('Failed to save subject:', error);
    toast.add({
      severity: 'error', summary: 'Error', detail: error.message || 'Failed to save subject', life: 3000
    });
  } finally {
    loading.value = false;
    offerForm.subject = null;
    offerForm.department = null;
  }
};

const addSchedule = async (instructor) => {
  if (!scheduleForm.day || !scheduleForm.time || !scheduleForm.section) {
    toast.add({ severity: 'error', summary: 'Missing Info', detail: 'Please complete the schedule details', life: 3000 });
    return;
  }

  try {
    const payload = {
      day: scheduleForm.day,
      time: scheduleForm.time,
      section: scheduleForm.section,
      instructor: scheduleForm.instructor || ''
    };

    await SubjectOffering.addSchedule(selectedSubject.value.id, payload);
    toast.add({ severity: 'success', summary: 'Instructor Added', life: 3000 });

    const res = await SubjectOffering.getBySubjectOffers(selectedSubject.value.id);
    subjectSchedules.value = res.data;

  } catch (error) {
    console.error(error);
    toast.add({ severity: 'error', summary: 'Failed', detail: 'Could not add schedule', life: 3000 });
  }
};

const addInstructor = async (scheduleID) => {
  if (!scheduleID) {
    toast.add({ severity: 'error', summary: 'Error', detail: 'Schedule ID is missing', life: 3000 });
    return;
  }

  const instructorName = newInstructor.value.name?.trim();

  if (!instructorName) {
    toast.add({ severity: 'error', summary: 'Error', detail: 'Instructor name is required', life: 3000 });
    return;
  }

  try {
    await Schedule.patch(scheduleID, { instructor: instructorName });

    toast.add({ severity: 'success', summary: 'Instructor Added', life: 3000 });

    const res = await SubjectOffering.getBySubjectOffers(selectedSubject.value.id);
    subjectSchedules.value = res.data;

  } catch (error) {
    console.error('Failed to add instructor:', error);
    toast.add({ severity: 'error', summary: 'Failed', detail: error.response?.data?.detail || 'Could not add instructor', life: 3000 });
  } finally {
    showAddInstructorDialog.value = false;
    newInstructor.value = { name: '', scheduleId: null };
  }
};

const deleteSchedule = async (scheduleID) => {
  if (!scheduleID) {
    toast.add({ severity: 'error', summary: 'Error', detail: 'Schedule ID is missing', life: 3000 });
    return;
  }

  try {
    await Schedule.delete(scheduleID);
    toast.add({ severity: 'success', summary: 'Deleted', detail: 'Schedule deleted successfully', life: 3000 });

    const res = await SubjectOffering.getBySubjectOffers(selectedSubject.value.id);
    subjectSchedules.value = res.data;

  } catch (error) {
    console.error('Failed to delete schedule:', error);
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: error.response?.data?.detail || 'Failed to delete schedule',
      life: 3000
    });
  }finally {
    deleteScheduleDialog.value = false;
  }
};

const confirmDeleteSchedule = (schedule) => {
  scheduleToDelete.value = schedule;
  deleteScheduleDialog.value = true;
}

const confirmDeleteOfferedSubject = (subject) => {
  subjectToDelete.value = subject;
  deleteOfferedSubjectDialog.value = true;
}

</script>



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