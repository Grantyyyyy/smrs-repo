<template>
    <div class="registrar-dashboard">
      <!-- Header Section -->
      <div class="header-section">
        <div class="header-content">
          <h1><i class="pi pi-id-card"></i> Registrar Clearance Dashboard</h1>
          <p class="subtitle">Monitor and manage student clearance status</p>
        </div>
        <div class="header-actions">
          <Button 
            icon="pi pi-refresh" 
            label="Refresh Data" 
            class="p-button-text p-button-sm" 
            @click="refreshData"
          />
        </div>
      </div>
  
      <!-- Stats Overview -->
      <div class="stats-container">
        <div class="stat-card total">
          <div class="stat-icon"><i class="pi pi-users"></i></div>
          <div class="stat-content">
            <div class="stat-value">{{ totalStudents }}</div>
            <div class="stat-label">Total Students</div>
          </div>
        </div>
        <div class="stat-card pending">
          <div class="stat-icon"><i class="pi pi-clock"></i></div>
          <div class="stat-content">
            <div class="stat-value">{{ pendingClearances }}</div>
            <div class="stat-label">Pending</div>
          </div>
        </div>
        <div class="stat-card approved">
          <div class="stat-icon"><i class="pi pi-check-circle"></i></div>
          <div class="stat-content">
            <div class="stat-value">{{ approvedClearances }}</div>
            <div class="stat-label">Approved</div>
          </div>
        </div>
        <div class="stat-card rejected">
          <div class="stat-icon"><i class="pi pi-times-circle"></i></div>
          <div class="stat-content">
            <div class="stat-value">{{ rejectedClearances }}</div>
            <div class="stat-label">Rejected</div>
          </div>
        </div>
      </div>

      <!-- Main Content -->
      <div class="main-content">
        <!-- Recent Clearances Table -->
        <div class="card table-card">
          <div class="card-header">
            <h3>Recent Clearance Requests</h3>
            <div class="card-actions">
              <Dropdown 
                v-model="selectedTimeRange" 
                :options="timeRangeOptions" 
                optionLabel="name" 
                placeholder="Last 7 Days"
                class="p-column-filter"
              />
            </div>
          </div>
          <DataTable 
            :value="recentClearances" 
            :paginator="true" 
            :rows="5"
            responsiveLayout="scroll"
            class="p-datatable-sm"
          >
            <Column field="studentId" header="Student ID" :sortable="true"></Column>
            <Column field="studentName" header="Student Name" :sortable="true"></Column>
            <Column field="department" header="Department" :sortable="true"></Column>
            <Column field="dateSubmitted" header="Date Submitted" :sortable="true">
              <template #body="{data}">
                {{ formatDate(data.dateSubmitted) }}
              </template>
            </Column>
            <Column field="status" header="Status" :sortable="true">
              <template #body="{data}">
                <Tag :value="data.status" 
                    :severity="getStatusSeverity(data.status)" />
              </template>
            </Column>
            <Column header="Actions" style="width: 120px">
              <template #body="{data}">
                <Button 
                  icon="pi pi-eye" 
                  class="p-button-rounded p-button-text p-button-sm"
                  @click="viewClearanceDetails(data)"
                  v-tooltip.top="'View Details'"
                />
                <Button 
                  v-if="data.status === 'Pending'"
                  icon="pi pi-check" 
                  class="p-button-rounded p-button-text p-button-success p-button-sm"
                  @click="approveClearance(data)"
                  v-tooltip.top="'Approve'"
                />
                <Button 
                  v-if="data.status === 'Pending'"
                  icon="pi pi-times" 
                  class="p-button-rounded p-button-text p-button-danger p-button-sm"
                  @click="rejectClearance(data)"
                  v-tooltip.top="'Reject'"
                />
              </template>
            </Column>
          </DataTable>
        </div>
      </div>

      <!-- Clearance Details Dialog -->
      <Dialog 
        v-model:visible="displayDialog" 
        :header="selectedClearance ? `${selectedClearance.studentName} - Clearance Details` : ''" 
        :modal="true"
        :style="{width: '700px'}"
        :dismissableMask="true"
      >
        <div v-if="selectedClearance" class="clearance-details">
          <div class="grid">
            <div class="col-6">
              <div class="field">
                <label>Student ID:</label>
                <div class="p-text-bold">{{ selectedClearance.studentId }}</div>
              </div>
              <div class="field">
                <label>Department:</label>
                <div>{{ selectedClearance.department }}</div>
              </div>
            </div>
            <div class="col-6">
              <div class="field">
                <label>Date Submitted:</label>
                <div>{{ formatDate(selectedClearance.dateSubmitted) }}</div>
              </div>
              <div class="field">
                <label>Status:</label>
                <div>
                  <Tag :value="selectedClearance.status" 
                      :severity="getStatusSeverity(selectedClearance.status)" />
                </div>
              </div>
            </div>
          </div>
          
          <Divider align="left">
            <div class="inline-flex align-items-center">
              <i class="pi pi-list mr-2"></i>
              <span>Requirements</span>
            </div>
          </Divider>
          
          <div class="requirements-list">
            <div v-for="(req, index) in selectedClearance.requirements" :key="index" class="requirement-item">
              <div class="requirement-name">{{ req.name }}</div>
              <div class="requirement-status">
                <Tag :value="req.status" :severity="getStatusSeverity(req.status)" />
              </div>
            </div>
          </div>
          
          <div class="field remarks-field" v-if="selectedClearance.remarks">
            <label>Remarks:</label>
            <div>{{ selectedClearance.remarks }}</div>
          </div>
          
          <div class="flex justify-content-end mt-4" v-if="selectedClearance.status === 'Pending'">
            <Button 
              label="Reject" 
              icon="pi pi-times" 
              class="p-button-danger mr-2"
              @click="rejectClearance(selectedClearance)"
            />
            <Button 
              label="Approve" 
              icon="pi pi-check" 
              class="p-button-success"
              @click="approveClearance(selectedClearance)"
            />
          </div>
        </div>
      </Dialog>
    </div>
  </template>
  
  <script>
  import { ref, computed, onMounted } from 'vue';
  import { useToast } from 'primevue/usetoast';
  import { useRouter } from 'vue-router';

  export default {
    setup() {
      const toast = useToast();
      const router = useRouter();
      const displayDialog = ref(false);
      const selectedClearance = ref(null);
      const selectedTimeRange = ref({name: 'Last 7 Days', value: 7});
      
      // Sample data for recent clearances
      const recentClearances = ref([
        {
          id: 1,
          studentId: '2023-00123',
          studentName: 'Juan Dela Cruz',
          department: 'College of Engineering',
          program: 'BS Computer Engineering',
          dateSubmitted: new Date(2025, 4, 25),
          status: 'Pending',
          requirements: [
            { name: 'Library Clearance', status: 'Completed' },
            { name: 'Finance Clearance', status: 'Pending' },
            { name: 'Guidance Clearance', status: 'Pending' },
          ]
        },
        {
          id: 2,
          studentId: '2023-00124',
          studentName: 'Maria Santos',
          department: 'College of Business',
          program: 'BS Business Administration',
          dateSubmitted: new Date(2025, 4, 24),
          status: 'Approved',
          requirements: [
            { name: 'Library Clearance', status: 'Completed' },
            { name: 'Finance Clearance', status: 'Completed' },
            { name: 'Guidance Clearance', status: 'Completed' },
          ]
        },
        {
          id: 3,
          studentId: '2023-00125',
          studentName: 'Pedro Reyes',
          department: 'College of Arts and Sciences',
          program: 'BS Psychology',
          dateSubmitted: new Date(2025, 4, 23),
          status: 'Rejected',
          requirements: [
            { name: 'Library Clearance', status: 'Completed' },
            { name: 'Finance Clearance', status: 'Pending' },
            { name: 'Guidance Clearance', status: 'Rejected' },
          ]
        },
        {
          id: 4,
          studentId: '2023-00126',
          studentName: 'Ana Martinez',
          department: 'College of Education',
          program: 'BS Education',
          dateSubmitted: new Date(2025, 4, 22),
          status: 'Pending',
          requirements: [
            { name: 'Library Clearance', status: 'Pending' },
            { name: 'Finance Clearance', status: 'Pending' },
            { name: 'Guidance Clearance', status: 'Completed' },
          ]
        },
        {
          id: 5,
          studentId: '2023-00127',
          studentName: 'Luis Garcia',
          department: 'College of Engineering',
          program: 'BS Civil Engineering',
          dateSubmitted: new Date(2025, 4, 21),
          status: 'Approved',
          requirements: [
            { name: 'Library Clearance', status: 'Completed' },
            { name: 'Finance Clearance', status: 'Completed' },
            { name: 'Guidance Clearance', status: 'Completed' },
          ]
        }
      ]);

      // Computed properties for stats
      const totalStudents = computed(() => recentClearances.value.length);
      const pendingClearances = computed(() => 
        recentClearances.value.filter(c => c.status === 'Pending').length
      );
      const approvedClearances = computed(() => 
        recentClearances.value.filter(c => c.status === 'Approved').length
      );
      const rejectedClearances = computed(() => 
        recentClearances.value.filter(c => c.status === 'Rejected').length
      );

      // Format date for display
      const formatDate = (date) => {
        if (!date) return '';
        return new Date(date).toLocaleDateString('en-US', {
          year: 'numeric',
          month: 'short',
          day: 'numeric'
        });
      };

      // Get severity for status tag
      const getStatusSeverity = (status) => {
        switch (status) {
          case 'Approved':
            return 'success';
          case 'Rejected':
            return 'danger';
          case 'Pending':
            return 'warning';
          default:
            return 'info';
        }
      };

      // View clearance details
      const viewClearanceDetails = (clearance) => {
        selectedClearance.value = clearance;
        displayDialog.value = true;
      };

      // Approve clearance
      const approveClearance = (clearance) => {
        const index = recentClearances.value.findIndex(c => c.id === clearance.id);
        if (index !== -1) {
          recentClearances.value[index].status = 'Approved';
          recentClearances.value[index].requirements.forEach(req => req.status = 'Approved');
          
          toast.add({
            severity: 'success',
            summary: 'Success',
            detail: 'Clearance approved successfully',
            life: 3000
          });
        }
      };

      // Reject clearance
      const rejectClearance = (clearance) => {
        const index = recentClearances.value.findIndex(c => c.id === clearance.id);
        if (index !== -1) {
          recentClearances.value[index].status = 'Rejected';
          recentClearances.value[index].requirements.forEach(req => {
            if (req.status !== 'Approved') req.status = 'Rejected';
          });
          
          toast.add({
            severity: 'warn',
            summary: 'Rejected',
            detail: 'Clearance has been rejected',
            life: 3000
          });
        }
      };

      // Refresh data
      const refreshData = () => {
        // In a real app, this would fetch fresh data from an API
        toast.add({
          severity: 'info',
          summary: 'Refreshed',
          detail: 'Data has been refreshed',
          life: 3000
        });
      };

      return {
        displayDialog,
        selectedClearance,
        recentClearances,
        totalStudents,
        pendingClearances,
        approvedClearances,
        rejectedClearances,
        selectedTimeRange,
        timeRangeOptions: [
          { name: 'Today', value: 1 },
          { name: 'Last 7 Days', value: 7 },
          { name: 'Last 30 Days', value: 30 },
          { name: 'This Year', value: 365 }
        ],
        formatDate,
        getStatusSeverity,
        viewClearanceDetails,
        approveClearance,
        rejectClearance,
        refreshData
      };
    }
  };
  </script>
  
  <style scoped>
  .registrar-dashboard {
    padding: 1.5rem;
  }
  
  /* Header Section */
  .header-section {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 1.5rem;
  }
  
  .header-content h1 {
    margin: 0;
    font-size: 1.75rem;
    font-weight: 600;
    color: var(--primary-color);
  }
  
  .subtitle {
    margin: 0.25rem 0 0;
    color: var(--text-color-secondary);
    font-size: 0.875rem;
  }
  
  .header-actions {
    display: flex;
    gap: 1rem;
    align-items: center;
  }
  
  /* Stats Cards */
  .stats-container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 1rem;
    margin-bottom: 1.5rem;
  }
  
  .stat-card {
    background: white;
    border-radius: 8px;
    padding: 1.25rem;
    display: flex;
    align-items: center;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    transition: transform 0.2s, box-shadow 0.2s;
  }
  
  .stat-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  }
  
  .stat-icon {
    font-size: 1.75rem;
    width: 48px;
    height: 48px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 1rem;
    color: white;
  }
  
  .stat-icon i {
    font-size: 1.25rem;
  }
  
  .stat-content {
    display: flex;
    flex-direction: column;
  }
  
  .stat-value {
    font-size: 1.5rem;
    font-weight: 600;
    line-height: 1.2;
  }
  
  .stat-label {
    font-size: 0.875rem;
    color: var(--text-color-secondary);
    margin-top: 0.25rem;
  }
  
  /* Card styles */
  .card {
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    margin-bottom: 1.5rem;
    overflow: hidden;
  }
  
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.25rem 1.25rem 0;
  }
  
  .card-header h3 {
    margin: 0;
    font-size: 1.25rem;
  }
  
  .table-card {
    padding: 0 1.25rem 1.25rem;
  }
  
  .chart-card {
    padding: 1.25rem;
    height: 100%;
  }
  
  .chart-card h3 {
    margin-top: 0;
    margin-bottom: 1rem;
  }
  
  /* Clearance details */
  .clearance-details {
    padding: 0.5rem;
  }
  
  .field {
    margin-bottom: 1rem;
  }
  
  .field label {
    display: block;
    font-weight: 500;
    color: var(--text-color-secondary);
    margin-bottom: 0.25rem;
    font-size: 0.875rem;
  }
  
  .requirements-list {
    margin-top: 1rem;
  }
  
  .requirement-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem;
    border-bottom: 1px solid #e9ecef;
  }
  
  .requirement-item:last-child {
    border-bottom: none;
  }
  
  .requirement-name {
    font-weight: 500;
  }
  
  .remarks-field {
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px dashed #e9ecef;
  }
  
  /* Table styles */
  :deep(.p-datatable) {
    font-size: 0.9rem;
    
  }
  
  :deep(.p-datatable .p-datatable-thead > tr > th) {
    background: #f8f9fa;
    font-weight: 600;
    text-transform: uppercase;
    font-size: 0.75rem;
    letter-spacing: 0.5px;
    color: var(--text-color-secondary);
    border: none;
    padding: 0.75rem 1rem;
    
  }
  
  :deep(.p-datatable .p-datatable-tbody > tr) {
    transition: background-color 0.2s;
  }
  
  :deep(.p-datatable .p-datatable-tbody > tr > td) {
    padding: 1rem;
    border: none;
    border-bottom: 1px solid #e9ecef;
  }
  
  :deep(.p-datatable .p-datatable-tbody > tr:last-child > td) {
    border-bottom: none;
  }
  
  :deep(.p-datatable .p-datatable-tbody > tr:hover) {
    background-color: #f8f9fa;
  }
  
  /* Status tags */
  :deep(.p-tag) {
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
  }
  
  /* Color themes for status cards */
  .stat-card.total {
    border-left: 4px solid #3b82f6;
  }
  
  .stat-card.total .stat-icon {
    background-color: #3b82f6;
  }
  
  .stat-card.pending {
    border-left: 4px solid #F59E0B;
  }
  
  .stat-card.pending .stat-icon {
    background-color: #F59E0B;
  }
  
  .stat-card.approved {
    border-left: 4px solid #10B981;
  }
  
  .stat-card.approved .stat-icon {
    background-color: #10B981;
  }
  
  .stat-card.rejected {
    border-left: 4px solid #EF4444;
  }
  
  .stat-card.rejected .stat-icon {
    background-color: #EF4444;
  }
  
  /* Responsive adjustments */
  @media (max-width: 992px) {
    .header-section {
      flex-direction: column;
      gap: 1rem;
    }
    
    .header-actions {
      width: 100%;
      justify-content: flex-end;
    }
    
    .stats-container {
      grid-template-columns: 1fr 1fr;
    }
  }
  
  @media (max-width: 576px) {
    .stats-container {
      grid-template-columns: 1fr;
    }
  }
  
  /* Make sure dropdowns take full width of their container */
  :deep(.p-dropdown) {
    width: 100%;
  }

  </style>