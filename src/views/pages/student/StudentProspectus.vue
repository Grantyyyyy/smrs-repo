<template>
    <div class="prospectus">
      <h2>Course Prospectus</h2>
      <div v-for="(year, index) in prospectus" :key="year.year" class="academic-year">
        <h3>{{ year.year }} ({{ year.schoolYear }})</h3>
        <div v-for="semester in year.semesters" :key="semester.semester" class="semester">
          <h4>{{ semester.semester }}</h4>
          <table>
            <thead>
              <tr>
                <th>Subject Code</th>
                <th>Subject Name</th>
                <th>Units</th>
                <th>Final Grade</th>
                <th>Prerequisites</th>
                <th>Corequisites</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="subject in semester.subjects" :key="subject.subjectCode">
                <td>{{ subject.subjectCode }}</td>
                <td>{{ subject.subjectName }}</td>
                <td>{{ subject.units }}</td>
                <td>{{ subject.finalGrade }}</td>
                <td>{{ subject.prerequisites || '-' }}</td>
                <td>{{ subject.corequisites || '-' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
      <div class="overall-summary">
        <h3>Overall Summary</h3>
        <div class="summary-row">
          <span>Total Units Earned</span>
          <span>{{ overallSummary.totalUnits }}</span>
        </div>
        <div class="summary-row">
          <span>General Weighted Average (GWA)</span>
          <span>{{ overallSummary.gwa }}</span>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'CourseProspectus',
    data() {
      return {
        prospectus: [
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
                    finalGrade: '1.50',
                    prerequisites: 'None',
                    corequisites: 'None'
                  },
                  {
                    subjectCode: 'ENG101',
                    subjectName: 'Communication Skills 1',
                    units: 3,
                    finalGrade: '1.75',
                    prerequisites: 'None',
                    corequisites: 'None'
                  },
                  {
                    subjectCode: 'FIL101',
                    subjectName: 'Komunikasyon sa Akademikong Filipino',
                    units: 3,
                    finalGrade: '1.25',
                    prerequisites: 'None',
                    corequisites: 'None'
                  },
                  {
                    subjectCode: 'NSTP1',
                    subjectName: 'National Service Training Program 1',
                    units: 3,
                    finalGrade: '1.00',
                    prerequisites: 'None',
                    corequisites: 'None'
                  }
                ]
              },
              {
                semester: 'Second Semester',
                subjects: [
                  {
                    subjectCode: 'MATH102',
                    subjectName: 'Trigonometry',
                    units: 3,
                    finalGrade: '1.75',
                    prerequisites: 'MATH101',
                    corequisites: 'None'
                  },
                  {
                    subjectCode: 'ENG102',
                    subjectName: 'Communication Skills 2',
                    units: 3,
                    finalGrade: '2.00',
                    prerequisites: 'ENG101',
                    corequisites: 'None'
                  },
                  {
                    subjectCode: 'PHYS101',
                    subjectName: 'Physics for Engineers',
                    units: 4,
                    finalGrade: '2.25',
                    prerequisites: 'MATH101',
                    corequisites: 'MATH102'
                  },
                  {
                    subjectCode: 'NSTP2',
                    subjectName: 'National Service Training Program 2',
                    units: 3,
                    finalGrade: '1.00',
                    prerequisites: 'NSTP1',
                    corequisites: 'None'
                  }
                ]
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
                    finalGrade: '2.00',
                    prerequisites: 'MATH102',
                    corequisites: 'None'
                  },
                  {
                    subjectCode: 'PHYS201',
                    subjectName: 'Engineering Physics',
                    units: 4,
                    finalGrade: '2.25',
                    prerequisites: 'PHYS101, MATH102',
                    corequisites: 'MATH201'
                  },
                  {
                    subjectCode: 'CS201',
                    subjectName: 'Computer Programming 1',
                    units: 3,
                    finalGrade: '1.50',
                    prerequisites: 'None',
                    corequisites: 'None'
                  },
                  {
                    subjectCode: 'HUM101',
                    subjectName: 'Art Appreciation',
                    units: 3,
                    finalGrade: '1.25',
                    prerequisites: 'None',
                    corequisites: 'None'
                  }
                ]
              },
              {
                semester: 'Second Semester',
                subjects: [
                  {
                    subjectCode: 'MATH202',
                    subjectName: 'Calculus 2',
                    units: 4,
                    finalGrade: '2.25',
                    prerequisites: 'MATH201',
                    corequisites: 'None'
                  },
                  {
                    subjectCode: 'CS202',
                    subjectName: 'Computer Programming 2',
                    units: 3,
                    finalGrade: '1.75',
                    prerequisites: 'CS201',
                    corequisites: 'None'
                  },
                  {
                    subjectCode: 'CHEM201',
                    subjectName: 'General Chemistry',
                    units: 4,
                    finalGrade: '2.00',
                    prerequisites: 'None',
                    corequisites: 'None'
                  },
                  {
                    subjectCode: 'SOCSCI101',
                    subjectName: 'Understanding the Self',
                    units: 3,
                    finalGrade: '1.50',
                    prerequisites: 'None',
                    corequisites: 'None'
                  }
                ]
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
                    subjectCode: 'MATH301',
                    subjectName: 'Differential Equations',
                    units: 3,
                    finalGrade: '2.25',
                    prerequisites: 'MATH202',
                    corequisites: 'None'
                  },
                  {
                    subjectCode: 'CS301',
                    subjectName: 'Data Structures and Algorithms',
                    units: 3,
                    finalGrade: '1.75',
                    prerequisites: 'CS202',
                    corequisites: 'None'
                  },
                  {
                    subjectCode: 'EE301',
                    subjectName: 'Circuit Theory',
                    units: 4,
                    finalGrade: '2.00',
                    prerequisites: 'PHYS201, MATH202',
                    corequisites: 'None'
                  },
                  {
                    subjectCode: 'ENGG301',
                    subjectName: 'Engineering Economics',
                    units: 3,
                    finalGrade: '1.50',
                    prerequisites: 'MATH201',
                    corequisites: 'None'
                  }
                ]
              },
              {
                semester: 'Second Semester',
                subjects: [
                  {
                    subjectCode: 'CS302',
                    subjectName: 'Database Systems',
                    units: 3,
                    finalGrade: '1.75',
                    prerequisites: 'CS301',
                    corequisites: 'None'
                  },
                  {
                    subjectCode: 'EE302',
                    subjectName: 'Electronics',
                    units: 4,
                    finalGrade: '2.25',
                    prerequisites: 'EE301',
                    corequisites: 'None'
                  },
                  {
                    subjectCode: 'ENGG302',
                    subjectName: 'Engineering Management',
                    units: 3,
                    finalGrade: '1.50',
                    prerequisites: 'ENGG301',
                    corequisites: 'None'
                  },
                  {
                    subjectCode: 'MATH302',
                    subjectName: 'Probability and Statistics',
                    units: 3,
                    finalGrade: '2.00',
                    prerequisites: 'MATH202',
                    corequisites: 'None'
                  }
                ]
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
                    subjectName: 'Operating Systems',
                    units: 3,
                    finalGrade: '2.00',
                    prerequisites: 'CS302',
                    corequisites: 'None'
                  },
                  {
                    subjectCode: 'CS402',
                    subjectName: 'Computer Networks',
                    units: 3,
                    finalGrade: '1.75',
                    prerequisites: 'CS302',
                    corequisites: 'None'
                  },
                  {
                    subjectCode: 'CS403',
                    subjectName: 'Software Engineering',
                    units: 3,
                    finalGrade: '1.50',
                    prerequisites: 'CS302',
                    corequisites: 'None'
                  },
                  {
                    subjectCode: 'ITE192',
                    subjectName: 'Capstone 1',
                    units: 3,
                    finalGrade: '1.25',
                    prerequisites: 'None',
                    corequisites: 'None'
                  }
                ]
              },
              {
                semester: 'Second Semester',
                subjects: [
                  {
                    subjectCode: 'CS404',
                    subjectName: 'Artificial Intelligence',
                    units: 3,
                    finalGrade: '1.75',
                    prerequisites: 'CS301',
                    corequisites: 'None'
                  },
                  {
                    subjectCode: 'CS405',
                    subjectName: 'Web Development',
                    units: 3,
                    finalGrade: '1.50',
                    prerequisites: 'CS302',
                    corequisites: 'None'
                  },
                  {
                    subjectCode: 'CS406',
                    subjectName: 'Mobile Application Development',
                    units: 3,
                    finalGrade: '1.25',
                    prerequisites: 'CS302',
                    corequisites: 'None'
                  },
                  {
                    subjectCode: 'ENGG402',
                    subjectName: 'Capstone 2',
                    units: 3,
                    finalGrade: '1.00',
                    prerequisites: 'ITE192',
                    corequisites: 'None'
                  }
                ]
              }
            ]
          }
        ],
        overallSummary: {
          totalUnits: 160,
          gwa: '1.72'
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .prospectus {
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
    table-layout: fixed;
}
.semester th, .semester td {
  padding: 12px;
  border-bottom: 1px solid #eee;
  vertical-align: middle;
}

.semester th {
  background: #f7f7f7;
  font-weight: 600;
  color: #333;
  border-bottom: 2px solid #eee;
  text-align: left;
}

.semester td {
  color: #444;
  text-align: left;
}
  
  .semester tr:nth-child(even) {
    background: #f9f9f9;
  }
  
  .semester tr:hover {
    background: #f4f4f4;
  }
  /* Column width adjustments */
.semester th:nth-child(1), .semester td:nth-child(1) { /* Subject Code */
  width: 12%;
}
.semester th:nth-child(2), .semester td:nth-child(2) { /* Subject Name */
  width: 28%;
}
.semester th:nth-child(3), .semester td:nth-child(3) { /* Units */
  width: 8%;
}
.semester th:nth-child(4), .semester td:nth-child(4) { /* Final Grade */
  width: 10%;
}
.semester th:nth-child(5), .semester td:nth-child(5) { /* Prerequisites */
  width: 22%;
}
.semester th:nth-child(6), .semester td:nth-child(6) { /* Corequisites */
  width: 20%;
}

.overall-summary {
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 2px solid #eee;
}

.overall-summary h3 {
  color: #333;
  margin: 0 0 1rem 0;
  font-size: 1.25rem;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.summary-row:last-child {
  margin-bottom: 0;
}

@media (max-width: 768px) {
  .prospectus {
    padding: 16px;
  }
  
  .academic-year h3,
  .semester h4 {
    font-size: 1rem;
  }
  
  .semester table {
    font-size: 0.85rem;
  }
  
  .semester th, 
  .semester td {
    padding: 8px;
  }
  
  /* Adjust column widths for mobile */
  .semester th:nth-child(1), .semester td:nth-child(1) { width: 15%; }
  .semester th:nth-child(2), .semester td:nth-child(2) { width: 25%; }
  .semester th:nth-child(5), .semester td:nth-child(5),
  .semester th:nth-child(6), .semester td:nth-child(6) { 
    width: 17.5%; 
    font-size: 0.8rem;
    padding-left: 5px;
  }
  
  .summary-row {
    font-size: 0.9rem;
  }
  }
  </style>  