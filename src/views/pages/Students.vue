<template>
  <div class="bg-white p-4 rounded-xl">
    <div class="flex items-center justify-between mb-4 mt-4">
       <h2 class="text-3xl font-bold ml-8 ">Registered Students</h2>
    </div>
    
    <div class="flex flex-col bg-white rounded-lg shadow-sm m-6 w-[calc(100%-3rem)] h-[calc(100%-3rem)]">
      <DataTable 
        :value="students" 
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
            {{ data.first_name }} {{ data.last_name }}
          </template>
        </Column>

        <Column 
          field="email" 
          header="Email" 
          :sortable="true" 
          style="min-width: 150px"
        >
          <template #body="{ data }">
            {{ data?.email }}
          </template>
        </Column>
        <Column 
          field="status" 
          header="Status" 
          :sortable="true" 
          style="min-width: 150px"
        >
          <template #body="{ data }">
            {{ data.account_status }}
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
      <Approval 
        v-if="selectedStudent" 
        :student="{
          id: selectedStudent.id,
          first_name: selectedStudent.first_name,
          last_name: selectedStudent.last_name,
          department: selectedStudent.department,
          course: selectedStudent.course,
          yearLevel: selectedStudent.yearLevel,
          account_status: selectedStudent.account_status,
        }"
        @close="closeDialog"
        @clearance-updated="handleStatusUpdated"
        @clearance-submitted="handleClearanceSubmitted"
        @close-dialog="closeDialog"
      />
    </Dialog>
  </div>
</template>


<script setup>

import { Student } from '@/service/students';
import Button from 'primevue/button';
import Column from 'primevue/column';
import DataTable from 'primevue/datatable';
import Dialog from 'primevue/dialog';
import { useToast } from 'primevue/usetoast';
import { onMounted, ref } from 'vue';
import Approval from './registrar/Approval.vue';

const toast = useToast();
const loading = ref(false);
const students = ref([]);
const selectedStudent = ref(null);
const displayDialog = ref(false);

const success = {
    severity: 'success',
    summary: 'Success',
    detail: 'Operation completed successfully',
    life: 3000
}


onMounted(async () => {
  loading.value = true
  try {
    const res = await Student.getAll()
    students.value = res.data
    console.log('Students loaded:', students.value)
  } catch (error) {
    console.error('Failed to load students:', error)
  } finally {
    loading.value = false
  }
});

const viewStudentDetails = (student) => {
    selectedStudent.value = student;
    displayDialog.value = true;
};



const handleStatusUpdated = () => {
  displayDialog.value = false;
};

const closeDialog = () => {
  displayDialog.value = false;
};


const addDepartment = async () => {
  try {
    const newDepartment = { 
        name: 'Test Department' // Replace with actual input from user
    }
    await Department.create(newDepartment);
    
    toast.add({
      severity: 'success',
      summary: 'Success',
      detail: 'Student added successfully',
      life: 3000
    });
    // Refresh the department list
    const res = await Department.getAll();
    departments.value = res.data;

  } catch (error) {
    console.error('Failed to add student:', error);
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'Failed to add student',
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




