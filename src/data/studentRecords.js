// src/data/studentRecords.js
export const studentRecords = [
  {
    year: 'First Year',
    schoolYear: '2023-2024',
    semesters: [
      {
        semester: 'First Semester',
        subjects: [
          { subjectCode: 'IT101', subjectName: 'Introduction to Computing', units: 3, finalGrade: '1.75', status: 'Passed', remarks: '-' },
          // ...other subjects
        ],
        totalUnits: 17,
        gpa: '1.63'
      },
      // ...other semesters
    ]
  },
  // ...Second Year, Third Year, Fourth Year
];