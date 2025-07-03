<template>
    <div class="office-clearance-container">
      <div class="clearance-header">
        <h2>{{ officeName }} Clearance Approval</h2>
        <div class="office-info">
          <div class="info-row">
            <span class="label">Office:</span>
            <span class="value">{{ officeName }}</span>
          </div>
          <div class="info-row">
            <span class="label">Approver:</span>
            <span class="value">{{ approverName }}</span>
          </div>
        </div>
      </div>
  
      <div class="student-info-section">
        <h3>Student Information</h3>
        <div class="student-info">
          <div class="info-row">
            <span class="label">Student Name:</span>
            <span class="value">{{ student.lastName }}, {{ student.firstName }}</span>
          </div>
          <div class="info-row">
            <span class="label">Student ID:</span>
            <span class="value">{{ student.id }}</span>
          </div>
          <div class="info-row">
            <span class="label">Course:</span>
            <span class="value">{{ student.course }}</span>
          </div>
          <div class="info-row">
            <span class="label">Year Level:</span>
            <span class="value">{{ getYearLabel(student.yearLevel) }}</span>
          </div>
        </div>
      </div>
  
      <div class="clearance-body">
        <div class="requirements-section">
          <h3>Requirements</h3>
          <div class="requirements-list">
            <div v-for="(requirement, index) in requirements" :key="index" class="requirement-item">
              <input 
                type="checkbox" 
                :id="`req-${index}`"
                v-model="requirement.cleared"
                :disabled="isApproved"
              >
              <label :for="`req-${index}`">{{ requirement.description }}</label>
            </div>
          </div>
        </div>
  
        <div class="approval-section" v-if="!isApproved">
          <div class="approver-input">
            <label for="approver-name">Approver Name:</label>
            <input 
              type="text" 
              id="approver-name"
              v-model="approverName"
              placeholder="Enter your name"
            >
          </div>
          <div class="approver-input">
            <label for="approver-title">Title:</label>
            <input 
              type="text" 
              id="approver-title"
              v-model="approverTitle"
              :placeholder="defaultTitle"
            >
          </div>
          <button 
            class="approve-btn"
            @click="approveClearance"
            :disabled="!canApprove"
          >
            Approve Clearance
          </button>
        </div>
  
        <div class="approval-details" v-else>
          <h3>Approval Details</h3>
          <div class="detail-item">
            <span class="detail-label">Status:</span>
            <span class="detail-value approved">Approved</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">Approved By:</span>
            <span class="detail-value">{{ approverName }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">Title:</span>
            <span class="detail-value">{{ approverTitle }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">Date Approved:</span>
            <span class="detail-value">{{ formatDate(approvalDate) }}</span>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import Button from 'primevue/button';
  export default {
    name: 'OfficeClearance',
    components: {
      Button
    },
    props: {
      student: {
        type: Object,
        required: true
      },
      officeType: {
        type: String,
        required: true
      },
      approverName: {
        type: String,
        default: 'Office Staff'
      },
      approverTitle: {
        type: String,
        default: 'Office Staff'
      }
    },
    data() {
      return {
        requirements: [],
        isApproved: false,
        approvalDate: null,
        officeTypes: {
          'cashier': 'Cashier Office',
          'library': 'Library',
          'clinic': 'Clinic',
          'guidance': 'Guidance Office',
          'canteen': 'Canteen',
          'student-council': 'Student Council',
          'osas-staff': 'OSAS Staff',
          'osas-director': 'OSAS Director'
        }
      };
    },
    computed: {
      officeName() {
        return this.officeTypes[this.officeType] || 'Office';
      },
      defaultTitle() {
        return `${this.officeName} Staff`;
      },
      canApprove() {
        return this.requirements.length > 0 && 
               this.requirements.every(req => req.cleared) && 
               !this.isApproved;
      }
    },
    created() {
      this.requirements = this.getOfficeRequirements();
    },
    methods: {
      async approveClearance() {
        try {
          // In a real app, you would make an API call here
          // const response = await this.$http.post('/api/clearance/approve', {
          //   studentId: this.student.id,
          //   office: this.officeType,
          //   approverName: this.approverName,
          //   approverTitle: this.approverTitle
          // });
          
          // Simulate API call
          await new Promise(resolve => setTimeout(resolve, 500));
          
          this.approvalDate = new Date();
          this.isApproved = true;
          this.$emit('approved');
          this.$toast.add({
            severity: 'success',
            summary: 'Success',
            detail: 'Clearance approved successfully',
            life: 3000
          });
        } catch (error) {
          console.error('Approval failed:', error);
          this.$toast.add({
            severity: 'error',
            summary: 'Error',
            detail: 'Failed to submit approval. Please try again.',
            life: 3000
          });
        }
      },
      getYearLabel(year) {
        const labels = {
          1: '1st Year',
          2: '2nd Year',
          3: '3rd Year',
          4: '4th Year'
        };
        return labels[year] || year;
      },
      getOfficeRequirements() {
        // Default requirements that can be overridden by specific offices
        const defaultRequirements = [
          { description: 'All documents submitted', cleared: false },
          { description: 'No pending obligations', cleared: false },
          { description: 'Clearance form signed', cleared: false }
        ];

        // Office-specific requirements
        const officeRequirements = {
          'cashier': [
            { description: 'All fees paid', cleared: false },
            { description: 'No outstanding balance', cleared: false },
            { description: 'Payment receipts submitted', cleared: false }
          ],
          'library': [
            { description: 'All books returned', cleared: false },
            { description: 'No pending fines', cleared: false },
            { description: 'Library card cleared', cleared: false }
          ],
          'clinic': [
            { description: 'Medical clearance submitted', cleared: false },
            { description: 'Health records updated', cleared: false },
            { description: 'No pending medical requirements', cleared: false }
          ]
        };

        return officeRequirements[this.officeType] || defaultRequirements;
      },
      formatDate(date) {
        if (!date) return '';
        const options = { 
          year: 'numeric', 
          month: 'long', 
          day: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
        };
        return new Date(date).toLocaleDateString('en-US', options);
      }
    }
  }
  </script>
  
  <style scoped>
  .office-clearance-container {
    padding: 1.5rem;
    max-width: 800px;
    margin: 0 auto;
  }
  
  .clearance-header {
    margin-bottom: 2rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid #e5e7eb;
  }
  
  .office-info {
    background-color: #f9fafb;
    padding: 1rem;
    border-radius: 0.5rem;
    margin-top: 1rem;
  }
  
  .info-row {
    display: flex;
    margin-bottom: 0.5rem;
  }
  
  .info-row .label {
    font-weight: 600;
    min-width: 120px;
    color: #4b5563;
  }
  
  .student-info-section {
    margin-bottom: 2rem;
    padding: 1.5rem;
    background-color: #ffffff;
    border-radius: 0.5rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  }
  
  .requirements-section {
    margin-bottom: 2rem;
    padding: 1.5rem;
    background-color: #ffffff;
    border-radius: 0.5rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  }
  
  .requirements-list {
    margin-top: 1rem;
  }
  
  .requirement-item {
    display: flex;
    align-items: center;
    padding: 0.75rem 0;
    border-bottom: 1px solid #e5e7eb;
  }
  
  .requirement-item:last-child {
    border-bottom: none;
  }
  
  .requirement-item input[type="checkbox"] {
    margin-right: 0.75rem;
  }
  
  .requirement-item label {
    cursor: pointer;
    user-select: none;
  }
  
  .actions {
    display: flex;
    justify-content: flex-end;
    margin-top: 1.5rem;
  }
  
  .approval-section {
    margin-top: 2rem;
    padding: 1.5rem;
    background-color: #f0fdf4;
    border-radius: 0.5rem;
    border: 1px solid #bbf7d0;
  }
  
  .approval-details {
    margin-top: 1rem;
    padding: 1rem;
    background-color: #ffffff;
    border-radius: 0.25rem;
    border: 1px solid #e5e7eb;
  }
  
  .approved-badge {
    display: inline-flex;
    align-items: center;
    padding: 0.25rem 0.75rem;
    background-color: #dcfce7;
    color: #166534;
    border-radius: 9999px;
    font-size: 0.875rem;
    font-weight: 500;
  }
  
  .approved-badge i {
    margin-right: 0.5rem;
  }
  
  button {
    padding: 0.5rem 1rem;
    background-color: #3b82f6;
    color: white;
    border: none;
    border-radius: 0.375rem;
    cursor: pointer;
    font-weight: 500;
    transition: background-color 0.2s;
  }
  
  button:hover {
    background-color: #2563eb;
  }
  
  button:disabled {
    background-color: #9ca3af;
    cursor: not-allowed;
  }
  
  .back-btn {
    background-color: #6b7280;
    margin-bottom: 1rem;
  }
  
  .back-btn:hover {
    background-color: #4b5563;
  }
  </style>