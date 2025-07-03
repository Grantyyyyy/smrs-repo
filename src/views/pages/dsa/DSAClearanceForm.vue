<template>
  <div class="student-info">
    <div class="grid">
      <div class="col-12 md-col-6">
        <div class="field">
          <label>Student Name</label>
          <InputText type="text" :value="`${student.lastName}, ${student.firstName}`" class="w-full" readonly />
        </div>
      </div>
      <div class="col-12 md-col-6">
        <div class="field">
          <label>Student ID</label>
          <InputText type="text" :value="student.id" class="w-full" readonly />
        </div>
      </div>
      <div class="col-12 md-col-6">
        <div class="field">
          <label>Course</label>
          <InputText type="text" :value="student.course" class="w-full" readonly />
        </div>
      </div>
      <div class="col-12 md-col-6">
        <div class="field">
          <label>Year Level</label>
          <InputText 
            type="text" 
            :value="getYearLevelText(student.yearLevel)" 
            class="w-full year-level" 
            readonly 
          />
        </div>
      </div>
    </div>
  </div>

  <div class="clearance-body">
    <div class="department-section" v-for="department in departments" :key="department.id">


      <div class="department-body">
        <div class="requirements" v-if="department.requirements.length > 0">
          <div class="requirement" v-for="(req, index) in department.requirements" :key="index">
            <span class="requirement-text">{{ req.description }}</span>
            <span class="requirement-status" :class="{ 'cleared': req.cleared }">
              {{ req.cleared ? '✓ Approved' : 'Pending' }}
            </span>
          </div>
        </div>

        <div v-if="!isEditing || currentDepartmentId !== department.id" class="status-view">
          <div v-if="department.requirements[0]?.cleared" class="success-message">
            <i class="pi pi-check-circle"></i>
            <span>Clearance has been submitted and is pending for approval.</span>
          </div>
          <Button 
            v-else
            label="Edit Status" 
            icon="pi pi-pencil" 
            class="edit-status-button"
            @click="startEditing(department.id)"
          />
        </div>

        <div v-else class="edit-form">
          <div class="field">
            <label>Status</label>
            <Dropdown 
              v-model="editedStatus" 
              :options="statusOptions" 
              optionLabel="label"
              optionValue="value"
              class="status-dropdown w-full"
            />
          </div>
          <div class="field">
            <label>Remarks</label>
            <Textarea 
              v-model="remarks" 
              :autoResize="true" 
              rows="3" 
              class="w-full"
              placeholder="Enter any remarks or notes about this clearance"
            />
          </div>
          <div class="form-actions">
            <Button 
              label="Cancel" 
              icon="pi pi-times" 
              class="p-button-danger cancel-button"
              @click="cancelEditing"
            />
            <Button 
              label="Save" 
              icon="pi pi-check" 
              class="p-button-success save-button"
              @click="saveStatus"
            />
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="clearance-footer">
    <div class="overall-status">
      <span>Clearance Status:</span>
      <span class="status-badge" :class="{ 'approved': allApproved, 'pending': !allApproved }">
        {{ allApproved ? 'APPROVED' : 'PENDING' }}
      </span>
    </div>
    <button v-if="allApproved" class="submit-btn" @click="submitClearance">
      Submit Clearance
    </button>
  </div>
</template>

<script>
import { ref, reactive } from 'vue';

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
      isEditing: false,
      currentDepartmentId: null,
      remarks: '',
      editedStatus: 'pending',
      requirements: [
        {
          description: 'Canteen Fee',
          cleared: this.student ? this.student.clearanceStatus === 'Approved' : false
        }
      ],
      statusOptions: [
        { label: 'Pending', value: 'pending' },
        { label: 'Approved', value: 'approved' }
      ],
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
            { description: 'Canteen Fee', cleared: this.student ? this.student.clearanceStatus === 'Approved' : false },
            { description: 'Enrollment Fee', cleared: false },
            { description: 'Student Council Treasurer', cleared: false },
            { description: 'OSAS Staff', cleared: false },
            { description: 'OSAS Director', cleared: false },
          ]
        }
      ]
    }
  },

  watch: {
    'student.clearanceStatus': function(newStatus) {
      if (typeof newStatus !== 'undefined') {
        const isApproved = (newStatus === 'Approved');
        this.requirements[0].cleared = isApproved;
        if (this.isEditing) {
          this.editedStatus = isApproved ? 'approved' : 'pending';
        }
      }
    }
  },
  computed: {
    allApproved() {
      return this.requirements.every(req => req.cleared);
    }
  },
  methods: {
    getYearLevelText(yearLevel) {
      const levels = ['1st Year', '2nd Year', '3rd Year', '4th Year']
      return levels[yearLevel - 1] || `Year ${yearLevel}`
    },
    
    startEditing(departmentId) {
      this.currentDepartmentId = departmentId;
      const department = this.departments.find(d => d.id === departmentId);
      if (department) {
        this.editedStatus = department.requirements[0]?.cleared ? 'approved' : 'pending';
        this.remarks = department.remarks || '';
        this.isEditing = true;
      }
    },
    
    cancelEditing() {
      this.isEditing = false;
      this.currentDepartmentId = null;
    },
    
    saveStatus() {
      console.log('Saving status:', this.editedStatus); 
      const isApproved = this.editedStatus === 'approved';
      
      if (this.currentDepartmentId) {
        // Update the specific department's requirements
        this.departments = this.departments.map(department => {
          if (department.id === this.currentDepartmentId) {
            const updatedRequirements = department.requirements.map(req => ({
              ...req,
              cleared: isApproved
            }));
            
            return {
              ...department,
              requirements: updatedRequirements,
              remarks: this.remarks
            };
          }
          return department;
        });
        
        // Also update the main requirements array if needed
        if (this.requirements.length > 0) {
          this.requirements[0].cleared = isApproved;
        }
        
        this.isEditing = false;
        this.currentDepartmentId = null;
        
        // Force update to ensure UI reflects the changes
        this.$forceUpdate();

        this.$emit('clearance-updated', {
          studentId: this.student.id,
          cleared: isApproved,
          remarks: this.remarks
        });
      }
    },
    
    async submitClearance() {
      try {
        // Check if all requirements are approved
        const allApproved = this.departments.every(dept => 
          dept.requirements.every(req => req.cleared)
        );

        if (!allApproved) {
          this.$toast.add({
            severity: 'warn',
            summary: 'Cannot Submit',
            detail: 'Please approve all requirements before submitting clearance.',
            life: 3000
          });
          return;
        }

        // Show loading state
        this.$toast.add({
          severity: 'info',
          summary: 'Submitting',
          detail: 'Submitting clearance to Registrar Portal...',
          life: 3000
        });

        // Prepare submission data
        const submissionData = {
          studentId: this.student.id,
          studentName: `${this.student.lastName}, ${this.student.firstName}`,
          course: this.student.course,
          yearLevel: this.student.yearLevel,
          submissionDate: new Date().toISOString(),
          requirements: this.departments.flatMap(dept => 
            dept.requirements.map(req => ({
              department: dept.name,
              requirement: req.description,
              status: req.cleared ? 'Approved' : 'Pending',
              approvedBy: 'DSA Office',
              approvedDate: new Date().toISOString()
            }))
          )
        };

        // Emit the submit event with all necessary data
        this.$emit('submit-clearance', submissionData);

        // Show success message
        this.$toast.add({
          severity: 'success',
          summary: 'Submitted',
          detail: 'Clearance submitted to Registrar Portal for final approval.',
          life: 5000
        });

        // Emit close-dialog event to notify parent to close the dialog
        this.$emit('close-dialog');

      } catch (error) {
        console.error('Error submitting clearance:', error);
        this.$toast.add({
          severity: 'error',
          summary: 'Submission Failed',
          detail: 'There was an error submitting the clearance. Please try again.',
          life: 5000
        });
      }
    }
  }
}
</script>

<style scoped>
.student-info {
  padding: 1rem;
  margin-bottom: 1rem;
  border-radius: 6px;
  background-color: #f8f9fa;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.field {
  margin-bottom: 0.5rem;
}

.field label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #4a5563;
}

.clearance-body {
  margin: 20px 0;
}

.department-section {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.department-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background-color: #f9fafb;
}

.department-header h3 {
  font-size: 15px;
  font-weight: 600;
  color: #111827;
}

.status {
  font-size: 13px;
  font-weight: 500;
  padding: 4px 10px;
  border-radius: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status.pending {
  background-color: #fef3c7;
  color: #92400e;
  border-radius: 4px;
}

.status.approved {
  background-color: #dcfce7;
  color: #166534;
  border-radius: 4px;
}

.department-body {
  padding: 16px;
}

.requirement {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid #f3f4f6;
  align-items: center;
}

.requirement:last-child {
  border-bottom: none;
}

.requirement-text {
  color: #374151;
  font-size: 14px;
}

.requirement-status {
  font-size: 13px;
  font-weight: 500;
  padding: 3px 8px;
  border-radius: 4px;
  background-color: #fff3cd;
  color: #856404;
  border-color: #fcefc2;
}

.requirement-status.cleared {
  background-color: #d4edda;
  color: #155724;
  border-color: #c3e6cb;
}

.clearance-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.overall-status {
  display: flex;
  align-items: center;
  gap: 10px;
}

.overall-status span:first-child {
  color: #4b5563;
  font-size: 14px;
}

.status-badge {
  font-weight: 600;
  font-size: 12px;
  padding: 4px 10px;
  border-radius: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-badge.pending {
  background-color: #fff3cd;
  color: #856404;
  border-color: #fcefc2;
  border-radius: 4px;
}

.status-badge.approved {
  background-color: #d4edda;
  color: #155724;
  border-color: #c3e6cb;
  border-radius: 4px;
}

.submit-btn {
  background-color: #10b981;
  color: white;
  padding: 8px 16px;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  font-size: 14px;
  margin-left: auto;
  display: block;
  position: relative;
  top: 0;
}

.submit-btn:hover {
  background-color: #0d9f6e;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.status-view {
  margin-top: 1rem;
  text-align: center;
}

.edit-form {
  max-width: 400px;
  margin: 1rem auto 0;
  padding: 1.25rem;
  background-color: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.edit-form .field {
  margin-bottom: 1.5rem;
  width: 100%;
}

.edit-form .field label {
  display: block;
  font-weight: 500;
  color: var(--text-color);
}

.form-actions {
  display: flex;
  gap: 80px;
  justify-content: center;
  align-items: center;
}

.status-dropdown {
  width: 100%;
}

.success-message {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  color: #15803d;
  background-color: #f0fdf4;
  padding: 0.75rem;
  border-radius: 6px;
  margin: 0.5rem 0;
  font-size: 0.875rem;
}

.success-message i {
  font-size: 1.25rem;
}

.edit-status-button {
  margin-top: 1rem;
  background-color: #10b981;
  color: white;
  border: 1px solid #bbf7d0;
  width: 100%;
  max-width: 200px;
  padding: 0.5rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s, border-color 0.2s, box-shadow 0.2s;
  position: relative;
  top: 0;
}

.edit-status-button:hover {
  background-color: #0d9f6e;
  border-color: #0d9f6e;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.cancel-button {
  background-color: #c74848;
  color: white;
  border: 1px solid #fecaca;
  transition: background-color 0.2s, border-color 0.2s, box-shadow 0.2s;
}

.cancel-button:hover {
  background-color: #dc2626;
  color: white;
  border-color: #dc2626;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.save-button {
  background-color: #10b981;
  color: white;
  border: 1px solid #bbf7d0;
  transition: background-color 0.2s, border-color 0.2s, box-shadow 0.2s;
}

.save-button:hover {
  background-color: #0d9f6e;
  color: white;
  border-color: #0d9f6e;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

@media (max-width: 768px) {
  .form-actions {
    flex-direction: column;
  }
  
  .form-actions button {
    width: 100%;
  }
}
</style>
