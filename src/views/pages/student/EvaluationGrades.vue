<template>
  <div class="evaluation">
    <h2>My Evaluation of Grades</h2>

    <div class="selectors p-fluid p-grid">
      <div class="p-field p-col-12 p-md-6 p-lg-3 p-mb-2">
        <label for="academicYear" class="p-d-block p-mb-2">Academic Year</label>
        <Dropdown 
          id="academicYear" 
          v-model="selectedYear" 
          :options="evaluationData" 
          optionLabel="year" 
          class="w-100" 
          placeholder="Select Academic Year"
          @change="onYearChange">
          <template #value="slotProps">
            <div v-if="slotProps.value">
              {{ slotProps.value.year }}
            </div>
            <span v-else>
              Select Year
            </span>
          </template>
        </Dropdown>
      </div>
      <div class="p-field p-col-12 p-md-6 p-lg-3 p-mb-2">
        <label for="semester" class="p-d-block p-mb-2">Semester</label>
        <Dropdown 
          id="semester" 
          v-model="selectedSemester" 
          :options="selectedYear ? selectedYear.semesters : []" 
          optionLabel="semester" 
          class="w-100" 
          :disabled="!selectedYear"
          placeholder="Select Semester">
        </Dropdown>
      </div>
    </div>

    <div v-if="currentSemester" class="semester-header">
      <h6>{{ selectedYear.year }}, {{ selectedSemester.semester }}, AY {{ selectedYear.schoolYear }}</h6>

    <table v-if="currentSemester">
      <thead>
        <tr>
          <th>Subject Code</th>
          <th>Subject Name</th>
          <th>Units</th>
          <th>Prerequisite</th>
          <th>Corequisite</th>
          <th>Final Grade</th>
          <th>Status</th>
          <th>Remarks</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="subject in currentSemester.subjects" :key="subject.subjectCode">
          <td>{{ subject.subjectCode }}</td>
          <td>{{ subject.subjectName }}</td>
          <td>{{ subject.units }}</td>
          <td>{{ subject.prerequisite || 'None' }}</td>
          <td>{{ subject.corequisite || 'None' }}</td>
          <td>{{ subject.finalGrade }}</td>
          <td>
            <span :class="{
              'passed': subject.status === 'Passed',
              'failed': subject.status === 'Failed',
              'inc': subject.status === 'Incomplete',
              'drop': subject.status === 'Dropped'
            }">
              {{ subject.status }}
            </span>
          </td>
          <td>{{ subject.remarks || '-' }}</td>
        </tr>
        <tr class="semester-summary">
          <td colspan="2">Total Units:</td>
          <td colspan="2">{{ currentSemester.totalUnits }}</td>
          <td colspan="1">GPA:</td>
          <td colspan="3">{{ currentSemester.gpa }}</td>
        </tr>
      </tbody>
    </table>
  </div>

    <div class="overall-summary">
      <div class="summary-row">
        <span class="summary-label">Total Units Earned</span>
        <span class="summary-separator">:</span>
        <span class="summary-value">{{ overallSummary.totalUnits }}</span>
      </div>
      <div class="summary-row">
        <span class="summary-label">Total Subjects Taken</span>
        <span class="summary-separator">:</span>
        <span class="summary-value">{{ overallSummary.totalSubjects }}</span>
      </div>
      <div class="summary-row">
        <span class="summary-label">Cumulative GPA</span>
        <span class="summary-separator">:</span>
        <span class="summary-value">{{ overallSummary.cumulativeGPA }}</span>
      </div>
    </div>

    <div class="legend">
      <h4>Legend:</h4>
      <div class="legend-items">
        <span class="legend-item passed">Passed</span>
        <span class="legend-item failed">Failed</span>
        <span class="legend-item inc">Incomplete</span>
        <span class="legend-item drop">Dropped</span>
      </div>
    </div>
  </div>
</template>

<script>
import Dropdown from 'primevue/dropdown';

export default {
  name: 'EvaluationOfGrades',
  components: {
    Dropdown
  },
  data() {
    return {
      selectedYear: null,
      selectedSemester: null,
      evaluationData: [
        {
          year: 'First Year',
          schoolYear: '2023-2024',
          semesters: [
            {
              semester: 'First Semester',
              subjects: [
                {
                  subjectCode: 'MATH101',
                  subjectName: 'College Algebra',
                  units: 3,
                  prerequisite: 'None',
                  corequisite: 'None',
                  finalGrade: '1.50',
                  status: 'Passed',
                  remarks: '-'
                },
                {
                  subjectCode: 'ENG101',
                  subjectName: 'Communication Skills 1',
                  units: 3,
                  prerequisite: 'None',
                  corequisite: 'None',
                  finalGrade: '1.75',
                  status: 'Passed',
                  remarks: '-'
                },
                {
                  subjectCode: 'FIL101',
                  subjectName: 'Komunikasyon sa Akademikong Filipino',
                  units: 3,
                  prerequisite: 'None',
                  corequisite: 'None',
                  finalGrade: '1.25',
                  status: 'Passed',
                  remarks: '-'
                },
                {
                  subjectCode: 'NSTP1',
                  subjectName: 'National Service Training Program 1',
                  units: 3,
                  prerequisite: 'None',
                  corequisite: 'None',
                  finalGrade: '1.00',
                  status: 'Passed',
                  remarks: '-'
                }
              ],
              totalUnits: 12,
              gpa: '1.38'
            },
            {
              semester: 'Second Semester',
              subjects: [
                {
                  subjectCode: 'MATH102',
                  subjectName: 'Trigonometry',
                  units: 3,
                  prerequisite: 'MATH101',
                  corequisite: 'None',
                  finalGrade: '1.75',
                  status: 'Passed',
                  remarks: '-'
                },
                {
                  subjectCode: 'ENG102',
                  subjectName: 'Communication Skills 2',
                  units: 3,
                  prerequisite: 'ENG101',
                  corequisite: 'None',
                  finalGrade: '2.00',
                  status: 'Passed',
                  remarks: '-'
                },
                {
                  subjectCode: 'PHYS101',
                  subjectName: 'Physics for Engineers',
                  units: 4,
                  prerequisite: 'MATH101',
                  corequisite: 'MATH102',
                  finalGrade: '2.25',
                  status: 'Passed',
                  remarks: 'Conditional'
                },
                {
                  subjectCode: 'NSTP2',
                  subjectName: 'National Service Training Program 2',
                  units: 3,
                  prerequisite: 'NSTP1',
                  corequisite: 'None',
                  finalGrade: '1.00',
                  status: 'Passed',
                  remarks: '-'
                }
              ],
              totalUnits: 13,
              gpa: '1.75'
            }
          ]
        },
        {
          year: 'Second Year',
          schoolYear: '2024-2025',
          semesters: [
            {
              semester: 'First Semester',
              subjects: [
                {
                  subjectCode: 'MATH201',
                  subjectName: 'Calculus 1',
                  units: 4,
                  prerequisite: 'MATH102',
                  corequisite: 'None',
                  finalGrade: '2.00',
                  status: 'Passed',
                  remarks: '-'
                },
                {
                  subjectCode: 'PHYS201',
                  subjectName: 'Engineering Physics',
                  units: 4,
                  prerequisite: 'PHYS101, MATH102',
                  corequisite: 'MATH201',
                  finalGrade: '2.25',
                  status: 'Passed',
                  remarks: '-'
                },
                {
                  subjectCode: 'CS201',
                  subjectName: 'Computer Programming 1',
                  units: 3,
                  prerequisite: 'None',
                  corequisite: 'None',
                  finalGrade: '1.50',
                  status: 'Passed',
                  remarks: '-'
                },
                {
                  subjectCode: 'HUM101',
                  subjectName: 'Art Appreciation',
                  units: 3,
                  prerequisite: 'None',
                  corequisite: 'None',
                  finalGrade: '1.25',
                  status: 'Passed',
                  remarks: '-'
                }
              ],
              totalUnits: 14,
              gpa: '1.75'
            },
            {
              semester: 'Second Semester',
              subjects: [
                {
                  subjectCode: 'MATH202',
                  subjectName: 'Calculus 2',
                  units: 4,
                  prerequisite: 'MATH201',
                  corequisite: 'None',
                  finalGrade: '2.25',
                  status: 'Passed',
                  remarks: '-'
                },
                {
                  subjectCode: 'CS202',
                  subjectName: 'Computer Programming 2',
                  units: 3,
                  prerequisite: 'CS201',
                  corequisite: 'None',
                  finalGrade: '1.75',
                  status: 'Passed',
                  remarks: '-'
                },
                {
                  subjectCode: 'CHEM201',
                  subjectName: 'General Chemistry',
                  units: 4,
                  prerequisite: 'None',
                  corequisite: 'None',
                  finalGrade: '2.00',
                  status: 'Passed',
                  remarks: '-'
                },
                {
                  subjectCode: 'SOCSCI101',
                  subjectName: 'Understanding the Self',
                  units: 3,
                  prerequisite: 'None',
                  corequisite: 'None',
                  finalGrade: '1.50',
                  status: 'Passed',
                  remarks: '-'
                }
              ],
              totalUnits: 14,
              gpa: '1.88'
            }
          ]
        },
        {
          year: 'Third Year',
          schoolYear: '2025-2026',
          semesters: [
            {
              semester: 'First Semester',
              subjects: [
                {
                  subjectCode: 'CS301',
                  subjectName: 'Data Structures and Algorithms',
                  units: 3,
                  prerequisite: 'CS202',
                  corequisite: 'None',
                  finalGrade: '1.75',
                  status: 'Passed',
                  remarks: '-'
                },
                {
                  subjectCode: 'MATH301',
                  subjectName: 'Discrete Mathematics',
                  units: 3,
                  prerequisite: 'MATH202',
                  corequisite: 'None',
                  finalGrade: '2.00',
                  status: 'Passed',
                  remarks: '-'
                },
                {
                  subjectCode: 'CS302',
                  subjectName: 'Database Management Systems',
                  units: 3,
                  prerequisite: 'CS201',
                  corequisite: 'None',
                  finalGrade: '1.50',
                  status: 'Passed',
                  remarks: '-'
                },
                {
                  subjectCode: 'HUM102',
                  subjectName: 'Ethics',
                  units: 3,
                  prerequisite: 'None',
                  corequisite: 'None',
                  finalGrade: '1.25',
                  status: 'Passed',
                  remarks: '-'
                }
              ],
              totalUnits: 12,
              gpa: '1.63'
            },
            {
              semester: 'Second Semester',
              subjects: [
                {
                  subjectCode: 'CS303',
                  subjectName: 'Object-Oriented Programming',
                  units: 3,
                  prerequisite: 'CS202',
                  corequisite: 'None',
                  finalGrade: '1.75',
                  status: 'Passed',
                  remarks: '-'
                },
                {
                  subjectCode: 'CS304',
                  subjectName: 'Web Development',
                  units: 3,
                  prerequisite: 'CS201',
                  corequisite: 'None',
                  finalGrade: '1.50',
                  status: 'Passed',
                  remarks: '-'
                },
                {
                  subjectCode: 'MATH302',
                  subjectName: 'Probability and Statistics',
                  units: 3,
                  prerequisite: 'MATH202',
                  corequisite: 'None',
                  finalGrade: '2.00',
                  status: 'Passed',
                  remarks: '-'
                },
                {
                  subjectCode: 'SOCSCI102',
                  subjectName: 'Life and Works of Rizal',
                  units: 3,
                  prerequisite: 'None',
                  corequisite: 'None',
                  finalGrade: '1.25',
                  status: 'Passed',
                  remarks: '-'
                }
              ],
              totalUnits: 12,
              gpa: '1.63'
            }
          ]
        },
        {
          year: 'Fourth Year',
          schoolYear: '2026-2027',
          semesters: [
            {
              semester: 'First Semester',
              subjects: [
                {
                  subjectCode: 'CS401',
                  subjectName: 'Software Engineering',
                  units: 3,
                  prerequisite: 'CS303, CS304',
                  corequisite: 'None',
                  finalGrade: '1.75',
                  status: 'Passed',
                  remarks: '-'
                },
                {
                  subjectCode: 'CS402',
                  subjectName: 'Mobile Application Development',
                  units: 3,
                  prerequisite: 'CS304',
                  corequisite: 'None',
                  finalGrade: '1.50',
                  status: 'Passed',
                  remarks: '-'
                },
                {
                  subjectCode: 'CS403',
                  subjectName: 'Networking',
                  units: 3,
                  prerequisite: 'CS301',
                  corequisite: 'None',
                  finalGrade: '2.00',
                  status: 'Passed',
                  remarks: '-'
                },
                {
                  subjectCode: 'CS404',
                  subjectName: 'Thesis 1',
                  units: 3,
                  prerequisite: 'Completion of 90 units',
                  corequisite: 'None',
                  finalGrade: '1.75',
                  status: 'Passed',
                  remarks: '-'
                }
              ],
              totalUnits: 12,
              gpa: '1.75'
            },
            {
              semester: 'Second Semester',
              subjects: [
                {
                  subjectCode: 'CS405',
                  subjectName: 'Artificial Intelligence',
                  units: 3,
                  prerequisite: 'CS301, MATH302',
                  corequisite: 'None',
                  finalGrade: '1.75',
                  status: 'Passed',
                  remarks: '-'
                },
                {
                  subjectCode: 'CS406',
                  subjectName: 'Capstone Project',
                  units: 3,
                  prerequisite: 'CS404',
                  corequisite: 'None',
                  finalGrade: '1.50',
                  status: 'Passed',
                  remarks: '-'
                },
                {
                  subjectCode: 'CS407',
                  subjectName: 'Professional Elective',
                  units: 3,
                  prerequisite: 'Completion of 90 units',
                  corequisite: 'None',
                  finalGrade: '1.75',
                  status: 'Passed',
                  remarks: '-'
                },
                {
                  subjectCode: 'CS408',
                  subjectName: 'Practicum',
                  units: 6,
                  prerequisite: 'Completion of 90 units',
                  corequisite: 'None',
                  finalGrade: '1.25',
                  status: 'Passed',
                  remarks: '-'
                }
              ],
              totalUnits: 15,
              gpa: '1.56'
            }
          ]
        }
      ],
      overallSummary: {
        totalUnits: 104,
        totalSubjects: 32,
        cumulativeGPA: '1.68',
        academicStanding: 'Good Standing'
      }
    }
  },
  computed: {
    currentSemester() {
      return this.selectedSemester;
    }
  },
  methods: {
    onYearChange() {
      this.selectedSemester = null;
      // Auto-select first semester if available
      if (this.selectedYear?.semesters?.length > 0) {
        this.selectedSemester = this.selectedYear.semesters[0];
      }
    }
  },
  created() {
    // Set initial values
    if (this.evaluationData.length > 0) {
      this.selectedYear = this.evaluationData[0];
      if (this.selectedYear.semesters?.length > 0) {
        this.selectedSemester = this.selectedYear.semesters[0];
      }
    }
  }
}
</script>

<style scoped>
.evaluation {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  width: 100%;
  margin: 0 auto;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.07);
}

h2 {
  margin-top: 0;
  color: #333;
  text-align: start;
}

.selectors {
  margin-bottom: 1.5rem;
  display: flex;
  gap: 1.5rem;
  align-items: center;
  justify-content: left;
}

.selectors label {
  font-weight: 600;
}

.selectors select {
  padding: 8px 12px;
  border-radius: 4px;
  border: 1px solid #ddd;
  font-size: 1rem;
  margin-left: 7px;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.95rem;
  margin-bottom: 1.5rem;
}

th {
  background: #f7f7f7;
  padding: 12px;
  font-weight: 600;
  color: #333;
  border-bottom: 2px solid #eee;
  text-align: left;
}

td {
  padding: 12px;
  color: #444;
  border-bottom: 1px solid #eee;
  text-align: left;
}

tr:nth-child(even) {
  background: #f9f9f9;
}

tr:hover {
  background: #f4f4f4;
}

.semester-summary {
  background-color: rgba(46, 204, 113, 0.1);
  font-weight: 600;
}

.summary-row {
  display: flex;
  align-items: center;
  margin-bottom: 0.25rem;
  width: auto;
}

.summary-label {
  min-width: 150px;
  text-align: left;
  font-weight: 600;
  color: #333;
}

.summary-separator {
  margin-right: 25px;
  font-weight: 600;
  color: #333;
}

.summary-value {
  color: #2c3e50;
  font-weight: bold;
}

.legend {
  margin-top: 1.5rem;
  padding-top: 1rem;
}

.legend h4 {
  margin: 0 0 0.5rem 0;
  font-size: 1rem;
  color: #666;
}

.legend-items {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.legend-item {
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 0.85rem;
  font-weight: 500;
}

.passed {
  color: #2ecc71;
  font-weight: 600;
}

.failed {
  color: #e74c3c;
  font-weight: 600;
}

.inc {
  color: #f39c12;
  font-weight: 600;
}

.drop {
  color: #9b59b6;
  font-weight: 600;
}

.legend-item.passed {
  background-color: rgba(46, 204, 113, 0.1);
}

.legend-item.failed {
  background-color: rgba(231, 76, 60, 0.1);
}

.legend-item.inc {
  background-color: rgba(243, 156, 18, 0.1);
}

.legend-item.drop {
  background-color: rgba(155, 89, 182, 0.1);
}

.semester-header {
  padding: 12px;
  border-radius: 4px;
  margin-bottom: 1rem;
}

@media (max-width: 768px) {
  .evaluation {
    padding: 16px;
  }

  .selectors {
    flex-direction: column;
    gap: 0.7rem;
  }

  table {
    font-size: 0.85rem;
  }

  th,
  td {
    padding: 8px;
  }
}
</style>