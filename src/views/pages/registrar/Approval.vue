<template>
  <div class="bg-gray-100 p-4 rounded-md shadow mb-4">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label class="block mb-1 font-medium text-gray-700">Student Name</label>
        <InputText type="text" :value="`${student.last_name}, ${student.first_name}`" class="w-full" readonly />
      </div>
      <div>
        <label class="block mb-1 font-medium text-gray-700">Student ID</label>
        <InputText type="text" :value="student.id" class="w-full" readonly />
      </div>
      <div>
        <label class="block mb-1 font-medium text-gray-700">Course</label>
        <InputText type="text" :value="student.course" class="w-full" readonly />
      </div>
      <div>
        <label class="block mb-1 font-medium text-gray-700">Year Level</label>
        <InputText type="text" :value="getYearLevelText(student.year_level)" class="w-full" readonly />
      </div>
    </div>
  </div>
  <form @submit.prevent="saveStatus">
    <div class="max-w-md mx-auto p-5 mt-4 bg-gray-100 rounded border border-gray-200 shadow">
    <div class="mb-4">
      <label class="block font-medium text-gray-700 mb-1">Status</label>
      <Dropdown 
        v-model="editedStatus" 
        :options="statusOptions" 
        optionLabel="label" 
        optionValue="value" 
        class="w-full" 
      />
    </div>
    <div class="mb-4">
      <label class="block font-medium text-gray-700 mb-1">Remarks</label>
      <Textarea
        v-model="remarks"
        :autoResize="true"
        rows="3"
        class="w-full"
        placeholder="Enter any remarks or notes about this clearance"
      />
    </div>
    <div class="flex flex-col sm:flex-row justify-center gap-6">
      <Button
        label="Cancel"
        icon="pi pi-times"
        class="p-button-secondary"
        @click="emit('close')"
      />
      <Button
        label="Save"
        icon="pi pi-check"
        class="p-button-success"
        type="submit"
      />
    </div>
    </div>
  </form>
  

  <div class="flex justify-between items-center mt-6">
    <div class="flex items-center gap-3 text-sm text-gray-600">
      <span>Status:</span>
      <span
        class="font-semibold px-3 py-1 rounded-full uppercase text-xs"
        :class="student.account_status === 'Approved' ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'"
      >
        {{ student.account_status }}
      </span>
    </div>
  </div>
</template>

<script setup>
import { Student } from '@/service/students';
import { Button, Dropdown, InputText, Textarea } from 'primevue';
import { useToast } from 'primevue/usetoast';
import { onMounted, ref } from 'vue';

const props = defineProps({
  student: {
    type: Object,
    required: true
  }
});

const remarks = ref('');
const editedStatus = ref('');
const toast = useToast();
const emit = defineEmits(['close']);


const statusOptions = [
  { label: 'Pending', value: 'pending' },
  { label: 'Approved', value: 'approved' }
];

const requirements = ref([
  {
    description: 'Canteen Fee',
    cleared: props.student?.clearanceStatus === 'Approved'
  }
]);


const saveStatus = async () => {
  try {
    const status = editedStatus.value === 'approved' ? 'Approved' : 'Pending';

    await Student.approve(props.student.id, {
      account_status: status,
      remarks: remarks.value
    });

    requirements.value[0].cleared = status === 'Approved';

    toast.add({
      severity: 'success',
      summary: 'Success',
      detail: `Status updated to ${status}`,
      life: 3000
    });

    emit('close');

  } catch (error) {
    console.error('Failed to update status:', error);
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'Failed to add department',
      life: 3000
    });
  }
  emit('close')
};

onMounted(() => {
  editedStatus.value = props.student.account_status?.toLowerCase() || 'pending';
});


const getYearLevelText = (yearLevel) => {
  const levels = ['1st Year', '2nd Year', '3rd Year', '4th Year'];
  return levels[yearLevel - 1] || `Year ${yearLevel}`;
};


</script>

<style scoped>
</style>
