<template>
    <div class="clearance-header">
      <div class="student-info">
        <div class="">
        <div class="info-row1">
          <span class="label">Student Name:</span>
          <span class="value">{{ student.lastName }}, {{ student.firstName }}</span>
        </div>
        <div class="info-row1">
          <span class="label">Student ID:</span>
          <span class="value">{{ student.id }}</span>
        </div>
        </div>

        <div class="">
        <div class="info-row2">
          <span class="label">Course:</span>
          <span class="value">{{ student.course }}</span>
        </div>
        <div class="info-row2">
          <span class="label">Year Level:</span>
          <span class="value">
            <span v-if="student.yearLevel === 1">1st Year</span>
            <span v-else-if="student.yearLevel === 2">2nd Year</span>
            <span v-else-if="student.yearLevel === 3">3rd Year</span>
            <span v-else-if="student.yearLevel === 4">4th Year</span>
            <span v-else>{{ student.yearLevel }}</span>
          </span>
        </div>
        </div>
      </div>

    <div class="clearance-body">
      <div class="department-section" v-for="department in departments" :key="department.id">
        <div class="department-header">
          <h3>{{ department.name }}</h3>
          <div class="status" :class="{'approved': department.status === 'Approved', 'pending': department.status === 'Pending'}">
            {{ department.status }}
          </div>
        </div>
        
        <div class="department-body">
          <div class="requirements" v-if="department.requirements.length > 0">
            <div class="requirement" v-for="(req, index) in department.requirements" :key="index">
              <span class="requirement-text">{{ req.description }}</span>
              <span class="requirement-status" :class="{'cleared': req.cleared}">
                {{ req.cleared ? '✓ Cleared' : 'Pending' }}
              </span>
            </div>
          </div>
          
          <button 
            v-if="department.status === 'Pending'"
            class="approve-btn"
            @click="approveDepartment(department.id)"
          >
            Approve Clearance
          </button>
          <div v-else class="approved-message">
            ✓ Approved
          </div>
        </div>
      </div>
    </div>

    <div class="clearance-footer">
      <div class="overall-status">
        <span>Clearance Status:</span>
        <span class="status-badge" :class="{'approved': allApproved, 'pending': !allApproved}">
          {{ allApproved ? 'CLEARED' : 'PENDING' }}
        </span>
      </div>
      <button 
        v-if="allApproved" 
        class="submit-btn"
        @click="submitClearance"
      >
        Submit Clearance
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ClearanceForm',
  props: {
    student: {
      type: Object,
      required: true
    }
  },

  data() {
    return {
      selectedYear: '',
      years: ['1st Year', '2nd Year', '3rd Year', '4th Year'],
      departments: [
        {
          id: 'registrar',
          name: 'Office',
          status: 'Pending',
          approvedBy: '',
          approvedTitle: 'Registrar',
          approvedDate: null,
          requirements: [
            { description: 'Registrar', cleared: false },
            { description: 'Cashier', cleared: false },
            { description: 'Guidance', cleared: false },
            { description: 'Library', cleared: false },
            { description: 'Clinic', cleared: false },
            { description: 'Canteen Fee', cleared: false },
            { description: 'Enrollment Fee', cleared: false },
            { description: 'Student Council Treasurer', cleared: false },
            { description: 'OSAS Staff', cleared: false },
            { description: 'OSAS Director', cleared: false },
          ]
        },
      ],
    }
  },

  computed: {
    allApproved() {
      return this.departments.every(dept => dept.status === 'Approved');
    }
  },
  methods: {
    approveDepartment(departmentId) {
      const department = this.departments.find(d => d.id === departmentId);
      if (department) {
        // Mark all requirements as cleared when approving
        department.requirements.forEach(req => {
          req.cleared = true;
        });
        department.status = 'Approved';
        department.approvedDate = new Date();
        // In a real app, this would be an API call to update the status
      }
    },
    formatDate(date) {
      if (!date) return '';
      return date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
      });
    },
    submitClearance() {
      // In a real app, this would submit to the Registrar portal
      alert('Clearance submitted to Registrar portal. Student has been officially cleared.');
      // Here you would typically make an API call to update the registrar's system
      // Example: this.$http.post('/api/clearance/submit', { studentId: this.student.id })
    }
  }
}
</script>

<style scoped>
.clearance-header {
  position: relative;
  width: 100%;
  margin-bottom: 10px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.close-btn {
  background: none;
  border: none;
  color: #6b7280;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  color: #1f2937;
  background-color: #f3f4f6;
}

.close-btn svg {
  width: 20px;
  height: 20px;
}

.clearance-container {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
  width: 90%;
  max-width: 1100px;
  margin: 20px auto;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.clearance-body {
  display: flex;
  flex-direction: column;
  padding: 24px;
  width: 100%;
  max-width: 800px;
}

.student-info {
    display: flex;
    justify-content: space-between;
    width: 70%;
    margin: 20px auto;
    padding: 16px;
    background: #f8f9fa;
    border-radius: 8px;
    box-shadow: 0 2px 2px rgba(0,0,0,0.05);
}

.info-row1, .info-row2 {
  margin: 10px 0;
  display: flex;
  gap: 10px;
}

.info-row1 {
  margin-left: 0;
}

.info-row2 {
  margin-right: 0;
}

.label {
  font-weight: 600;
  color: #555;
}

.value {
  color: #333;
}

.department-section {
  margin-bottom: 10px;
  border: 1px solid #eee;
  border-radius: 8px;
  overflow: hidden;
}

.department-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background-color: #f8f9fa;
}

.department-header h3 {
  margin: 0;
  font-size: 1rem;
  color: #333;
}

.status {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
}

.status.pending {
  background-color: #fff3cd;
  color: #856404;
}

.status.approved {
  background-color: #d4edda;
  color: #155724;
}

.department-body {
  padding: 16px;
  width: 100%;
}

.requirements {
  margin-bottom: 16px;
}

.requirement {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #eee;
}

.requirement-text {
  flex-grow: 1;
}

.requirement-status {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.85em;
  background-color: #fff3cd;
  color: #856404;
}

.requirement-status.cleared {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.approve-btn {
  display: block;
  margin: 16px auto 0;
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.approve-btn:hover {
  background-color: #388e3c;
}

.approved-message {
  color: #2e7d32;
  font-weight: bold;
  margin-top: 12px;
}

.clearance-footer {
  margin-top: 10px;
  padding-top: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
}

.overall-status {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
}

.status-badge {
  padding: 6px 12px;
  border-radius: 4px;
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.9rem;
}

.status-badge.pending {
  background-color: #fff3cd;
  color: #856404;
}

.status-badge.approved {
  background-color: #d4edda;
  color: #155724;
}

.submit-btn {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}

.submit-btn:hover {
  background-color: #45a049;
}

@media (max-width: 768px) {
  .clearance-container {
    padding: 16px;
  }
  
  .student-info {
    grid-template-columns: 1fr;
  }
  
  .department-header {
    flex-direction: column;
    align-items: flex-start;
      gap: 8px;
  }
  
  .clearance-footer {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }
}
</style>