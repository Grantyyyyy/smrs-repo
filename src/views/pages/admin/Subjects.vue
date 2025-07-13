<template>
  <div>
    <div class="card">
      <div v-if="apiError" class="p-4 mb-4 bg-red-100 border-round flex items-center">
        <i class="pi pi-exclamation-circle text-red-500 mr-2"></i>
        <span class="text-red-500">{{ apiError }}</span>
      </div>

      <Toolbar class="mb-4">
        <template #start>
          <Button 
            label="New" 
            icon="pi pi-plus" 
            class="p-button-success mr-2" 
            @click="openNew" 
          />
          <Button 
            label="Delete" 
            icon="pi pi-trash" 
            class="p-button-danger" 
            @click="confirmDeleteSelectedSubjects" 
            :disabled="!selectedSubjects?.length" 
          />
        </template>
        <template #end>
          <Button 
            label="Export" 
            icon="pi pi-upload" 
            class="p-button-help ml-2" 
            @click="exportCSV" 
          />
        </template>
      </Toolbar>

      <DataTable
        ref="dt"
        v-model:selection="selectedSubjects"
        :value="subjects"
        :loading="loading"
        dataKey="id"
        :paginator="true"
        :rows="10"
        :filters="filters"
        paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
        :rowsPerPageOptions="[5,10,25]"
        currentPageReportTemplate="Showing {first} to {last} of {totalRecords} subjects"
        stripedRows
      >
        <template #header>
          <div class="flex flex-wrap gap-2 items-center justify-between">
            <h4 class="m-0">Subjects List</h4>
            <IconField>
              <InputIcon>
                <i class="pi pi-search" />
              </InputIcon>
              <InputText 
                v-model="filters['global'].value" 
                placeholder="Search..." 
              />
            </IconField>
          </div>
        </template>

        <template #loading>
          <div class="flex items-center justify-center p-4">
            <i class="pi pi-spinner pi-spin mr-2"></i>
            Loading subjects...
          </div>
        </template>

        <template #empty>
          <div class="text-center p-4">
            <template v-if="apiError">
              <i class="pi pi-exclamation-triangle mr-2"></i>
              <span class="text-red-500">{{ apiError }}</span>
            </template>
            <template v-else>
              <i class="pi pi-database mr-2"></i>
              No subjects found
            </template>
          </div>
        </template>

        <Column selectionMode="multiple" headerStyle="width: 3rem" :exportable="false"></Column>
        <Column field="code" header="Code" sortable></Column>
        <Column field="name" header="Name" sortable></Column>
        <Column field="units" header="Units" sortable >
          <template #body="{ data }">
            <Tag :value="data.units" />
          </template>
        </Column>
        <Column field="department_name" header="Department" sortable>
          <template #body="{ data }">
            <Tag 
              :value="data.department_name" 
              :severity="data.department ? 'success' : 'warning'" 
            />
          </template>
        </Column>
        <Column field="created_at" header="Date Created" sortable>
          <template #body="{ data }">
            {{ formatDate(data.created_at) }}
          </template>
        </Column>
        <Column :exportable="false" header="Actions" style="min-width: 150px">
          <template #body="slotProps">
            <Button 
              icon="pi pi-pencil" 
              class="p-button-rounded p-button-text p-button-primary mr-2" 
              @click="editSubject(slotProps.data)" 
            />
            <Button 
              icon="pi pi-trash" 
              class="p-button-rounded p-button-text p-button-danger" 
              @click="confirmDeleteSubject(slotProps.data)" 
            />
          </template>
        </Column>
      </DataTable>
    </div>

    <Dialog 
      v-model:visible="subjectDialog" 
      :style="{ width: '450px' }" 
      :header="subjects.value ? 'Edit Subject' : 'Add Subject'" 
      :modal="true"
      :closable="!loading"
    >
      <div class="p-fluid">
        <div class="field mb-4">
          <label for="department" class="font-bold block mb-2">Department</label>
          <Dropdown 
            id="department"
            v-model="subjectForm.department"
            :options="departments"
            optionLabel="name"
            placeholder="Select Department"
            :class="{ 'p-invalid': submitted && !subjectForm.department }"
            class="w-full"
          />
          <small v-if="submitted && !subjectForm.department" class="p-error">Department is required</small>
        </div>
        <div class="field mb-4">
          <label for="subjectCode" class="font-bold block mb-2">Subject Code</label>
          <InputText 
            id="subjectCode" 
            v-model.trim="subjectForm.code" 
            required
            :class="{ 'p-invalid': submitted && !subjectForm.code }"
            class="w-full"
          />
          <small v-if="submitted && !subjectForm.code" class="p-error">Code is required</small>
        </div>
        <div class="field mb-4">
          <label for="subjectName" class="font-bold block mb-2">Subject Name</label>
          <InputText 
            id="subjectName" 
            v-model.trim="subjectForm.name" 
            required
            :class="{ 'p-invalid': submitted && !subjectForm.name }"
            class="w-full"
          />
          <small v-if="submitted && !subjectForm.name" class="p-error">Name is required</small>
        </div>
        <div class="field">
          <label for="units" class="font-bold block mb-2">Units</label>
          <InputNumber 
            id="units" 
            v-model="subjectForm.units" 
            required
            :class="{ 'p-invalid': submitted && !subjectForm.units }"
            class="w-full"
          />
          <small v-if="submitted && !subjectForm.units" class="p-error">Units are required</small>
        </div>
      </div>

      <template #footer>
        <Button 
          label="Cancel" 
          icon="pi pi-times" 
          class="p-button-text" 
          @click="hideDialog" 
          :disabled="loading" 
        />
        <Button 
          label="Save" 
          icon="pi pi-check" 
          @click="saveSubject" 
          :loading="loading" 
        />
      </template>
    </Dialog>

    <Dialog 
      v-model:visible="deleteSubjectDialog" 
      :style="{ width: '450px' }" 
      header="Confirm" 
      :modal="true"
      :closable="!loading"
    >
      <div class="flex items-center gap-4">
        <i class="pi pi-exclamation-triangle text-red-500 text-2xl" />
        <span v-if="subjectToDelete">Are you sure you want to delete <b>{{ subjectToDelete.name }} ?
        </b>?</span>
      </div>
      <template #footer>
        <Button 
          label="No" 
          icon="pi pi-times" 
          class="p-button-text" 
          @click="deleteSubjectDialog = false" 
          :disabled="loading" 
        />
        <Button 
          label="Yes" 
          icon="pi pi-check" 
          class="p-button-danger" 
          @click="deleteSubject" 
          :loading="loading" 
        />
      </template>
    </Dialog>

    <Dialog 
      v-model:visible="deleteSubjectsDialog" 
      :style="{ width: '450px' }" 
      header="Confirm" 
      :modal="true"
      :closable="!loading"
    >
      <div class="flex items-center gap-4">
        <i class="pi pi-exclamation-triangle text-red-500 text-2xl" />
        <span>Are you sure you want to delete the selected subjects?</span>
      </div>
      <template #footer>
        <Button 
          label="No" 
          icon="pi pi-times" 
          class="p-button-text" 
          @click="deleteSubjectsDialog = false" 
          :disabled="loading" 
        />
        <Button 
          label="Yes" 
          icon="pi pi-check" 
          class="p-button-danger" 
          @click="deletedSelectedSubjects" 
          :loading="loading" 
        />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { Department, Subject } from '@/service/academicService';
import { FilterMatchMode } from '@primevue/core/api';
import { useToast } from 'primevue/usetoast';
import { onMounted, reactive, ref } from 'vue';

const toast = useToast();
const dt = ref();
const subjects = ref([]);
const departments = ref([]);
const loading = ref(true);
const apiError = ref(null);
const subjectDialog = ref(false);
const deleteSubjectDialog = ref(false);
const deleteSubjectsDialog = ref(false);
const subjectForm = reactive({
  code: '',
  name: '',
  units: 0,
  department: null,
});

const selectedSubjects = ref([]);
const subjectToDelete = ref(null);


const filters = ref({
  global: { value: null, matchMode: FilterMatchMode.CONTAINS }
});
const submitted = ref(false);

onMounted(async () => {
  loading.value = true;
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
    loading.value = false;
  }
});


const saveSubject = async () => {
  submitted.value = true;
  loading.value = true;

  if (!subjectForm.code || 
    !subjectForm.name || 
    !subjectForm.units || 
    !subjectForm.department || !subjectForm.department.id
  ) {

    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'Please fill in all required fields',
      life: 3000
    });

    loading.value = false;
    return;
  }
  try {
    const payload = {
      ...subjectForm,
      department: subjectForm.department.id || subjectForm.department
    };


    if (subjectForm.id) {
      await Subject.update(subjectForm.id, payload);
      toast.add({
        severity: 'success', summary: 'Success', detail: 'Subject updated successfully', life: 3000
      });
    } else {
      await Subject.create(payload);
      toast.add({
        severity: 'success', summary: 'Success', detail: 'Subject added successfully', life: 3000
      });
    }

    const res = await Subject.getAll();
    subjects.value = res.data;
    resetForm();
    subjectDialog.value = false;

  } catch (error) {
    console.error('Failed to save subject:', error);
    toast.add({
      severity: 'error', summary: 'Error', detail: error.message || 'Failed to save subject', life: 3000
    });
  } finally {
    loading.value = false;
  }
};

const deleteSubject = async () => {
  if (!subjectToDelete.value || !subjectToDelete.value.id) return;
    loading.value = true;

    try {
      await Subject.delete(subjectToDelete.value.id);

      toast.add({
        severity: 'success', summary: 'Success', detail: 'Subject deleted successfully', life: 3000
      });

      const res = await Subject.getAll();
      subjects.value = res.data;
      deleteSubjectDialog.value = false;
      subjectToDelete.value = null;
    } catch (error) {
      toast.add({
        severity: 'error', summary: 'Error', detail: error.message || 'Failed to delete subject', life: 3000
      })
    } finally {
      loading.value = false;
  }
}

const deletedSelectedSubjects = async () => {
  if (!selectedSubjects.value.length) return;

  loading.value = true;
  try{
    await Promise.all(
      selectedSubjects.value.map(sub => Subject.delete(sub.id))
    );

    toast.add({
      severity: 'success', summary: 'Success', detail: 'Subjects deleted successfully', life: 3000
    });

    const res = await Subject.getAll();
    subjects.value = res.data;
    deleteSubjectsDialog.value = false;
    selectedSubjects.value = [];
  }catch (error) {
    toast.add({
      severity: 'error', summary: 'Error', detail: error.message || 'Failed to delete subjects', life: 3000
    })
  }finally {
    loading.value = false;
  }
}


const formatDate = (dateString) => {
  const options = { year: 'numeric', month: 'short', day: 'numeric' };
  return new Date(dateString).toLocaleDateString(undefined, options);
};

function openNew() {
  subjectForm.value = {
    id: null,
    department: null,
    code: '',
    name: '',
    units: 0
  };
  submitted.value = false;
  subjectDialog.value = true;
}

function editSubject(sub) {
  subjectForm.id = sub.id;
  subjectForm.code = sub.code;
  subjectForm.name = sub.name;
  subjectForm.units = sub.units;

  subjectForm.department =
    departments.value.find(d => d.id === sub.department || d.id === sub.department?.id) || null;

  submitted.value = false;
  subjectDialog.value = true;

}

function confirmDeleteSubject(sub) {
  subjectToDelete.value = sub;
  deleteSubjectDialog.value = true;

}

function confirmDeleteSelectedSubjects() {
  deleteSubjectsDialog.value = true;
}

function resetForm() {
  subjectForm.code = '';
  subjectForm.name = '';
  subjectForm.units = 0;
  subjectForm.department = null;
}

function hideDialog() {
  subjectDialog.value = false;
  submitted.value = false;
}

function exportCSV() {
  dt.value.exportCSV();
}
</script>
