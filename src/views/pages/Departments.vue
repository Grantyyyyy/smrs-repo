<template>
  <div class="bg-white p-4 rounded-xl">
    <div class="flex items-center justify-between mb-4">
       <h2 class="text-2xl font-bold">Departments</h2>
       <div class="flex gap-2">
         <Button 
            label="Add Department" 
            icon="pi pi-plus" 
            @click="addDepartment" 
            class="p-button-success"
         />
       </div>  
    </div>
    
    <div class="flex flex-col bg-white rounded-lg shadow-sm m-6 w-[calc(100%-3rem)] h-[calc(100%-3rem)]">
      <DataTable 
        :value="departments" 
        :paginator="true" 
        :rows="10"
        :rowsPerPageOptions="[10,20]"
        paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
        currentPageReportTemplate="Showing {first} to {last} of {totalRecords} departments"
        responsiveLayout="scroll"
        :loading="loading"
        scrollable
        scrollHeight="flex"
      >
        <Column 
          field="name" 
          header="Name" 
          :sortable="true" 
          style="min-width: 150px"
        >
          <template #body="{ data }">
            {{ data.name }}
          </template>
        </Column>
      </DataTable>
    </div>
  </div>
</template>


<script setup>
import { Department } from '@/service/department';
import Column from 'primevue/column';
import DataTable from 'primevue/datatable';
import { useToast } from 'primevue/usetoast';
import { onMounted, ref } from 'vue';

const toast = useToast();
const loading = ref(false);
const departments = ref([]);

const success = {
    severity: 'success',
    summary: 'Success',
    detail: 'Operation completed successfully',
    life: 3000
}


onMounted(async () => {
  loading.value = true
  try {
    const res = await Department.getAll()
    departments.value = res.data
    console.log('Departments loaded:', departments.value)
  } catch (error) {
    console.error('Failed to load departments:', error)
  } finally {
    loading.value = false
  }
});


const addDepartment = async () => {
  try {
    const newDepartment = { 
        name: 'Test Department' // Replace with actual input from user
    }
    await Department.create(newDepartment);
    
    toast.add({
      severity: 'success',
      summary: 'Success',
      detail: 'Department added successfully',
      life: 3000
    });
    // Refresh the department list
    const res = await Department.getAll();
    departments.value = res.data;

  } catch (error) {
    console.error('Failed to add department:', error);
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'Failed to add department',
      life: 3000
    });
  } 
};

const deleteDepartment = async (departmentId) => {
  try {
    await Department.delete(departmentId);
    toast.add({
      severity: 'success',
      summary: 'Success',
      detail: 'Department deleted successfully',
      life: 3000
    });
    // Refresh the department list
    const res = await Department.getAll();
    departments.value = res.data;
  } catch (error) {
    console.error('Failed to delete department:', error);
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'Failed to delete department',
      life: 3000
    });
  }
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
</script>




