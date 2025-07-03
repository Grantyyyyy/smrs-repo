<template>
  <div class="clearance-form">
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

    <div class="clearance-status">
      <h5 class="status-title">Canteen Clearance Status</h5>
      
      <div v-if="!isEditing" class="status-view">
        <div class="status-chip">
          <Chip 
            :label="requirements[0].cleared ? 'Cleared' : 'Pending'" 
            :class="{'status-cleared': requirements[0].cleared, 'status-pending': !requirements[0].cleared}"
          />
        </div>
        <div v-if="requirements[0].cleared" class="success-message">
          <i class="pi pi-check-circle"></i>
          <span>Clearance has been submitted to DSA and is pending for approval.</span>
        </div>
        <Button 
          v-else
          label="Edit Status" 
          icon="pi pi-pencil" 
          class="edit-button"
          @click="startEditing"
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
            class="status-dropdown"
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
            class="cancel-button"
            @click="cancelEditing"
          />
          <Button 
            label="Save" 
            icon="pi pi-check" 
            class="save-button"
            @click="saveStatus"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    student: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      isEditing: false,
      editedStatus: this.student ? (this.student.clearanceStatus === 'Cleared' ? 'cleared' : 'pending') : 'pending',
      requirements: [
        {
          description: 'Canteen Fee',
          cleared: this.student ? this.student.clearanceStatus === 'Cleared' : false
        }
      ],
      statusOptions: [
        { label: 'Pending', value: 'pending' },
        { label: 'Cleared', value: 'cleared' }
      ]
    };
  },
  watch: {
    'student.clearanceStatus': function(newStatus) {
      if (typeof newStatus !== 'undefined') {
        this.requirements[0].cleared = (newStatus === 'Cleared');
        if (this.isEditing) {
          this.editedStatus = this.requirements[0].cleared ? 'cleared' : 'pending';
        }
      }
    }
  },
  methods: {
    getYearLevelText(yearLevel) {
      const levels = ['1st Year', '2nd Year', '3rd Year', '4th Year']
      return levels[yearLevel - 1] || `Year ${yearLevel}`
    },
    startEditing() {
      this.editedStatus = this.requirements[0].cleared ? 'cleared' : 'pending'
      this.isEditing = true
    },
    cancelEditing() {
      this.isEditing = false;
    },
    saveStatus() {
      console.log('Saving status:', this.editedStatus); 
      const isCleared = this.editedStatus === 'cleared';
      this.requirements[0].cleared = isCleared; 
      this.isEditing = false; 

      // Emit the clearance-updated event first
      this.$emit('clearance-updated', {
        studentId: this.student.id,
        cleared: isCleared,
        remarks: this.remarks
      });
      
      // Use nextTick to ensure the parent has processed the clearance-updated event
      this.$nextTick(() => {
        // Emit close-dialog event to close the dialog
        this.$emit('close-dialog');
      });
    }
  }
}
</script>

<style scoped>
.clearance-form {
  display: flex;
  flex-direction: column;
  width: 100%;
  min-width: 200px;
  max-width: 600px;
  margin: auto;
}

.student-info {
  padding: 1rem;
  margin-bottom: 1.5rem;
  border-radius: 6px;
  background-color: #f8f9fa;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.clearance-status {
  padding: 1rem;
  border-radius: 6px;
  background-color: #f8f9fa;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  justify-content: center;
}

.status-title {
  display: flex;
  justify-content: center;
  margin-bottom: 1rem;
  color: var(--text-color);
  font-size: 1.25rem;
  font-weight: 600;
}

.field {
  margin-bottom: 1rem;
}

.field label {
  display: block;
  font-weight: 500;
  margin-bottom: 0.5rem;
}

.status-view {
  text-align: center;
}

.status-chip {
  margin-bottom: 1rem;
  border-radius: 4px;
}

:deep(.p-chip) {
  font-size: 1.1rem;
  padding: 0.5rem 1.5rem;
}

.status-cleared {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
  border-radius: 6px;
}

.status-pending {
  background-color: #fff3cd;
  color: #856404;
  border: 1px solid #fcefc2;
  border-radius: 6px;
}

.edit-button,
.save-button {
  background-color: #10b981;
  color: white;
  border: 1px solid #bbf7d0;
}

.edit-button:hover,
.save-button:hover {
  background-color: #0d9f6e;
  color: white;
  border-color: #0d9f6e;
}

.cancel-button {
  background-color: #c74848;  
  color: white;
  border: 1px solid #fecaca;
}

.cancel-button:hover {
  background-color: #dc2626;
  color: white;
  border-color: #dc2626;
}

.edit-form {
  max-width: 300px;
  margin: 0 auto;
}

.edit-form .field {
  margin-bottom: 1.5rem;
  width: 100%;
  border-color: #dc2626;

}

.edit-form .field label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--text-color);
}

.status-dropdown {
  width: 100%;
}

.status-dropdown .p-dropdown {
  width: 100%;
}

.status-dropdown .p-dropdown-label {
  text-align: left;
  padding: 0.5rem 0.75rem;
}

.form-actions {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
}

.success-message {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin: 1rem 0;
  padding: 0.75rem 1rem;
  background-color: #e8f5e9;
  color: #1b5e20;
  border-radius: 6px;
  font-size: 0.9rem;
}

.success-message i {
  font-size: 1.2rem;
}

.p-textarea {
  margin-bottom: 1rem;
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