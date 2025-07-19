<template>
  <div>
    <div class="card">
      <!-- Error Display -->
      <div v-if="apiError" class="p-4 mb-4 bg-red-100 border-round">
        <div class="flex align-items-center">
          <i class="pi pi-exclamation-circle text-red-500 mr-2"></i>
          <span class="text-red-500">{{ apiError }}</span>
        </div>
      </div>

      <Toolbar class="mb-4">
        <template #start>
          <span class="text-4xl font-bold">Curriculums List</span>
        </template>
        <template #end>
          <IconField iconPosition="left">
            <InputIcon class="pi pi-search" />
            <InputText 
              v-model="searchQuery" 
              placeholder="Search..." 
              @input="filterCourses"
            />
          </IconField>
        </template>
      </Toolbar>

      <!-- Department Filter -->
      <div class="flex flex-col md:flex-row aling-items-center gap-4 mb-4">
        <label for="departmentFilter" class="mt-2 font-medium block mb-2">Filter by Department :</label>
        <div class="flex gap-2 align-items-center">
          <Dropdown 
            id="departmentFilter"
            v-model="selectedDepartment"
            :options="departmentOptions"
            optionLabel="label"
            optionValue="value"
            placeholder="All Departments"
            class="w-500 md:w-20rem"
            @change="onDepartmentChange"
          />
          <Button 
            v-if="selectedDepartment"
            icon="pi pi-times"
            severity="secondary"
            @click="resetDepartmentFilter"
            v-tooltip="'Clear department filter'"
          />
        </div>
      </div>

      <!-- Loading Indicator -->
      <!-- <div  class="flex justify-center p-4">
        <ProgressSpinner style="width: 50px; height: 50px" />
      </div> -->

      <!-- No Results -->
      <div  class="p-4 text-center">
        <p>No courses found matching your criteria.</p>
        <Button 
          v-if="selectedDepartment || searchQuery"
          label="Reset Filters"
          icon="pi pi-filter-slash"
          severity="secondary"
          class="mt-2"
          @click="resetDepartmentFilter"
        />
      </div>

      <!-- Courses List -->
      <div >
        <div v-for="course in filteredCourses" :key="course.id" class="mb-6 surface-card p-4 border-round">
          <div class="flex justify-between align-items-center mb-4">
            <div>
              <h4 class="m-0">{{ course.course_name }} ({{ course.course_code }})</h4>
              <span class="text-color-secondary text-sm">
                {{ course.department_code }} - {{ course.department_name }}
              </span>
            </div>
            <Button 
              label="Add Curriculum" 
              icon="pi pi-plus" 
              @click="openNewCurriculum(course)" 
            />
          </div>

          <DataTable 
            :value="course.curriculums" 
            :paginator="true" 
            :rows="5"
            :rowsPerPageOptions="[5,10,25]"
            stripedRows
            class="p-datatable-sm"
          >
            <Column field="year_started" header="Year" sortable>
              <template #body="{ data }">
                {{ data.year_started }}
              </template>
            </Column>
            <Column field="is_active" header="Status" sortable>
              <template #body="{ data }">
                <Tag 
                  :value="data.is_active ? 'Active' : 'Inactive'" 
                  :severity="data.is_active ? 'success' : 'danger'" 
                />
              </template>
            </Column>
            <Column header="Actions" style="min-width: 180px">
              <template #body="slotProps">
                <div class="flex gap-2">
                  <Button 
                    icon="pi pi-eye" 
                    severity="help"
                    outlined
                    rounded
                    @click="viewProspectus(course, slotProps.data)"
                    v-tooltip="'View Prospectus'"
                  />
                  <Button 
                    icon="pi pi-pencil" 
                    severity="info"
                    outlined
                    rounded
                    @click="editCurriculum(course, slotProps.data)" 
                    v-tooltip="'Edit'"
                  />
                  <Button 
                    icon="pi pi-trash" 
                    severity="danger" 
                    outlined
                    rounded
                    @click="confirmDeleteCurriculum(course, slotProps.data)" 
                    v-tooltip="'Delete'"
                  />
                </div>
              </template>
            </Column>
          </DataTable>
        </div>
      </div>
    </div>

    <!-- Curriculum Dialog -->
    <Dialog 
      v-model:visible="curriculumDialog" 
      :style="{ width: '350px' }" 
      :header="curriculum.curriculum_id ? 'Edit Curriculum' : 'Add Curriculum'" 
      :modal="true"
      :closable="!loading"
    >
      <div class="p-fluid">
        <div class="field mb-4">
          <label for="year_started" class="font-bold block mb-2">Year *</label>
          <Dropdown 
            id="year_started"
            v-model="curriculum.year_started"
            :options="yearOptions"
            placeholder="Select Year"
            :class="{ 'p-invalid': submitted && !curriculum.year_started }"
            class="w-full"
          />
          <small v-if="submitted && !curriculum.year_started" class="p-error">Year is required</small>
        </div>
        <div class="field">
          <label for="is_active" class="font-bold block mb-2">Status</label>
          <Dropdown 
            id="is_active" 
            v-model="curriculum.is_active" 
            :options="statusOptions" 
            optionLabel="label"
            optionValue="value"
            class="w-full"
          />
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
          @click="saveCurriculum" 
          :loading="loading" 
        />
      </template>
    </Dialog>

    <!-- Delete Confirmation Dialog -->
    <Dialog 
      v-model:visible="deleteCurriculumDialog" 
      :style="{ width: '450px' }" 
      header="Confirm Deletion" 
      :modal="true"
    >
      <div class="flex align-items-center gap-3">
        <i class="pi pi-exclamation-triangle text-3xl text-red-500" />
        <span>Are you sure you want to delete this curriculum?</span>
      </div>
      <template #footer>
        <Button 
          label="No" 
          icon="pi pi-times" 
          class="p-button-text" 
          @click="deleteCurriculumDialog = false" 
        />
        <Button 
          label="Yes" 
          icon="pi pi-check" 
          class="p-button-danger" 
          @click="deleteCurriculum" 
          :loading="loading" 
        />
      </template>
    </Dialog>
  </div>
</template>


<script setup>
import { Course, Department } from '@/service/academicService';
import { useToast } from 'primevue/usetoast';
import { computed, onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';

const toast = useToast();
const router = useRouter();
const coursesWithCurriculums = ref([]);
const filteredCourses = ref([]);
const loading = ref(false);
const apiError = ref(null);
const searchQuery = ref('');
const selectedDepartment = ref(null);

const departments = ref([]);
const courses = ref([]);

// Dialogs and form state
const curriculumDialog = ref(false);
const deleteCurriculumDialog = ref(false);
const submitted = ref(false);

// Selected items
const selectedCourse = ref(null);
const selectedCurriculum = ref(null);
const curriculum = ref({
  year_started: null,
  is_active: true,
  course: null
});

onMounted(async () => {
  loading.value = true;
  try {
    const [departmentsRes, courseRes] = await Promise.all([
      Department.getAll(),
      Course.getAll()
    ]);
    departments.value = departmentsRes.data;
    courses.value = courseRes.data;

    console.log('Departments loaded:', departments.value);
    console.log('Courses loaded:', courses.value);
  } catch (error) {
    console.error('Failed to load departments and subjects:', error);
  } finally {
    loading.value = false;
  }
});




// Status options for dropdown
const statusOptions = ref([
  { label: 'Active', value: true },
  { label: 'Inactive', value: false }
]);

// Load data on mount
// onMounted(async () => {
//   await loadData();
// });

// Main data loading function
// async function loadData() {
//   try {
//     loading.value = true;
//     apiError.value = null;
    
//     const [departmentsResponse, coursesResponse, curriculumsResponse] = await Promise.all([
//       DepartmentsService.getDepartments(),
//       coursesService.getCourses(),
//       curriculumService.getCurriculums()
//     ]);
    
//     departments.value = departmentsResponse;
    
//     coursesWithCurriculums.value = coursesResponse.map(course => {
//       const department = departments.value.find(d => d.id === course.department);
//       return {
//         ...course,
//         department_name: department?.department_name || 'N/A',
//         department_code: department?.department_code || '',
//         curriculums: curriculumsResponse.filter(c => c.course === course.id)
//       };
//     });
    
//     filterCourses(); // Apply initial filtering
    
//   } catch (error) {
//     handleApiError(error, 'Failed to load curriculum data');
//   } finally {
//     loading.value = false;
//   }
// }

function viewProspectus(course, curriculum) {
  router.push({
    name: 'prospectus',
    params: { 
      courseId: course.id,
      curriculumId: curriculum.curriculum_id 
    },
    query: { 
      courseName: course.course_name,
      curriculumYear: curriculum.year_started 
    }
  });
}

// Improved filtering function
function filterCourses() {
  const query = searchQuery.value.toLowerCase();
  
  // First filter by department if selected
  let results = selectedDepartment.value
    ? coursesWithCurriculums.value.filter(
        course => course.department === selectedDepartment.value.id
      )
    : [...coursesWithCurriculums.value];
  
  // Then filter by search query if provided
  if (query) {
    results = results.filter(course => 
      course.course_name.toLowerCase().includes(query) || 
      course.course_code.toLowerCase().includes(query) ||
      (course.department_name && course.department_name.toLowerCase().includes(query)) ||
      (course.department_code && course.department_code.toLowerCase().includes(query))
    );
  }
  
  filteredCourses.value = results;
}

function onDepartmentChange() {
  searchQuery.value = ''; // Reset search when department changes
  filterCourses();
}

function resetDepartmentFilter() {
  selectedDepartment.value = null;
  searchQuery.value = '';
  filterCourses();
}

function handleApiError(error, defaultMessage) {
  console.error(error);
  
  let errorMessage = defaultMessage;
  if (error.response?.data) {
    if (typeof error.response.data === 'object') {
      errorMessage = Object.entries(error.response.data)
        .map(([field, errors]) => `${field}: ${Array.isArray(errors) ? errors.join(', ') : errors}`)
        .join('; ');
    } else {
      errorMessage = error.response.data.detail || JSON.stringify(error.response.data);
    }
  }
  
  apiError.value = errorMessage;
  toast.add({
    severity: 'error',
    summary: 'Error',
    detail: errorMessage,
    life: 5000
  });
}

function openNewCurriculum(course) {
  selectedCourse.value = course;
  curriculum.value = {
    year_started: new Date().getFullYear(),
    is_active: true,
    course: course.id
  };
  submitted.value = false;
  curriculumDialog.value = true;
}

function editCurriculum(course, curriculumToEdit) {
  selectedCourse.value = course;
  selectedCurriculum.value = curriculumToEdit;
  curriculum.value = { ...curriculumToEdit };
  curriculumDialog.value = true;
}

// async function saveCurriculum() {
//   submitted.value = true;

//   if (!curriculum.value.year_started) {
//     return;
//   }

//   try {
//     loading.value = true;
    
//     const curriculumData = {
//       year_started: curriculum.value.year_started,
//       is_active: curriculum.value.is_active,
//       course: curriculum.value.course
//     };
    
//     if (curriculum.value.curriculum_id) {
//       await curriculumService.updateCurriculum(
//         curriculum.value.curriculum_id, 
//         curriculumData
//       );
//       toast.add({
//         severity: 'success',
//         summary: 'Updated',
//         detail: 'Curriculum updated successfully',
//         life: 3000
//       });
//     } else {
//       await curriculumService.createCurriculum(curriculumData);
//       toast.add({
//         severity: 'success',
//         summary: 'Created',
//         detail: 'Curriculum created successfully',
//         life: 3000
//       });
//     }

//     await loadData();
//     curriculumDialog.value = false;
//     curriculum.value = {};
//   } catch (error) {
//     handleApiError(error, 'Failed to save curriculum');
//   } finally {
//     loading.value = false;
//   }
// }

async function confirmDeleteCurriculum(course, curriculumToDelete) {
  selectedCourse.value = course;
  selectedCurriculum.value = curriculumToDelete;
  deleteCurriculumDialog.value = true;
}

// async function deleteCurriculum() {
//   try {
//     loading.value = true;
//     await curriculumService.deleteCurriculum(selectedCurriculum.value.curriculum_id);
//     toast.add({
//       severity: 'success',
//       summary: 'Deleted',
//       detail: 'Curriculum deleted successfully',
//       life: 3000
//     });
//     await loadData();
//   } catch (error) {
//     handleApiError(error, 'Failed to delete curriculum');
//   } finally {
//     deleteCurriculumDialog.value = false;
//     loading.value = false;
//   }
// }

function hideDialog() {
  curriculumDialog.value = false;
  submitted.value = false;
}

const departmentOptions = computed(() => {
  return departments.value.map(d => ({
    label: `${d.department_code} - ${d.department_name}`,
    value: d
  }));
});

const yearOptions = computed(() => {
  const currentYear = new Date().getFullYear();
  return Array.from({ length: 10 }, (_, i) => currentYear - i);
});
</script>



<style scoped>
.p-error {
  color: #ef4444;
  font-size: 0.875rem;
}

/* Responsive adjustments */
@media screen and (max-width: 960px) {
  .toolbar {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .toolbar #end {
    width: 100%;
  }
  
  .p-input-icon-left {
    width: 100%;
  }
}

.surface-card {
  background: var(--surface-card);
  border: 1px solid var(--surface-border);
  transition: box-shadow 0.2s;
}

.surface-card:hover {
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.flex.gap-2 {
  gap: 0.5rem;
}
</style>