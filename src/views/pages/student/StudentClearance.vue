<template>
  <div class="clearance-container">
    <div class="clearance-header">
      <h2>My Clearance</h2>
    </div>

    <div class="clearance-body">
      <div class="department-section" v-for="department in departments" :key="department.id">


        <div class="department-body">
          <div class="requirements-list" v-if="department.requirements && department.requirements.length > 0">
            <div v-for="(requirement, index) in department.requirements" :key="index" class="requirement-item">
              <span class="requirement-name">{{ requirement.description }}</span>
              <span class="requirement-status"
                :class="{ 'cleared': requirement.cleared, 'pending': !requirement.cleared }">
                {{ requirement.cleared ? 'Cleared' : 'Pending' }}
              </span>
            </div>
          </div>

          <div class="approval-info" v-if="department.status === 'Approved'">
            <div class="approval-detail">
              <span class="detail-label">Approved By:</span>
              <span class="detail-value">{{ department.approvedBy || 'Dean of Student Affairs' }}</span>
            </div>
            <div class="approval-detail">
              <span class="detail-label">Title:</span>
              <span class="detail-value">{{ department.approvedTitle }}</span>
            </div>
            <div class="approval-detail">
              <span class="detail-label">Date Approved:</span>
              <span class="detail-value">{{ formatDate(department.approvedDate) || 'N/A' }}</span>
            </div>
          </div>

          <div class="pending-message" v-else>
            <p>Your clearance is pending, and needs approval from the DSA (Dean of Student Affairs).</p>
          </div>
        </div>
      </div>
    </div>

    <div class="clearance-footer">
      <div class="overall-status">
        <span>Clearance Status:</span>
        <span class="status-badge" :class="allApproved ? 'approved' : 'pending'">
          {{ allApproved ? 'CLEARED' : 'PENDING' }}
        </span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StudentClearance',
  data() {
    return {
      student: {
        name: "Juan Dela Cruz",
        id: "2020-12345",
        course: "Bachelor of Science in Computer Science",
        yearLevel: "4th Year"
      },
      departments: [
        {
          id: 'dsa',

          name: 'Office',
          status: 'Pending', // This should come from DSA portal
          approvedBy: '',
          approvedTitle: 'Dean of Student Affairs',
          approvedDate: null,
          requirements: [
            { description: 'Registrar', pending: true },
            { description: 'Cashier', pending: true },
            { description: 'Guidance', pending: true },
            { description: 'Library', pending: true },
            { description: 'Clinic', pending: true },
            { description: 'Canteen Fee', pending: true },
            { description: 'Enrollment Fee', pending: true },
            { description: 'Student Council Treasurer', pending: true },
            { description: 'OSAS Staff', pending: true },
            { description: 'OSAS Director', pending: true },
          ]
        },
      ]
    }
  },
  computed: {
    allApproved() {
      return this.departments.every(dept => dept.status === 'Approved');
    }
  },
  methods: {
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
    },
    fetchClearanceStatus() {
      // This method should fetch the clearance status from the DSA portal API
      // Example:
      // this.$http.get('/api/dsa/clearance-status').then(response => {
      //   this.departments = response.data.departments;
      // });
    }
  },
  mounted() {
    this.fetchClearanceStatus();
  }
}
</script>

<style scoped>
.clearance-container {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  width: 100%;
  margin: 0 auto;
}

.clearance-header h2 {
  margin: 0 0 10px 0;
  color: #333;
  text-align: start;
}

.student-info {
  display: flex;
  justify-content: space-between;
  width: 70%;
  margin: 10px auto;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
  box-shadow: 0 2px 2px rgba(0, 0, 0, 0.05);
}

.info-column {
  margin: 10px 0;
  display: flex;
  margin-left: 20px;
}

.left-column {
  text-align: left;
}

.right-column {
  text-align: right;

}

.info-row1,
.info-row2 {
  margin: 10px 0;
  display: flex;
  gap: 10px;
}

.info-row1 {
  margin-left: 10px;
}

.info-row2 {
  margin-right: 10px;
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
  border-bottom: 1px solid #eee;
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
  border-color: #c3e6cb;
}

.department-body {
  padding: 12px;
}

.requirements-list {
  padding: 12px;
}

.requirement-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
}

.requirement-item:last-child {
  border-bottom: none;
}

.requirement-name {
  color: #333;
  font-size: 0.9rem;
}

.requirement-status {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 500;
}

.requirement-status.cleared {
  background-color: #d4edda;
  color: #155724;
  border-color: #c3e6cb;
}

.requirement-status.pending {
  background-color: #fff3cd;
  color: #856404;
  border-color: #fcefc2;
}

.approval-info {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.approval-detail {
  display: flex;
  flex-direction: column;
}

.detail-label {
  font-weight: 600;
  color: #555;
  font-size: 0.9rem;
}

.detail-value {
  color: #333;
  margin-top: 4px;
}

.pending-message {
  padding: 12px;
  background-color: #f8f9fa;
  border-radius: 4px;
  color: #555;
}

.pending-message p {
  margin: 0;
}

.clearance-footer {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
}

.overall-status {
  display: flex;
  align-items: center;
  gap: 8px;
  text-align: center;
}

.status-badge {
  padding: 6px 12px;
  border-radius: 4px;
  font-weight: bold;
  text-transform: uppercase;
  font-size: 0.9rem;
}

.status-badge.pending {
  background-color: #fff3cd;
  color: #856404;
  border-color: #fcefc2;
}

.status-badge.approved {
  background-color: #d4edda;
  color: #155724;
  border-color: #c3e6cb;
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

.clearance-body {
  width: 70%;
  margin: 0 auto;
  padding: 16px 0;
}

.department-section {
  margin-bottom: 24px;
  /* Example value */
}

@media (max-width: 768px) {
  .student-info {
    display: flex;
    flex-direction: column;
  }

  .info-column {
    padding: 0;
    margin-bottom: 20px;
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

  .approval-info {
    grid-template-columns: 1fr;
  }

  .office {
    margin-bottom: 10px;
  }
}
</style>