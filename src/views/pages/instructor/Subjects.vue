<script setup>
import { ref, computed, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import Button from 'primevue/button'
import Card from 'primevue/card'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Dialog from 'primevue/dialog'
import InputText from 'primevue/inputtext'
import Tag from 'primevue/tag'
import Toast from 'primevue/toast'
import Dropdown from 'primevue/dropdown'
import ConfirmDialog from 'primevue/confirmdialog'
import { useConfirm } from 'primevue/useconfirm'

const FilterMatchMode = {
  STARTS_WITH: 'startsWith',
  CONTAINS: 'contains',
  NOT_CONTAINS: 'notContains',
  ENDS_WITH: 'endsWith',
  EQUALS: 'equals',
  NOT_EQUALS: 'notEquals',
  IN: 'in',
  LESS_THAN: 'lt',
  LESS_THAN_OR_EQUAL_TO: 'lte',
  GREATER_THAN: 'gt',
  GREATER_THAN_OR_EQUAL_TO: 'gte',
  BETWEEN: 'between',
  DATE_IS: 'dateIs',
  DATE_IS_NOT: 'dateIsNot',
  DATE_BEFORE: 'dateBefore',
  DATE_AFTER: 'dateAfter'
}

// Data
const subjects = ref([])
const selectedSubject = ref(null)
const toast = useToast()
const confirm = useConfirm()
const loading = ref(false)
const dialogVisible = computed({
  get: () => selectedSubject.value !== null,
  set: (value) => {
    if (!value) selectedSubject.value = null
  }
})

const gradeDialog = ref(false)
const selectedStudent = ref(null)
const gradeError = ref(false)
const isRegistrar = ref(false) // This would normally come from auth system
const isAdmin = ref(false) // This would normally come from auth system

const gradeOptions = [
  { label: '1.00', value: 1.00 },
  { label: '1.25', value: 1.25 },
  { label: '1.50', value: 1.50 },
  { label: '1.75', value: 1.75 },
  { label: '2.00', value: 2.00 },
  { label: '2.25', value: 2.25 },
  { label: '2.50', value: 2.50 },
  { label: '2.75', value: 2.75 },
  { label: '3.00', value: 3.00 },
  { label: '5.00 (Failed)', value: 5.00 },
  { label: 'Dropped', value: -1 }
]

const filters = ref({
  global: { value: null, matchMode: FilterMatchMode.CONTAINS },
  code: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
  name: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
  section: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
  year: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
  academicYear: { value: null, matchMode: FilterMatchMode.STARTS_WITH }
})

// Computed properties
const filteredSubjects = computed(() => {
  if (!filters.value.global.value) return subjects.value
  const searchTerm = filters.value.global.value.toLowerCase()
  return subjects.value.filter(subject => 
    subject.code.toLowerCase().includes(searchTerm) ||
    subject.name.toLowerCase().includes(searchTerm) ||
    subject.section.toLowerCase().includes(searchTerm) ||
    subject.year.toLowerCase().includes(searchTerm) ||
    subject.academicYear.toLowerCase().includes(searchTerm) ||
    subject.instructor.toLowerCase().includes(searchTerm))
})

// Check if subject grades are locked
const gradesLocked = computed(() => {
  return selectedSubject.value?.gradesLocked || false
})

// Methods
const viewStudents = (subject) => {
  selectedSubject.value = { ...subject }
}

const exportList = () => {
  try {
    // Create CSV content
    let csvContent = "Subject Code,Subject Name,Section,Year,Academic Year,Instructor,Schedule,Room,Student Count\n"
    subjects.value.forEach(subject => {
      csvContent += `${subject.code},${subject.name},${subject.section},${subject.year},${subject.academicYear},${subject.instructor},${subject.schedule},${subject.room},${subject.students.length}\n`
    })
    
    // Create download link
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', 'subjects_list.csv')
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    
    toast.add({
      severity: 'success',
      summary: 'Export Successful',
      detail: 'Subject list has been exported',
      life: 3000
    })
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Export Failed',
      detail: error.message,
      life: 3000
    })
  }
}

const loadSubjects = async () => {
  try {
    loading.value = true
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 500))
    
    // Simulate getting user role from auth system
    isRegistrar.value = false // Change to true to test registrar functions
    isAdmin.value = false // Change to true to test admin functions
    
    // Filipino names from Classes.vue
    const filipinoNames = [
      { lastName: "Dela Cruz", firstName: "Juan" },
      { lastName: "Reyes", firstName: "Maria" },
      { lastName: "Santos", firstName: "Jose" },
      { lastName: "Garcia", firstName: "Ana" },
      { lastName: "Bautista", firstName: "Antonio" },
      { lastName: "Fernandez", firstName: "Carmen" },
      { lastName: "Aquino", firstName: "Manuel" },
      { lastName: "Cruz", firstName: "Rosa" },
      { lastName: "Gonzales", firstName: "Pedro" },
      { lastName: "Lopez", firstName: "Teresa" },
      { lastName: "Martinez", firstName: "Francisco" },
      { lastName: "Torres", firstName: "Sofia" },
      { lastName: "Romero", firstName: "Carlos" },
      { lastName: "Villanueva", firstName: "Isabel" },
      { lastName: "Rivera", firstName: "Miguel" },
      { lastName: "Castillo", firstName: "Elena" },
      { lastName: "Ocampo", firstName: "Ramon" },
      { lastName: "Salazar", firstName: "Lourdes" },
      { lastName: "Mendoza", firstName: "Alfredo" },
      { lastName: "Ramos", firstName: "Consuelo" },
      { lastName: "Alvarez", firstName: "Ricardo" },
      { lastName: "Chavez", firstName: "Patricia" },
      { lastName: "Dizon", firstName: "Fernando" },
      { lastName: "Espino", firstName: "Guadalupe" },
      { lastName: "Flores", firstName: "Eduardo" },
      { lastName: "Gutierrez", firstName: "Rosario" },
      { lastName: "Hernandez", firstName: "Roberto" },
      { lastName: "Ignacio", firstName: "Amparo" },
      { lastName: "Jimenez", firstName: "Arturo" },
      { lastName: "Katigbak", firstName: "Beatriz" },
      { lastName: "Lim", firstName: "Ernesto" },
      { lastName: "Navarro", firstName: "Dolores" },
      { lastName: "Ortega", firstName: "Felipe" },
      { lastName: "Panganiban", firstName: "Rebecca" },
      { lastName: "Quizon", firstName: "Gregorio" },
      { lastName: "Rubio", firstName: "Victoria" }
    ];

    // Function to generate students with Filipino names
    const generateStudents = (count) => {
      return Array.from({ length: count }, (_, i) => {
        const nameIndex = i % filipinoNames.length;
        const name = filipinoNames[nameIndex];
        const studentNumber = `21-${(1760 + i).toString().padStart(4, '0')}`;
        const email = `${name.firstName.toLowerCase()}.${name.lastName.toLowerCase().replace(/\s+/g, '')}@example.com`;
        
        return {
          id: i + 1,
          name: `${name.firstName} ${name.lastName}`,
          studentNumber: studentNumber,
          email: email,
          grade: i % 5 === 0 ? null : (1.0 + (i % 4 * 0.25)).toFixed(2),
          gradeLock: false,
          take: 1,
          gradeUpdatedAt: null
        };
      });
    };
    
    subjects.value = [
      {
        id: 1,
        code: 'CS401',
        name: 'Network Security',
        section: 'BSIT-4A',
        year: 'BSIT - 4',
        academicYear: '2023-2024',
        instructor: 'Prof. Johnson',
        schedule: 'Tuesday 8:00-10:00 AM',
        room: 'IT-401',
        students: generateStudents(32),
        gradesLocked: false
      },
      {
        id: 2,
        code: 'CS302',
        name: 'Application Development',
        section: 'BSCS-3B',
        year: 'BSCS - 3',
        academicYear: '2023-2024',
        instructor: 'Prof. Johnson',
        schedule: 'Thursday 8:00-10:00 AM',
        room: 'IT-402',
        students: generateStudents(28),
        gradesLocked: false
      },
      {
        id: 3,
        code: 'CS301',
        name: 'Application Development',
        section: 'BSCS-3A',
        year: 'BSCS - 3',
        academicYear: '2023-2024',
        instructor: 'Prof. Johnson',
        schedule: 'Sunday 1:00-3:00 PM',
        room: 'IT-502',
        students: generateStudents(30),
        gradesLocked: false
      },
      {
        id: 4,
        code: 'CS201',
        name: 'Data Structures',
        section: 'BSIT-2C',
        year: 'BSIT - 2',
        academicYear: '2023-2024',
        instructor: 'Prof. Martinez',
        schedule: 'Monday 1:00-3:00 PM',
        room: 'IT-303',
        students: generateStudents(35),
        gradesLocked: false
      },
      {
        id: 5,
        code: 'CS202',
        name: 'Data Structures',
        section: 'BSIT-2D',
        year: 'BSIT - 2',
        academicYear: '2023-2024',
        instructor: 'Prof. Martinez',
        schedule: 'Wednesday 1:00-3:00 PM',
        room: 'IT-304',
        students: generateStudents(33),
        gradesLocked: false
      },
      {
        id: 6,
        code: 'CS203',
        name: 'Data Structures',
        section: 'BSIT-2A',
        year: 'BSIT - 2',
        academicYear: '2023-2024',
        instructor: 'Prof. Martinez',
        schedule: 'Sunday 9:00-11:00 AM',
        room: 'IT-304',
        students: generateStudents(36),
        gradesLocked: false
      }
    ];
    
    loading.value = false;
  } catch (error) {
    console.error('Error loading subjects:', error);
    loading.value = false;
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'Failed to load subjects. Please try again.',
      life: 3000
    });
  }
};

const openGradeInput = (student) => {
  if (gradesLocked.value && !(isRegistrar.value || isAdmin.value)) {
    toast.add({
      severity: 'warn',
      summary: 'Grades Locked',
      detail: 'Grades are submitted and locked. Only admin/registrar can unlock.',
      life: 3000
    })
    return
  }
  
  selectedStudent.value = { ...student }
  gradeDialog.value = true
}

const saveGrade = () => {
  if (!selectedStudent.value.grade) {
    gradeError.value = true;
    return;
  }

  // Get current date and time in a readable format
  const now = new Date();
  const formattedDate = now.toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hour12: true
  });

  // Find and update the student's grade with proper reactivity
  const subjectIndex = subjects.value.findIndex(s => s.id === selectedSubject.value.id);
  const studentIndex = subjects.value[subjectIndex].students.findIndex(s => s.id === selectedStudent.value.id);
  
  if (studentIndex !== -1) {
    // Create a new array to ensure reactivity
    const updatedStudents = [...subjects.value[subjectIndex].students];
    updatedStudents[studentIndex] = {
      ...updatedStudents[studentIndex],
      grade: selectedStudent.value.grade,
      gradeUpdatedAt: formattedDate // Add timestamp
    };
    
    // Update the subjects array reactively
    subjects.value = [
      ...subjects.value.slice(0, subjectIndex),
      {
        ...subjects.value[subjectIndex],
        students: updatedStudents
      },
      ...subjects.value.slice(subjectIndex + 1)
    ];
    
    // Update the selectedSubject reference
    selectedSubject.value = subjects.value[subjectIndex];
    
    toast.add({ 
      severity: 'success', 
      summary: 'Success', 
      detail: 'Grade saved successfully', 
      life: 2000 
    });

    // Find the next student who hasn't been graded yet
    const nextStudentIndex = updatedStudents.findIndex((student, index) => 
      index > studentIndex && (student.grade === null || student.grade === undefined || student.grade === '')
    );

    // If there's a next student, open the grade dialog for them
    if (nextStudentIndex !== -1) {
      // Small delay to show the success message
      setTimeout(() => {
        selectedStudent.value = { ...updatedStudents[nextStudentIndex] };
        gradeDialog.value = true;
      }, 500);
    } else {
      // No more students to grade, close the dialog
      gradeError.value = false;
      gradeDialog.value = false;
      selectedStudent.value = null;
    }
  } else {
    // If student not found, just close the dialog
    gradeError.value = false;
    gradeDialog.value = false;
    selectedStudent.value = null;
  }
};

const cancelGrade = () => {
  gradeDialog.value = false
}

const exportStudentList = () => {
  try {
    if (!selectedSubject.value) return;

    // Create CSV content
    let csvContent = "Student Number,Name,Grade,Date & Time Added\n"
    selectedSubject.value.students.forEach(student => {
      csvContent += `${student.studentNumber},${student.name},${student.grade || ''},${student.gradeUpdatedAt || ''}\n`
    })
    
    // Create download link
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `${selectedSubject.value.code}_student_list.csv`)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    
    toast.add({
      severity: 'success',
      summary: 'Export Successful',
      detail: 'Student list has been exported',
      life: 3000
    })
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Export Failed',
      detail: error.message,
      life: 3000
    })
  }
};

const submitGrades = () => {
  const studentsWithoutGrades = selectedSubject.value.students.filter(s => !s.grade);
  
  if (studentsWithoutGrades.length > 0) {
    missingGradesStudents.value = [...studentsWithoutGrades];
    showMissingGradesDialog.value = true;
  } else {
    lockGradesAndSubmit();
  }
};

const lockGradesAndSubmit = () => {
  const subjectIndex = subjects.value.findIndex(s => s.id === selectedSubject.value.id);
  
  subjects.value[subjectIndex].students.forEach(student => {
    student.gradeLock = true;
  });
  
  subjects.value[subjectIndex].gradesLocked = true;
  
  toast.add({
    severity: 'success',
    summary: 'Grades Submitted',
    detail: `All grades for ${selectedSubject.value.code} have been locked and submitted to the Registrar's Office for verification.`,
    life: 5000
  });
};

//REGISTRAR UNLOCKING OF GRADES
const unlockGrades = () => {
  confirm.require({
    message: 'Are you sure you want to unlock grades for this class? This will allow instructors to make changes.',
    header: 'Confirm Grade Unlock',
    icon: 'pi pi-exclamation-triangle',
    accept: () => {
      const subjectIndex = subjects.value.findIndex(s => s.id === selectedSubject.value.id)
      subjects.value[subjectIndex].gradesLocked = false
      
      toast.add({
        severity: 'success',
        summary: 'Grades Unlocked',
        detail: 'Grades have been unlocked for editing',
        life: 3000
      })
    }
  })
}

const allGradesComplete = computed(() => {
  return selectedSubject.value?.students.every(s => s.grade !== null && s.grade !== undefined && s.grade !== '');
});

const pendingGradesCount = computed(() => {
  return selectedSubject.value?.students.filter(s => !s.grade).length || 0;
});

const forceCompleteSubmission = ref(false); // Set to true if you want to require all grades

const showMissingGradesDialog = ref(false);
const missingGradesStudents = ref([]);

const submitAnyway = () => {
  showMissingGradesDialog.value = false;
  lockGradesAndSubmit();
};

const getRemarks = (grade) => {
  if (grade === null || grade === undefined || grade === '') return 'Incomplete';
  const numericGrade = parseFloat(grade);
  if (isNaN(numericGrade)) return 'Incomplete';
  if (numericGrade === -1) return 'Dropped';
  if (numericGrade === 0) return 'Dropped';
  if (numericGrade <= 3.0) return 'Passed';
  if (numericGrade === 5.0) return 'Failed';
  return 'Incomplete';
};

const getRemarksSeverity = (grade) => {
  if (grade === null || grade === undefined || grade === '') return 'warning';
  const numericGrade = parseFloat(grade);
  if (isNaN(numericGrade)) return 'warning';
  if (numericGrade === -1) return 'help'; 
  if (numericGrade === 0) return 'help';
  if (numericGrade <= 3.0) return 'success';
  if (numericGrade === 5.0) return 'danger';
  return 'warning';
};

const getRemarksClass = (grade) => {
  if (grade === null || grade === undefined || grade === '') return 'remarks-cell inc';
  const numericGrade = parseFloat(grade);
  if (isNaN(numericGrade)) return 'remarks-cell inc';
  if (numericGrade === -1) return 'remarks-cell drop'; 
  if (numericGrade === 0) return 'remarks-cell drop';
  if (numericGrade <= 3.0) return 'remarks-cell passed';
  if (numericGrade === 5.0) return 'remarks-cell failed';
  return 'remarks-cell inc';
};

onMounted(() => {
  loadSubjects()
})
</script>

<template>
  <div class="grid">
    <Toast />
    <ConfirmDialog />
    
    <!-- Subjects List -->
    <div class="col-12">
      <Card>
        <template #title>
          <div class="flex align-items-center justify-content-between">
            <h2 class="font-bold mr-3">My Subjects Handled</h2>
            <span class="p-input-icon-right mt-1">
              <InputText v-model="filters['global'].value" placeholder="Search class" />
            </span>
          </div>
        </template>

        <template #content>
          <DataTable
            :value="filteredSubjects"
            :loading="loading"
            :paginator="true"
            :rows="10"
            :filters="filters"
            dataKey="id"
            responsiveLayout="scroll"
            stripedRows
            class="p-datatable-customers"
            @row-click="viewStudents"
          >
            <Column field="code" header="Subject Code" sortable style="min-width: 100px">
              <template #body="{ data }">
                <div class="flex align-items-center gap-2">
                  <i class="pi pi-book" style="color: var(--primary-color)"></i>
                  <span>{{ data.code }}</span>
                  <Tag 
                    v-if="data.gradesLocked" 
                    value="Locked" 
                    severity="danger" 
                    icon="pi pi-lock" 
                    class="tag-sm"
                  />
                </div>
              </template>
            </Column>
            <Column field="name" header="Descriptive Title" sortable style="min-width: 200px" />
            <Column field="section" header="Section" sortable style="min-width: 100px">
              <template #body="{ data }">
                <Tag :value="data.section" severity="success" />
              </template>
            </Column>
            <Column field="year" header="Course & Year" sortable style="min-width: 100px">
              <template #body="{ data }">
                <Tag :value="data.year" severity="info" />
              </template>
            </Column>
            <Column field="academicYear" header="Academic Year" sortable style="min-width: 120px">
              <template #body="{ data }">
                <Tag :value="data.academicYear" severity="help" />
              </template>
            </Column>
            <Column field="schedule" header="Schedule" sortable style="min-width: 150px" />
            <Column field="room" header="Room" sortable style="min-width: 100px" />
            <Column field="students.length" header="Students" sortable style="min-width: 100px">
              <template #body="{ data }">
                <div class="flex align-items-center gap-2">
                  <i class="pi pi-users" style="color: var(--primary-color)"></i>
                  <span>{{ data.students.length }}</span>
                </div>
              </template>
            </Column>
            <Column header="Actions" style="width: 100px">
              <template #body="{ data }">
                <Button 
                  icon="pi pi-eye" 
                  class="p-button-rounded p-button-text p-button-plain"
                  v-tooltip="'View students'"
                  @click.stop="viewStudents(data)"
                />
              </template>
            </Column>
          </DataTable>
        </template>
      </Card>
    </div>

    <!-- Student Details Dialog -->
    <Dialog
      v-model:visible="dialogVisible"
      :style="{ width: '80%', maxWidth: '100%' }"
      :modal="true"
      :header="selectedSubject ? `${selectedSubject.code} - ${selectedSubject.name}` : 'Class Details'"
      :closable="true"
    >
      <template v-if="selectedSubject">
        <div class="grid">
          <!-- Class Information Section -->
          <div class="grid">
            <div class="col-12 md:col-4">
              <div class="surface-50 p-4 border-round">
                <div class="flex flex-column gap-3">
                  <div class="info-item">
                    <span class="text-sm text-color-secondary block mb-1">Schedule</span>
                    <p class="font-medium m-0">{{ selectedSubject.schedule }}</p>
                  </div>
                  <div class="info-item">
                    <span class="text-sm text-color-secondary block mb-1">Room</span>
                    <p class="font-medium m-0">{{ selectedSubject.room }}</p>
                  </div>
                  <div class="info-item">
                    <span class="text-sm text-color-secondary block mb-1">Academic Year</span>
                    <p class="font-medium m-0">{{ selectedSubject.academicYear }}</p>
                  </div>
                  <div class="info-item">
                    <span class="text-sm text-color-secondary block mb-1">Total Students</span>
                    <p class="font-medium m-0">{{ selectedSubject.students.length }}</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Student List Section -->
            <div class="col-12 md:col-8">
              <div class="surface-50 p-4 border-round">
                <div class="flex justify-content-between align-items-center mb-3">
                  <h5 class="m-0 flex align-items-center gap-2">
                    <span>Student List ({{ selectedSubject.students.length }})</span>
                    <Tag 
                      v-if="selectedSubject.students.some(s => !s.grade) && !gradesLocked"
                      value="Pending Grades"
                      severity="warning"
                      icon="pi pi-exclamation-triangle"
                      class="tag-sm"
                    />
                  </h5>
                  <div>
                    <Button 
                      icon="pi pi-download" 
                      class="p-button-success p-button-sm ml-2"
                      v-tooltip="'Export student list'"
                      @click="exportStudentList"
                    />
                  </div>
                </div>
                <DataTable
                  :value="selectedSubject.students"
                  :paginator="true"
                  :rows="10"
                  responsiveLayout="scroll"
                  stripedRows
                  class="p-datatable-sm w-full"
                  columnResizeMode="expand"
                >
                  <Column field="studentNumber" header="ID" sortable style="width: 10%">
                    <template #body="{ data }">
                      <span class="font-medium">{{ data.studentNumber }}</span>
                    </template>
                  </Column>

                  <Column field="name" header="Name" sortable style="width: 25%">
                    <template #body="{ data }">
                      <span class="font-medium">{{ data.name }}</span>
                    </template>
                  </Column>

                  <Column field="grade" header="Grade" sortable style="width: 10%">
                    <template #body="{ data }">
                      <div class="flex align-items-center justify-content-end">
                        <span v-if="data.grade" class="grade-value">
                          {{ parseFloat(data.grade).toFixed(2) }}
                        </span>
                        <span v-else class="text-color-secondary">
                          &mdash; <!-- This shows a dash for empty grades -->
                        </span>
                      </div>
                    </template>
                  </Column>

                  <Column field="remarks" header="Remarks" sortable style="width: 12%">
                    <template #body="{ data }">
                      <Tag 
                        :value="getRemarks(data.grade)"
                        :severity="getRemarksSeverity(data.grade)"
                        :class="['tag-sm', {
                          'passed-tag': getRemarks(data.grade) === 'Passed',
                          'failed-tag': getRemarks(data.grade) === 'Failed',
                          'inc-tag': getRemarks(data.grade) === 'Incomplete',
                          'drop-tag': getRemarks(data.grade) === 'Dropped'
                        }]"
                      />
                    </template>
                  </Column>

                  <Column field="gradeUpdatedAt" header="Date & Time Added" sortable style="width: 15%">
                    <template #body="{ data }">
                      <div class="flex align-items-center justify-content-end">
                        <span v-if="data.gradeUpdatedAt" class="text-xs">
                          {{ data.gradeUpdatedAt }}
                        </span>
                        <span v-else class="text-color-secondary">
                          &mdash;
                        </span>
                      </div>
                    </template>
                  </Column>

                  <Column field="take" header="Take" sortable style="width: 10%">
                    <template #body="{ data }">
                      <Tag 
                        :value="data.take" 
                        :severity="data.take > 1 ? 'danger' : 'success'"
                        class="tag-sm"
                      />
                    </template>
                  </Column>

                  <Column header="Status" style="width: 10%">
                    <template #body="{ data }">
                      <Tag 
                        :value="data.grade ? 'Graded' : 'Pending'"
                        :severity="data.grade ? 'success' : 'warning'"
                        :icon="data.grade ? 'pi pi-check' : 'pi pi-clock'"
                        class="tag-sm"
                      />
                    </template>
                  </Column>

                  <Column header="Actions" style="width: 5%">
                    <template #body="{ data }">
                      <div class="flex justify-content-end gap-2">
                        <Button 
                          v-if="!data.grade && !data.gradeLock"
                          icon="pi pi-plus" 
                          class="p-button-rounded p-button-success p-button-outlined"
                          v-tooltip="'Add Grade'"
                          @click="openGradeInput(data)"
                        />
                        <i v-if="data.gradeLock" 
                          class="pi pi-lock text-primary"
                          style="font-size: 1.2rem"
                          v-tooltip="'Grade Locked - Contact admin to modify'"
                        />
                        <Button 
                          v-if="data.grade && !data.gradeLock"
                          icon="pi pi-pencil" 
                          class="p-button-rounded p-button-warning p-button-outlined"
                          v-tooltip="'Edit Grade'"
                          @click="openGradeInput(data)"
                        />
                      </div>
                    </template>
                  </Column>
                </DataTable>
                
                <div class="button-center-container"> 
                  <Button 
                    v-if="!gradesLocked && !(isRegistrar || isAdmin)"
                    :label="allGradesComplete ? 'Submit & Lock Grades' : 'Submit with Missing Grades'"
                    :icon="allGradesComplete ? 'pi pi-lock' : 'pi pi-exclamation-triangle'"
                    :class="[
                      'w-full md:w-20%',
                      allGradesComplete ? 'p-button-success' : 'p-button-warning'
                    ]"
                    @click="submitGrades"
                    :disabled="!allGradesComplete && forceCompleteSubmission"
                    v-tooltip="allGradesComplete 
                      ? 'All grades are complete - ready to submit' 
                      : `${pendingGradesCount} students still need grades`"
                  />
                  <Button 
                    v-if="gradesLocked && (isRegistrar || isAdmin)"
                    label="Unlock Grades" 
                    icon="pi pi-lock-open" 
                    class="w-20% p-button-danger"
                    @click="unlockGrades"
                    v-tooltip="'Unlock grades for editing (Admin/Registrar only)'"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </template>
    </Dialog>

    <!-- Grade Dialog -->
    <Dialog
      v-model:visible="gradeDialog"
      :style="{ width: '30vw', maxWidth: '400px' }"
      :modal="true"
      :showHeaderCloseIcon="false"
      :closable="false"
      class="grade-dialog"
    >
      <template v-if="selectedStudent">
        <div class="grid">
          <div class="col-12">
            <div class="flex justify-content-between align-items-center mb-4">
              <div>
                <h2 class="m-0">{{ selectedStudent.name }}</h2>
                <p class="text-color-secondary m-0">{{ selectedStudent.studentNumber }}</p>
              </div>
            </div>
          </div>

          <div class="col-12">
            <Dropdown
              v-model="selectedStudent.grade"
              :options="gradeOptions"
              optionLabel="label"
              optionValue="value"
              placeholder="Select a grade"
              class="w-full"
              :class="{ 'p-invalid': gradeError }"
              :disabled="gradesLocked"
            />
            <small v-if="gradeError" class="p-error">Please select a valid grade</small>
          </div>

          <div class="col-12 mt-4 flex gap-2">
            <Button 
              v-if="!gradesLocked"
              :label="selectedStudent.grade ? 'Save' : 'Submit'" 
              icon="pi pi-check" 
              class="p-button-success flex-1"
              @click="saveGrade"
            />
            <Button 
              label="Close" 
              icon="pi pi-times" 
              class="p-button-secondary flex-1"
              @click="cancelGrade"
            />
          </div>
        </div>
      </template>
    </Dialog>

    <!-- Missing Grades Dialog -->
    <Dialog 
      v-model:visible="showMissingGradesDialog" 
      :modal="true"
      :style="{ width: '500px', maxWidth: '90vw' }"
      :closable="false"
      class="missing-grades-dialog"
    >
      <template #header>
        <div class="dialog-header-content">
          <i class="pi pi-exclamation-triangle text-red-500"></i>
          <span class="dialog-title">Missing Grades Detected</span>
        </div>
      </template>
      <div class="confirmation-content missing-grades-dialog">
        <p class="text-color-secondary">{{ missingGradesStudents.length }} student(s) have not been graded yet:</p>
        <div class="overflow-auto border-round border-1 border-300 mt-2 p-3" style="max-height: 200px">
          <ul class="m-0 p-0 list-none">
            <li v-for="student in missingGradesStudents" :key="student.id" class="py-2 border-bottom-1 border-300">
              <i class="pi pi-user mr-2"></i>
              <span class="font-medium">{{ student.name }}</span>
              <span class="text-color-secondary ml-2">({{ student.studentNumber }})</span>
            </li>
          </ul>
        </div>
        <p class="mt-3 font-medium">Would you like to submit the grades anyway, or complete the missing grades first?</p>
      </div>
      <template #footer>
        <div style="display: flex; justify-content: space-around;  width: 100%;">
          <Button label="Complete Grades First" icon="pi pi-times" @click="showMissingGradesDialog = false" class="p-button-text" />
          <Button label="Submit Anyway" icon="pi pi-check" @click="submitAnyway" class="p-button-warning" autofocus />
        </div>
      </template>
    </Dialog>
  </div>
</template>

<style scoped>
/* Improved Tag styling */
.tag-sm {
  padding: 0.25rem 0.75rem;
  font-size: 0.85rem;
}

/* Information sections styling */
.surface-50 {
  background-color: var(--surface-50);
  transition: background-color 0.2s;
}

.info-item {
  padding: 0.75rem;
  border-radius: 6px;
  background-color: var(--surface-a);
  margin-bottom: 1rem;
}

/* Table improvements */
:deep(.p-datatable .p-datatable-tbody > tr) {
  cursor: pointer;
  transition: background-color 0.2s;
}

:deep(.p-datatable .p-datatable-tbody > tr:hover) {
  background-color: rgba(0, 0, 0, 0.03) !important;
}

/* Grade dialog specific styles */
:deep(.p-dialog.grade-dialog .p-dialog-header) {
  display: none !important;
}

:deep(.p-dialog.grade-dialog .p-dialog-content) {
  padding: 1.5rem !important;
}

.button-center-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 1.5rem;
  gap: 0.5rem;
}

/* Add to your existing styles */
.grade-value {
  font-weight: 600;
  min-width: 3.5rem;
  text-align: center;
}

.text-color-secondary {
  color: var(--text-color-secondary);
}

.pendingGradesMessage {
    width: 100vw;
    min-width: 500px;
    max-width: 1000px;
}

/* Responsive adjustments */
@media (min-width: 768px) {
  :deep(.md\:w-20\%) {
    width: 20%;
  }
}

/* Missing Grades Dialog Styles */
:deep(.missing-grades-dialog) .p-dialog-header {
  display: flex;
  justify-content: flex-end;  /* Changed from center to flex-end */
  align-items: center;
  padding: 1.25rem 1.5rem;
  width: 100%;
}

.dialog-header-content {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.dialog-header-content i {
  font-size: 1.5rem;
}

.dialog-title {
  font-size: 1.25rem;
  font-weight: 600;
  line-height: 1.2;
}

/* Remarks column styling */
:deep(.p-tag) {
  font-weight: 500;
  min-width: 80px;
  justify-content: center;
}

/* Remarks Column Styles */
.remarks-cell {
  padding: 0 !important;
}

.remarks-cell .p-tag {
  width: 100%;
  text-align: center;
  border: none !important;
}

/* Background colors for remarks */
.remarks-cell.passed {
  color: #2ecc71;
  background-color: rgba(46, 204, 113, 0.1) !important;
}

.remarks-cell.failed {
  color: #e74c3c;
  background-color: rgba(231, 76, 60, 0.1) !important;
}

.remarks-cell.inc {
  color: #e67e22;
  background-color: rgba(230, 126, 34, 0.1) !important;
}

.remarks-cell.drop {
  color: #9b59b6;
  background-color: rgba(155, 89, 182, 0.1) !important;
}

/* Status tag styles */
.p-tag.passed-tag {
  background-color: rgba(46, 204, 113, 0.1) !important;
  color: #2ecc71 !important;
}

.p-tag.failed-tag {
  background-color: rgba(231, 76, 60, 0.1) !important;
  color: #e74c3c !important;
}

.p-tag.inc-tag {
  background-color: rgba(230, 126, 34, 0.1) !important;
  color: #e67e22 !important;
}

.p-tag.drop-tag {
  background-color: rgba(155, 89, 182, 0.1) !important;
  color: #9b59b6 !important;
}

/* Dropdown styles for Dropped status */
:deep(.p-dropdown .p-dropdown-label.p-placeholder) {
  color: #9b59b6;
}

:deep(.p-dropdown:not(.p-disabled).p-focus) {
  box-shadow: 0 0 0 0.2rem rgba(155, 89, 182, 0.2);
  border-color: #9b59b6;
}

:deep(.p-dropdown:not(.p-disabled).p-focus .p-inputtext) {
  border-color: #9b59b6;
}

:deep(.p-dropdown-item.p-highlight) {
  background: rgba(155, 89, 182, 0.1);
  color: #9b59b6;
}

:deep(.p-dropdown-item.p-highlight.p-focus) {
  background: rgba(155, 89, 182, 0.2);
}

/* Remove background and text color from Take column */
:deep(.p-datatable .p-datatable-tbody > tr > td:nth-child(6) .p-tag) {
  background-color: transparent !important;
  color: inherit !important;
}

/* Remove background and text color from Status column */
:deep(.p-datatable .p-datatable-tbody > tr > td:nth-child(7) .p-tag) {
  background-color: transparent !important;
  color: inherit !important;
}

/* Style for Take and Status columns to match ID and Name */
:deep(.p-datatable .p-datatable-tbody > tr > td:nth-child(6) .p-tag),
:deep(.p-datatable .p-datatable-tbody > tr > td:nth-child(7) .p-tag) {
  background-color: transparent !important;
  color: inherit !important;
  font-size: 0.875rem; /* Match the default font size */
  line-height: 1.5; /* Match the default line height */
  padding: 0.25rem 0.5rem; /* Adjust padding to match other cells */
}

/* Ensure the text inside spans in these columns also matches */
:deep(.p-datatable .p-datatable-tbody > tr > td:nth-child(6) .p-tag .p-tag-value),
:deep(.p-datatable .p-datatable-tbody > tr > td:nth-child(7) .p-tag .p-tag-value) {
  font-size: 0.875rem;
}
</style>