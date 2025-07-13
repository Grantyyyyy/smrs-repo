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
            @click="confirmDeleteSelectedCourses" 
            :disabled="!selectedCourses?.length" 
          />
        </template>
        <template #end>
          <!-- <Button 
            label="Refresh" 
            icon="pi pi-refresh" 
            class="p-button-secondary" 
            @click="loadCourses" 
          /> -->
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
        v-model:selection="selectedCourses"
        :value="courses"
        :loading="loading"
        dataKey="id"
        :paginator="true"
        :rows="10"
        :filters="filters"
        paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
        :rowsPerPageOptions="[5,10,25]"
        currentPageReportTemplate="Showing {first} to {last} of {totalRecords} courses"
        stripedRows
      >
        <template #header>
          <div class="flex flex-wrap gap-2 items-center justify-between">
            <h4 class="m-0">Courses List</h4>
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
          <div class="flex align-items-center justify-content-center p-4">
            <i class="pi pi-spinner pi-spin mr-2"></i>
            Loading courses...
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
              No courses found
            </template>
          </div>
        </template>

        <!--table columns goes here-->

        <Column selectionMode="multiple" headerStyle="width: 3rem" :exportable="false"></Column>
        <Column field="code" header="Code" sortable></Column>
        <Column field="name" header="Name" sortable></Column>
        <Column field="department_name" header="Department" sortable>
          <template #body="{ data }">
            <Tag 
              :value="data.department_name" 
              :severity="data.department ? 'success' : 'warning'" 
            />
          </template>
        </Column>
        <Column :exportable="false" header="Actions" style="min-width: 150px">
          <template #body="slotProps">
            <Button 
              icon="pi pi-pencil" 
              class="p-button-rounded p-button-text p-button-primary mr-2" 
              @click="editCourse(slotProps.data)" 
            />
            <Button 
              icon="pi pi-trash" 
              class="p-button-rounded p-button-text p-button-danger" 
              @click="confirmDeleteCourse(slotProps.data)" 
            />
          </template>
        </Column>
      </DataTable>
    </div>

    <!-- Course Dialog -->
    <Dialog 
      v-model:visible="courseDialog" 
      :style="{ width: '450px' }" 
      :header="courses.id ? 'Edit Course' : 'Add Course'" 
      :modal="true"
      :closable="!loading"
    >
      <div class="p-fluid">
        <div class="field mb-4">
          <label for="department" class="font-bold block mb-2">Department</label>
          <Dropdown 
            id="department"
            v-model="courseForm.department"
            :options="departments"
            optionLabel="name"
            placeholder="Select Department"
            :class="{ 'p-invalid': submitted && !courseForm.department }"
            class="w-full"
          />
          <small v-if="submitted && !courseForm.department" class="p-error">Department is required</small>
        </div>
        <div class="field mb-4">
          <label for="courseCode" class="font-bold block mb-2">Course Code</label>
          <InputText 
            id="courseCode" 
            v-model.trim="courseForm.code" 
            required
            :class="{ 'p-invalid': submitted && !courseForm.code }"
            class="w-full"
          />
          <small v-if="submitted && !courseForm.code" class="p-error">Code is required</small>
        </div>
        <div class="field">
          <label for="courseName" class="font-bold block mb-2">Course Name</label>
          <InputText 
            id="courseName" 
            v-model.trim="courseForm.name" 
            required
            :class="{ 'p-invalid': submitted && !courseForm.name }"
            class="w-full"
          />
          <small v-if="submitted && !courseForm.name" class="p-error">Name is required</small>
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
          @click="saveCourse" 
          :loading="loading" 
        />
      </template>
    </Dialog>

    <!-- Delete Dialogs -->
    <Dialog 
      v-model:visible="deleteCourseDialog" 
      :style="{ width: '450px' }" 
      header="Confirm" 
      :modal="true"
      :closable="!loading"
    >
      <div class="flex items-center gap-4">
        <i class="pi pi-exclamation-triangle text-red-500 text-2xl" />
        <span v-if="courseToDelete">Are you sure you want to delete <b>{{ courseToDelete.name }}</b>?</span>
      </div>
      <template #footer>
        <Button 
          label="No" 
          icon="pi pi-times" 
          class="p-button-text" 
          @click="deleteCourseDialog = false" 
          :disabled="loading" 
        />
        <Button 
          label="Yes" 
          icon="pi pi-check" 
          class="p-button-danger" 
          @click="deleteCourse" 
          :loading="loading" 
        />
      </template>
    </Dialog>

    <Dialog 
      v-model:visible="deleteCoursesDialog" 
      :style="{ width: '450px' }" 
      header="Confirm" 
      :modal="true"
      :closable="!loading"
    >
      <div class="flex items-center gap-4">
        <i class="pi pi-exclamation-triangle text-red-500 text-2xl" />
        <span>Are you sure you want to delete the selected courses?</span>
      </div>
      <template #footer>
        <Button 
          label="No" 
          icon="pi pi-times" 
          class="p-button-text" 
          @click="deleteCoursesDialog = false" 
          :disabled="loading" 
        />
        <Button 
          label="Yes" 
          icon="pi pi-check" 
          class="p-button-danger" 
          @click="deletedSelectedCourses" 
          :loading="loading" 
        />
      </template>
    </Dialog>
  </div>
</template>


<script setup>
import { Course, Department } from '@/service/academicService';
import { FilterMatchMode } from '@primevue/core/api';
import { useToast } from 'primevue/usetoast';
import { onMounted, reactive, ref } from 'vue';

const toast = useToast();
const dt = ref();
const courses = ref([]);
const departments = ref([]);
const loading = ref(true);
const apiError = ref(null);
const courseDialog = ref(false);
const deleteCourseDialog = ref(false);
const deleteCoursesDialog = ref(false);
const filters = ref({
  global: { value: null, matchMode: FilterMatchMode.CONTAINS }
});
const submitted = ref(false);
const courseForm = reactive({
   code: '',
   name: '',
   department: null,
})

const selectedCourses = ref([]);
const courseToDelete = ref(null);



onMounted(async () => {
  loading.value = true;
  try {
    const [departmentsRes, courseRes] = await Promise.all([
      Department.getAll(),
      Course.getAll(),
    ]);
    departments.value = departmentsRes.data;
    courses.value = courseRes.data;
    console.log('Departments loaded:', departments.value);
    console.log('Courses loaded:', courses.value);
  } catch (error) {
    console.error('Failed to load departments and courses:', error);
  } finally {
    loading.value = false;
  }
});

const saveCourse = async () => {
  submitted.value = true;
  loading.value = true;

  if (!courseForm.code || 
    !courseForm.name || 
    !courseForm.department || !courseForm.department.id
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
      ...courseForm,
      department: courseForm.department.id || courseForm.department
    };


    if (courseForm.id) {
      await Course.update(courseForm.id, payload);
      toast.add({
        severity: 'success', summary: 'Success', detail: 'Course updated successfully', life: 3000
      });
    } else {
      await Course.create(payload);
      toast.add({
        severity: 'success', summary: 'Success', detail: 'Course added successfully', life: 3000
      });
    }

    const res = await Course.getAll();
    courses.value = res.data;
    resetForm();
    courseDialog.value = false;

  } catch (error) {
    console.error('Failed to save course:', error);
    toast.add({
      severity: 'error', summary: 'Error', detail: error.message || 'Failed to save course', life: 3000
    });
  } finally {
    loading.value = false;
  }
};

const deleteCourse = async () => {
  if (!courseToDelete.value || !courseToDelete.value.id) return;
    loading.value = true;

    try {
      await Course.delete(courseToDelete.value.id);

      toast.add({
        severity: 'success', summary: 'Success', detail: 'Course deleted successfully', life: 3000
      });

      const res = await Course.getAll();
      courses.value = res.data;
      deleteCourseDialog.value = false;
      courseToDelete.value = null;
    } catch (error) {
      toast.add({
        severity: 'error', summary: 'Error', detail: error.message || 'Failed to delete course', life: 3000
      })
    } finally {
      loading.value = false;
  }
}

const deletedSelectedCourses = async () => {
  if (!selectedCourses.value.length) return;

  loading.value = true;
  try{
    await Promise.all(
      selectedCourses.value.map(sub => Course.delete(sub.id))
    );

    toast.add({
      severity: 'success', summary: 'Success', detail: 'Courses deleted successfully', life: 3000
    });

    const res = await Course.getAll();
    courses.value = res.data;
    deleteCoursesDialog.value = false;
    selectedCourses.value = [];
  }catch (error) {
    toast.add({
      severity: 'error', summary: 'Error', detail: error.message || 'Failed to delete courses', life: 3000
    })
  }finally {
    loading.value = false;
  }
}

function resetForm() {
  courseForm.code = '';
  courseForm.name = '';
  courseForm.department = null;
}

function openNew() {
  courseForm.value = {
    id: null,
    code: '',
    name: '',
    department: null
  }
  submitted.value = false;
  courseDialog.value = true;
}

function editCourse(crs) {
  courseForm.id = crs.id;
  courseForm.code = crs.code;
  courseForm.name = crs.name;

  courseForm.department =
    departments.value.find(d => d.id === crs.department || d.id === crs.department?.id) || null;

  submitted.value = false;
  courseDialog.value = true;

}


function hideDialog() {
  courseDialog.value = false;
  submitted.value = false;
}

function confirmDeleteCourse(crs) {
  courseToDelete.value = crs;
  deleteCourseDialog.value = true;
}

function confirmDeleteSelectedCourses() {
  deleteCoursesDialog.value = true;
}

function exportCSV() {
  dt.value.exportCSV();
}



</script>



<style scoped>
.p-error {
  color: #ef4444;
  font-size: 0.875rem;
}
</style>