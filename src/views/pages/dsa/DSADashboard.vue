<template>
    <div class="dsa-dashboard">
      <!-- Stats Cards -->
      <div class="stats-container">
        <div class="stat-card total" @click="filterByStatus('')" style="cursor: pointer">
          <div class="stat-icon"><i class="pi pi-users"></i></div>
          <div class="stat-content">
            <div class="stat-value">{{ totalStudents }}</div>
            <div class="stat-label">Total Students</div>
  
          </div>
        </div>
        <div class="stat-card cleared" @click="filterByStatus('Cleared')" style="cursor: pointer">
          <div class="stat-icon"><i class="pi pi-check-circle"></i></div>
          <div class="stat-content">
            <div class="stat-value">{{ clearedCount }}</div>
            <div class="stat-label">Cleared</div>
          </div>
        </div>
        <div class="stat-card pending" @click="filterByStatus('Pending')" style="cursor: pointer">
          <div class="stat-icon"><i class="pi pi-clock"></i></div>
          <div class="stat-content">
            <div class="stat-value">{{ pendingCount }}</div>
            <div class="stat-label">Pending</div>
          </div>
        </div>
        <div class="stat-card enrolled" @click="filterByStatus('Enrolled')" style="cursor: pointer">
          <div class="stat-icon"><i class="pi pi-bookmark"></i></div>
          <div class="stat-content">
            <div class="stat-value">{{ enrolledCount }}</div>
            <div class="stat-label">Enrolled</div>
          </div>
        </div>
  
              <!-- 10/10 Totl Students with percentage -->
        <!-- <div class="stat-card pending" @click="filterByStatus('Pending')" style="cursor: pointer">
          <div class="stat-icon"><i class="pi pi-clock"></i></div>
          <div class="stat-content">
            <div class="stat-value">{{ pendingCount }} <span class="stat-total">/ {{ totalPendingCount }}</span></div>
            <div class="stat-label">Pending</div>
            <div class="stat-percentage">
              {{ totalStudents > 0 ? Math.round((pendingCount / totalStudents) * 100) : 0 }}% of filtered
              <span v-if="totalStudents !== totalAllStudents">
                ({{ Math.round((totalPendingCount / totalAllStudents) * 100) }}% of all)
              </span>
            </div>
          </div>
        </div> -->
  
      </div>
  
      <!-- Main Content -->
      <div class="main-content">
        <!-- Charts Section -->
        <div class="grid">
          <div class="col-12 md:col-8">
            <div class="chart-card">
              <h3>Clearance Status Overview</h3>
              <Chart type="bar" :data="statusChartData" :options="chartOptions" class="chart-container" />
            </div>
          </div>
          <div class="col-12 md:col-4">
            <div class="chart-card">
              <h3>Department-wise Distribution</h3>
              <Chart type="pie" :data="departmentChartData" :options="pieOptions" class="chart-container" />
            </div>
          </div>
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
  import { ref, computed } from 'vue';
  import { useToast } from 'primevue/usetoast';
  import { useRouter } from 'vue-router';
  import Chart from 'primevue/chart';
  
  export default {
    components: {
      Chart
    },
    setup() {
      const toast = useToast();
      const router = useRouter();
      const displayDialog = ref(false);
      const selectedClearance = ref(null);
      
      // Sample data - replace with your actual data
      const clearances = ref([
        {
          studentId: '2023-001',
          studentName: 'John Doe',
          department: 'Computer Science',
          dateSubmitted: '2023-06-15',
          status: 'Pending',
          requirements: [
            { name: 'Library Clearance', status: 'Pending' },
            { name: 'Finance Clearance', status: 'Pending' },
            { name: 'Department Clearance', status: 'Pending' }
          ]
        },
        // Add more sample data as needed
      ]);
  
      // Computed properties for stats
      const totalStudents = computed(() => clearances.value.length);
      const pendingClearances = computed(() => 
        clearances.value.filter(c => c.status === 'Pending').length
      );
      const approvedClearances = computed(() => 
        clearances.value.filter(c => c.status === 'Approved').length
      );
      const rejectedClearances = computed(() => 
        clearances.value.filter(c => c.status === 'Rejected').length
      );
  
      // Chart data for status overview
      const statusChartData = computed(() => {
        const statusCounts = {
          'Pending': 0,
          'Approved': 0,
          'Rejected': 0
        };
        
        clearances.value.forEach(clearance => {
          statusCounts[clearance.status] = (statusCounts[clearance.status] || 0) + 1;
        });
        
        return {
          labels: Object.keys(statusCounts),
          datasets: [
            {
              label: 'Clearance Status',
              backgroundColor: ['#FFA726', '#66BB6A', '#EF5350'],
              data: Object.values(statusCounts)
            }
          ]
        };
      });
  
      // Chart data for department distribution
      const departmentChartData = computed(() => {
        const departmentMap = {};
        
        clearances.value.forEach(clearance => {
          if (!departmentMap[clearance.department]) {
            departmentMap[clearance.department] = 0;
          }
          departmentMap[clearance.department]++;
        });
        
        const backgroundColors = [
          '#42A5F5', '#66BB6A', '#FFA726', '#26C6DA', '#7E57C2',
          '#EC407A', '#8D6E63', '#78909C', '#5C6BC0', '#26A69A'
        ];
        
        return {
          labels: Object.keys(departmentMap),
          datasets: [
            {
              data: Object.values(departmentMap),
              backgroundColor: backgroundColors.slice(0, Object.keys(departmentMap).length),
              hoverBackgroundColor: backgroundColors.slice(0, Object.keys(departmentMap).length)
            }
          ]
        };
      });
  
      const chartOptions = ref({
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top',
          },
          title: {
            display: true,
            text: 'Clearance Status Distribution',
            font: {
              size: 16
            }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              stepSize: 1
            }
          }
        }
      });
  
      const pieOptions = ref({
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'right',
          },
          title: {
            display: true,
            text: 'Clearance by Department',
            font: {
              size: 16
            }
          }
        }
      });
  
      // Format date for display
      const formatDate = (date) => {
        if (!date) return '';
        return new Date(date).toLocaleDateString('en-US', {
          year: 'numeric',
          month: 'short',
          day: 'numeric'
        });
      };
  
      // Get severity for status tags
      const getStatusSeverity = (status) => {
        switch (status) {
          case 'Approved':
            return 'success';
          case 'Rejected':
            return 'danger';
          case 'Pending':
          default:
            return 'warning';
        }
      };
  
      // View clearance details
      const viewClearanceDetails = (clearance) => {
        selectedClearance.value = { ...clearance };
        displayDialog.value = true;
      };
  
      // Approve clearance
      const approveClearance = (clearance) => {
        const index = clearances.value.findIndex(c => c.studentId === clearance.studentId);
        if (index !== -1) {
          clearances.value[index].status = 'Approved';
          toast.add({
            severity: 'success',
            summary: 'Success',
            detail: 'Clearance approved successfully',
            life: 3000
          });
        }
        displayDialog.value = false;
      };
  
      // Reject clearance
      const rejectClearance = (clearance) => {
        const index = clearances.value.findIndex(c => c.studentId === clearance.studentId);
        if (index !== -1) {
          clearances.value[index].status = 'Rejected';
          toast.add({
            severity: 'success',
            summary: 'Success',
            detail: 'Clearance rejected',
            life: 3000
          });
        }
        displayDialog.value = false;
      };
  
      // Refresh data
      const refreshData = () => {
        // In a real app, you would fetch fresh data here
        toast.add({
          severity: 'info',
          summary: 'Refreshed',
          detail: 'Data has been refreshed',
          life: 2000
        });
      };
  
      return {
        displayDialog,
        selectedClearance,
        statusChartData,
        departmentChartData,
        chartOptions,
        pieOptions,
        clearances,
        formatDate,
        getStatusSeverity,
        viewClearanceDetails,
        approveClearance,
        rejectClearance,
        refreshData,
        totalStudents,
        pendingClearances,
        approvedClearances,
        rejectedClearances
      };
    },
  };
  </script>
  
  <style scoped>
.dsa-container {
  background-color: #fff;
  padding: 1rem;
  border-radius: 12px;
}

/* Status tags */
:deep(.p-tag) {
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  border: 1px solid;
}

:deep(.p-tag.status-pending) {
  background-color: #fff3cd;
  color: #856404;
  border-color: #fcefc2;
}

:deep(.p-tag.status-cleared) {
  background-color: #d4edda;
  color: #155724;
  border-color: #c3e6cb;
}

:deep(.p-tag.status-enrolled) {
  background-color: #cbb6fa;
  color: #32254f;
  border-color: #ab86fc;
}

/* Color themes for status cards */
.stat-card.total {
  border-left: 4px solid #2563eb;
}

.stat-card.total .stat-icon {
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
}

.stat-card.cleared {
  border-left: 4px solid #10B981;
}

.stat-card.cleared .stat-icon {
  background: linear-gradient(135deg, #10B981 0%, #059669 100%);
}

.stat-card.pending {
  border-left: 4px solid #F59E0B;
}

.stat-card.pending .stat-icon {
  background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
}

.stat-card.enrolled {
  border-left: 4px solid #7c3aed;
}

.stat-card.enrolled .stat-icon {
  background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%);
}

/* Stats Cards */
.stats-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}

.stat-card {
  background: #fff;
  border-radius: 10px;
  padding: 1.25rem;
  display: flex;
  align-items: center;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  transition: transform 0.2s, box-shadow 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

.stat-icon {
  font-size: 1.75rem;
  min-width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 1rem;
  color: white;
  background: var(--primary-color);
}

.stat-icon i {
  font-size: 1.25rem;
}

.stat-content {
  min-width: 0; /* Prevents flex item from overflowing */
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 600;
  line-height: 1.2;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.stat-label {
  font-size: 0.875rem;
  color: var(--text-color-secondary);
  margin-top: 0.25rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.stat-total {
  font-size: 0.8em;
  opacity: 0.8;
  font-weight: normal;
}

.stat-percentage {
  font-size: 0.75rem;
  color: var(--text-secondary-color);
  margin-top: 0.25rem;
}

/* Specific styles for enrolled card */
.stat-card.enrolled .stat-icon {
  background: #7c3aed; /* Green color for enrolled */
}

/* Card styles */
.card {
  display: flex;
  flex-direction: column;
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  margin: 1.5rem;
  overflow: hidden;
  height: calc(100% - 3rem);
  width: calc(100% - 3rem);
}
  
  /* Chart Cards */
  .chart-card {
    background: white;
    border-radius: 8px;
    padding: 1.25rem;
    height: 100%;
    box-shadow: 0 2px 1px -1px rgba(0, 0, 0, 0.2), 0 1px 1px 0 rgba(0, 0, 0, 0.14), 0 1px 3px 0 rgba(0, 0, 0, 0.12);
    margin-top: 1rem;
    margin-bottom: 1rem;
  }
  
  .chart-card h3 {
    margin: 0 0 1.5rem 0;
    color: var(--text-color);
    font-size: 1.1rem;
    font-weight: 600;
  }
  
  .chart-container {
    width: 100%;
    height: 300px;
    position: relative;
  }
  
  /* Responsive adjustments */
  @media (max-width: 960px) {
    .chart-card {
      margin-bottom: 1.5rem;
    }
    
    .chart-container {
      height: 350px;
    }
  }
  
  /* Rest of your existing styles */
  .card {
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    border-radius: 6px;
    background: var(--surface-card);
    box-shadow: 0 2px 1px -1px rgba(0, 0, 0, 0.2), 0 1px 1px 0 rgba(0, 0, 0, 0.14), 0 1px 3px 0 rgba(0, 0, 0, 0.12);
  }
  
  h3 {
    margin-top: 0;
    margin-bottom: 1rem;
    color: var(--text-color);
  }
  
  .clearance-details .field {
    margin-bottom: 1rem;
  }
  
  .clearance-details label {
    display: block;
    font-weight: 500;
    margin-bottom: 0.25rem;
    color: var(--text-color-secondary);
  }
  
  .requirements-list {
    margin: 1rem 0;
    border: 1px solid var(--surface-border);
    border-radius: 4px;
    overflow: hidden;
  }
  
  .requirement-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem 1rem;
    border-bottom: 1px solid var(--surface-border);
  }
  
  .requirement-item:last-child {
    border-bottom: none;
  }
  
  .requirement-name {
    flex: 1;
  }
  
  .remarks-field {
    background-color: var(--surface-ground);
    padding: 1rem;
    border-radius: 4px;
    margin-top: 1rem;
  }
  
  :deep(.p-dialog .p-dialog-header) {
    padding: 1.5rem 1.5rem 0.5rem 1.5rem;
  }
  
  :deep(.p-dialog .p-dialog-content) {
    padding: 0 1.5rem 1.5rem 1.5rem;
  }
  
  :deep(.p-datatable .p-datatable-thead > tr > th) {
    background: var(--surface-card);
  }
  
  :deep(.p-dropdown) {
    width: 100%;
  }
  </style>