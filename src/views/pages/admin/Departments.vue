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
            @click="confirmDeleteSelectedDepartments" 
            :disabled="!selectedDepartments?.length" 
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
        v-model:selection="selectedDepartments"
        :value="departments"
        :loading="loading"
        dataKey="id"
        :paginator="true"
        :rows="10"
        :filters="filters"
        paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
        :rowsPerPageOptions="[5,10,25]"
        currentPageReportTemplate="Showing {first} to {last} of {totalRecords} departments"
        stripedRows
      >
        <template #header>
          <div class="flex flex-wrap gap-2 items-center justify-between">
            <h4 class="m-0">Department List</h4>
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
            Loading departments...
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
              No departments found
            </template>
          </div>
        </template>

        <Column selectionMode="multiple" headerStyle="width: 3rem" :exportable="false"></Column>
        <Column field="code" header="Code" sortable></Column>
        <Column field="name" header="Name" sortable></Column>
        <Column :exportable="false" header="Actions" style="min-width: 150px">
          <template #body="slotProps">
            <Button 
              icon="pi pi-pencil" 
              class="p-button-rounded p-button-text p-button-primary mr-2" 
              @click="editDepartment(slotProps.data)" 
            />
            <Button 
              icon="pi pi-trash" 
              class="p-button-rounded p-button-text p-button-danger" 
              @click="confirmDeleteDepartment(slotProps.data)" 
            />
          </template>
        </Column>
      </DataTable>
    </div>

    <Dialog 
      v-model:visible="departmentDialog" 
      :style="{ width: '450px' }" 
      :header="departments.value ? 'Edit Department' : 'Add Department'" 
      :modal="true"
      :closable="!loading"
    >
      <div class="p-fluid">
        <div class="field mb-4">
          <label for="departmentCode" class="font-bold block mb-2">Department Code</label>
          <InputText 
            id="departmentCode" 
            v-model.trim="departmentForm.code" 
            required
            :class="{ 'p-invalid': submitted && !departmentForm.code }"
            class="w-full"
          />
          <small v-if="submitted && !departmentForm.code" class="text-red-500 text-sm">Code is required</small>
        </div>
        <div class="field mb-4">
          <label for="departmentName" class="font-bold block mb-2">Department Name</label>
          <InputText 
            id="departmentName" 
            v-model.trim="departmentForm.name" 
            required
            :class="{ 'p-invalid': submitted && !departmentForm.name }"
            class="w-full"
          />
          <small v-if="submitted && !departmentForm.name" class="text-red-500 text-sm">Name is required</small>
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
          @click="saveDepartment" 
          :loading="loading" 
        />
      </template>
    </Dialog>

    <!-- delete one department  -->
    <Dialog 
      v-model:visible="deleteDepartmentDialog" 
      :style="{ width: '450px' }" 
      header="Confirm" 
      :modal="true"
      :closable="!loading"
    >
      <div class="flex items-center gap-4">
        <i class="pi pi-exclamation-triangle text-red-500 text-2xl" />
        <span v-if="departmentToDelete">Are you sure you want to delete <b>{{ departmentToDelete.name }}</b>?
        </span>
      </div>
      <template #footer>
        <Button 
          label="No" 
          icon="pi pi-times" 
          class="p-button-text" 
          @click="deleteDepartmentDialog = false" 
          :disabled="loading" 
        />
        <Button 
          label="Yes" 
          icon="pi pi-check" 
          class="p-button-danger" 
          @click="deleteDepartment" 
          :loading="loading" 
        />
      </template>
    </Dialog>

    <Dialog 
      v-model:visible="deleteDepartmentsDialog" 
      :style="{ width: '450px' }" 
      header="Confirm" 
      :modal="true"
      :closable="!loading"
    >
      <div class="flex items-center gap-4">
        <i class="pi pi-exclamation-triangle text-red-500 text-2xl" />
        <span>Are you sure you want to delete the selected departments?</span>
      </div>
      <template #footer>
        <Button 
          label="No" 
          icon="pi pi-times" 
          class="p-button-text" 
          @click="deleteDepartmentsDialog = false" 
          :disabled="loading" 
        />
        <Button 
          label="Yes" 
          icon="pi pi-check" 
          class="p-button-danger" 
          @click="deletedSelectedDepartments" 
          :loading="loading" 
        />
      </template>
    </Dialog>
  </div>
</template>


<script setup>
// import DepartmentsService from '@/service/DepartmentsService';
import { Department } from '@/service/academicService';
import { FilterMatchMode } from '@primevue/core/api';
import { useToast } from 'primevue/usetoast';
import { onMounted, reactive, ref } from 'vue';

const toast = useToast();
const dt = ref();
const departments = ref([]);
const loading = ref(true);
const apiError = ref(null);
const departmentDialog = ref(false);
const deleteDepartmentDialog = ref(false);
const deleteDepartmentsDialog = ref(false);


const filters = ref({
    global: { value: null, matchMode: FilterMatchMode.CONTAINS }
});
const submitted = ref(false);
const departmentForm = reactive({
    code: '',
    name: ''
})

const selectedDepartments = ref([]);
const departmentToDelete = ref(null);



onMounted(async() => {
    loading.value = true;
    try {
        const res = await Department.getAll();
        departments.value = res.data;
        console.log('Departments loaded:', departments.value);
        
    } catch (error) {
        console.error('Failed to load departments:', error);
    } finally {
        loading.value = false;
    }
})

const saveDepartment = async () => {
  submitted.value = true;
  loading.value = true;

  if (!departmentForm.code || 
    !departmentForm.name) {

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
      ...departmentForm,
    };


    if (departmentForm.id) {
      await Department.update(departmentForm.id, payload);
      toast.add({
        severity: 'success', summary: 'Success', detail: 'Department updated successfully', life: 3000
      });
    } else {
      await Department.create(payload);
      toast.add({
        severity: 'success', summary: 'Success', detail: 'Department added successfully', life: 3000
      });
    }

    const res = await Department.getAll();
    departments.value = res.data;
    resetForm();
    departmentDialog.value = false;

  } catch (error) {
    console.error('Failed to save department:', error);
    toast.add({
      severity: 'error', summary: 'Error', detail: error.message || 'Failed to save department', life: 3000
    });
  } finally {
    loading.value = false;
  }
};

const deleteDepartment = async () => {
  if (!departmentToDelete.value || !departmentToDelete.value.id) return;
    loading.value = true;

    try {
      await Department.delete(departmentToDelete.value.id);

      toast.add({
        severity: 'success', summary: 'Success', detail: 'Department deleted successfully', life: 3000
      });

      const res = await Department.getAll();
      departments.value = res.data;
      deleteDepartmentDialog.value = false;
      departmentToDelete.value = null;
    } catch (error) {
      toast.add({
        severity: 'error', summary: 'Error', detail: error.message || 'Failed to delete department', life: 3000
      })
    } finally {
      loading.value = false;
  }
}

const deletedSelectedDepartments = async () => {
  if (!selectedDepartments.value.length) return;

  loading.value = true;
  try{
    await Promise.all(
      selectedDepartments.value.map(sub => Department.delete(sub.id))
    );

    toast.add({
      severity: 'success', summary: 'Success', detail: 'Departments deleted successfully', life: 3000
    });

    const res = await Department.getAll();
    departments.value = res.data;
    deleteDepartmentsDialog.value = false;
    selectedDepartments.value = [];
  }catch (error) {
    toast.add({
      severity: 'error', summary: 'Error', detail: error.message || 'Failed to delete departments', life: 3000
    })
  }finally {
    loading.value = false;
  }
}

function resetForm() {
    departmentForm.code = '';
    departmentForm.name = '';
    submitted.value = false;
}

function openNew() {
    departmentForm.value = {
        id: null,
        code: '',
        name: ''
    };
    submitted.value = false;
    departmentDialog.value = true;
}

function hideDialog() {
    departmentDialog.value = false;
    submitted.value = false;
}

function editDepartment(dept) {
    departmentForm.id = dept.id;
    departmentForm.code = dept.code;
    departmentForm.name = dept.name;

    submitted.value = false;
    departmentDialog.value = true;
}

function confirmDeleteDepartment(dept) {
    departmentToDelete.value = dept;
    deleteDepartmentDialog.value = true;
}

function confirmDeleteSelectedDepartments() {
    deleteDepartmentsDialog.value = true;
}

// async function deleteDepartment() {
//     try {
//         await DepartmentsService.deleteDepartment(department.value.id);
//         departments.value = departments.value.filter((val) => val.id !== department.value.id);
//         deleteDepartmentDialog.value = false;
//         department.value = {};
//         toast.add({ severity: 'success', summary: 'Successful', detail: 'Department Deleted Successfully', life: 3000, group: 'department' });
//     } catch (error) {
//         toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to delete department', life: 3000 });
//     }
// }

function exportCSV() {
    dt.value.exportCSV();
}

// function confirmDeleteSelected() {
//     deleteDepartmentsDialog.value = true;
// }

// async function deleteSelectedDepartments() {
//     try {
//         const deletePromises = selectedDepartments.value.map(dept => 
//             DepartmentsService.deleteDepartment(dept.id)
//         );
//         await Promise.all(deletePromises);
//         departments.value = departments.value.filter((val) => !selectedDepartments.value.includes(val));
//         deleteDepartmentsDialog.value = false;
//         selectedDepartments.value = [];
//         toast.add({ severity: 'success', summary: 'Successful', detail: 'Departments Deleted Successfully', life: 3000, group: 'Department' });
//     } catch (error) {
//         toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to delete departments', life: 3000 });
//     }
// }
// </script>



<style scoped>
.p-error {
    color: #ef4444;
    font-size: 0.875rem;
}
</style>