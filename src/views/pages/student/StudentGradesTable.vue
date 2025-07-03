<template>
  <div class="transcript">
    <h2>My Transcript of Records</h2>
    <div v-for="(year, index) in transcript" :key="year.year" class="academic-year">
      <h3>{{ year.year }} ({{ year.schoolYear }})</h3>
      <div v-for="semester in year.semesters" :key="semester.semester" class="semester">
        <h4>{{ semester.semester }}</h4>
        <table>
          <thead>
            <tr>
              <th>Subject Code</th>
              <th>Descriptive Title</th>
              <th>Units</th>
              <th>Final Grade</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="grade in semester.grades" :key="grade.subjectCode">
              <td>{{ grade.subjectCode }}</td>
              <td>{{ grade.descriptiveTitle }}</td>
              <td>{{ grade.units }}</td>
              <td>{{ grade.finalGrade }}</td>
              <td>
                <span :class="{'passed': grade.status === 'Passed', 'failed': grade.status === 'Failed'}">
                  {{ grade.status }}
                </span>
              </td>
            </tr>
            <tr class="semester-summary">
              <td colspan="2">Total Units</td>
              <td>{{ semester.totalUnits }}</td>
              <td>GPA</td>
              <td>{{ semester.gpa }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div class="overall-summary">
      <div class="summary-row">
        <span>Total Units</span>
        <span>:</span>
        <span class="value">{{ overallSummary.totalUnits }}</span>
      </div>
      <div class="summary-row">
        <span>Cumulative GPA</span>
        <span>:</span>
        <span class="value">{{ overallSummary.cumulativeGPA }}</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StudentGradesTable',
  data() {
    return {
      transcript: [
        {
          year: 'First Year',
          schoolYear: '2023-2024',
          semesters: [
            {
              semester: 'First Semester',
              grades: [
                {
                  subjectCode: 'MATH101',
                  descriptiveTitle: 'Mathematics 1',
                  units: 3,
                  finalGrade: '1.25',
                  status: 'Passed'
                },
                {
                  subjectCode: 'PHYS101',
                  descriptiveTitle: 'Physics 1',
                  units: 4,
                  finalGrade: '1.75',
                  status: 'Passed'
                },
                {
                  subjectCode: 'ENG101',
                  descriptiveTitle: 'English 1',
                  units: 3,
                  finalGrade: '2.00',
                  status: 'Passed'
                }
              ],
              totalUnits: 10,
              gpa: '1.67'
            },
            {
              semester: 'Second Semester',
              grades: [
                {
                  subjectCode: 'MATH102',
                  descriptiveTitle: 'Mathematics 2',
                  units: 3,
                  finalGrade: '1.50',
                  status: 'Passed'
                },
                {
                  subjectCode: 'PHYS102',
                  descriptiveTitle: 'Physics 2',
                  units: 4,
                  finalGrade: '1.75',
                  status: 'Passed'
                },
                {
                  subjectCode: 'ENG102',
                  descriptiveTitle: 'English 2',
                  units: 3,
                  finalGrade: '2.25',
                  status: 'Passed'
                }
              ],
              totalUnits: 10,
              gpa: '1.83'
            }
          ]
        },
        {
          year: 'Second Year',
          schoolYear: '2024-2025',
          semesters: [
            {
              semester: 'First Semester',
              grades: [
                {
                  subjectCode: 'MATH201',
                  descriptiveTitle: 'Mathematics 3',
                  units: 3,
                  finalGrade: '1.75',
                  status: 'Passed'
                },
                {
                  subjectCode: 'PHYS201',
                  descriptiveTitle: 'Physics 3',
                  units: 4,
                  finalGrade: '2.00',
                  status: 'Passed'
                },
                {
                  subjectCode: 'ENG201',
                  descriptiveTitle: 'English 3',
                  units: 3,
                  finalGrade: '2.50',
                  status: 'Passed'
                }
              ],
              totalUnits: 10,
              gpa: '2.08'
            }
          ]
        },
        {
          year: 'Third Year',
          schoolYear: '2025-2026',
          semesters: [
            {
              semester: 'First Semester',
              grades: [
                {
                  subjectCode: 'MATH301',
                  descriptiveTitle: 'Mathematics 4',
                  units: 3,
                  finalGrade: '1.85',
                  status: 'Passed'
                },
                {
                  subjectCode: 'PHYS301',
                  descriptiveTitle: 'Physics 4',
                  units: 4,
                  finalGrade: '2.10',
                  status: 'Passed'
                },
                {
                  subjectCode: 'ENG301',
                  descriptiveTitle: 'English 4',
                  units: 3,
                  finalGrade: '2.75',
                  status: 'Passed'
                }
              ],
              totalUnits: 10,
              gpa: '2.23'
            }
          ]
        },
        {
          year: 'Fourth Year',
          schoolYear: '2026-2027',
          semesters: [
            {
              semester: 'First Semester',
              grades: [
                {
                  subjectCode: 'MATH401',
                  descriptiveTitle: 'Mathematics 5',
                  units: 3,
                  finalGrade: '2.00',
                  status: 'Passed'
                },
                {
                  subjectCode: 'PHYS401',
                  descriptiveTitle: 'Physics 5',
                  units: 4,
                  finalGrade: '2.25',
                  status: 'Passed'
                },
                {
                  subjectCode: 'ENG401',
                  descriptiveTitle: 'English 5',
                  units: 3,
                  finalGrade: '3.00',
                  status: 'Passed'
                }
              ],
              totalUnits: 10,
              gpa: '2.42'
            }
          ]
        }
      ],
      overallSummary: {
        totalUnits: 40,
        cumulativeGPA: '2.03'
      }
    }
  }
}
</script>

<style scoped>
.transcript {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}

.academic-year {
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #eee;
}

.academic-year:last-child {
  border-bottom: none;
}

.academic-year h3 {
  color: #333;
  margin: 0 0 1rem 0;
  font-size: 1.25rem;
}

.semester {
  margin-bottom: 1.5rem;
}

.semester h4 {
  color: #666;
  margin: 0 0 0.5rem 0;
  font-size: 1.1rem;
}

.semester table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.95rem;
}

.semester th {
  background: #f7f7f7;
  padding: 12px;
  font-weight: 600;
  color: #333;
  border-bottom: 2px solid #eee;
  text-align: left;
}

.semester td {
  padding: 12px;
  color: #444;
  border-bottom: 1px solid #eee;
  text-align: left;
}

.semester tr:nth-child(even) {
  background: #f9f9f9;
}

.semester tr:hover {
  background: #f4f4f4;
}

.semester-summary {
  background: #ACE1AF;
  font-weight: 600;
}



.summary-row {
  display: flex;
  margin-bottom: 0.25rem;
  gap: 1rem;
}

.summary-row span:first-child {
  min-width: 110px;
  text-align: left;
}

.summary-row .value {
  min-width: 50px;
  text-align: left;
  font-weight: bold;
}

.passed {
  color: #2ecc71;
  font-weight: 600;
}

.failed {
  color: #e74c3c;
  font-weight: 600;
}

@media (max-width: 768px) {
  .transcript {
    padding: 16px;
  }
  
  .academic-year h3,
  .semester h4 {
    font-size: 1rem;
  }
  
  .semester th,
  .semester td {
    padding: 8px;
    font-size: 0.9rem;
  }
  
  .summary-row {
    font-size: 0.9rem;
  }
}
</style>