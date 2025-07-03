<template>
  <div class="profile-card">
    <div class="profile-header">
      <img src="@/views/pages/student/profile.png" alt="Profile" class="profile-img" />
      <div class="profile-info">
        <h2>{{ student?.last_name }}, {{ student?.first_name }} {{ student.name?.middle_name }}</h2>
        <p class="student-id">ID: {{ student.studentID }}</p>
        <p class="course-name">{{ student.course }}</p>
        <p class="year-level">Year Level: {{ student.year }}</p>
      </div>
    </div>

    <div class="profile-sections">
      <div class="section">
        <h3>Personal Information</h3>
        <div class="info-grid">
          <div v-if="!isEditing" class="view-mode">
            <p><span class="label">Gender:</span> {{ student?.gender }}</p>
            <p><span class="label">Date of Birth:</span> {{ formatDate(student.personalInfo?.dateOfBirth) }}</p>
            <p><span class="label">Age:</span> {{ calculateAge(student.personalInfo?.dateOfBirth) }}</p>
            <p><span class="label">Contact Number:</span> {{ student?.contact_number }}</p>
            <p><span class="label">Email:</span> {{ student?.email }}</p>
          </div>
          <div v-else class="edit-mode">
            <div class="form-group">
              <label>Gender:</label>
              <input v-model="student.gender" type="text" class="form-input" />
            </div>
            <div class="form-group">
              <label>Date of Birth:</label>
              <input v-model="student.personalInfo.dateOfBirth" type="date" class="form-input" />
            </div>
            <div class="form-group">
              <label>Contact Number:</label>
              <input v-model="student.personalInfo.contactNumber" type="tel" class="form-input" />
            </div>
            <div class="form-group">
              <label>Email:</label>
              <input v-model="student.personalInfo.email" type="email" class="form-input" />
            </div>
          </div>
        </div>
      </div>

      <div class="section">
        <h3>Educational Background</h3>
        <div class="info-grid">
          <div v-if="!isEditing" class="view-mode">
            <p><span class="label">Elementary:</span> {{ student.student_profile?.elementary_school }} ({{
              student.educationalBackground?.elementary?.graduationYear }})</p>
            <p><span class="label">Junior High:</span> {{ student.student_profile?.high_school }} ({{
              student.student_profile?.juniorHigh?.graduationYear }})</p>
            <p><span class="label">Senior High:</span> {{ student.student_profile?.senior_high }} ({{
              student.student_profile?.seniorHigh?.graduationYear }})</p>
          </div>
          <div v-else class="edit-mode">
            <div class="form-group">
              <label>Elementary School:</label>
              <input v-model="student.student_profile.elementary_school" type="text" class="form-input" />
            </div>
            <div class="form-group">
              <label>Elementary Graduation Year:</label>
              <input v-model="student.educationalBackground.elementary.graduationYear" type="number"
                class="form-input" />
            </div>
            <div class="form-group">
              <label>Junior High School:</label>
              <input v-model="student.educationalBackground.juniorHigh.school" type="text" class="form-input" />
            </div>
            <div class="form-group">
              <label>Junior High Graduation Year:</label>
              <input v-model="student.educationalBackground.juniorHigh.graduationYear" type="number"
                class="form-input" />
            </div>
            <div class="form-group">
              <label>Senior High School:</label>
              <input v-model="student.educationalBackground.seniorHigh.school" type="text" class="form-input" />
            </div>
            <div class="form-group">
              <label>Senior High Graduation Year:</label>
              <input v-model="student.educationalBackground.seniorHigh.graduationYear" type="number"
                class="form-input" />
            </div>
          </div>
        </div>
      </div>

      <div class="section">
        <h3>Guardian Details</h3>
        <div class="info-grid">
          <div v-if="!isEditing" class="view-mode">
            <p><span class="label">Name:</span> {{ student.guardian?.fullName }}</p>
            <p><span class="label">Relationship:</span> {{ student.guardian?.relationship }}</p>
            <p><span class="label">Contact:</span> {{ student.guardian?.contactNumber }}</p>
            <p><span class="label">Address:</span> {{ student.guardian?.address }}</p>
          </div>
          <div v-else class="edit-mode">
            <div class="form-group">
              <label>Name:</label>
              <input v-model="student.guardian.fullName" type="text" class="form-input" />
            </div>
            <div class="form-group">
              <label>Relationship:</label>
              <input v-model="student.guardian.relationship" type="text" class="form-input" />
            </div>
            <div class="form-group">
              <label>Contact:</label>
              <input v-model="student.guardian.contactNumber" type="tel" class="form-input" />
            </div>
            <div class="form-group">
              <label>Address:</label>
              <textarea v-model="student.guardian.address" class="form-input" rows="2"></textarea>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="!isEditing" class="action-buttons">
      <button @click="editProfile" class="edit-btn">Edit Profile</button>
    </div>
    <div v-else class="action-buttons">
      <button @click="cancelEdit" class="cancel-btn">Cancel</button>
      <button @click="saveChanges" class="save-btn">Save Changes</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  student: Object
})

const emit = defineEmits(['profile-updated'])

const isEditing = ref(false)
const originalStudent = ref(null)

const editProfile = () => {
  originalStudent.value = JSON.parse(JSON.stringify(props.student))
  isEditing.value = true
}

const saveChanges = () => {
  emit('profile-updated', props.student)
  isEditing.value = false
}

const cancelEdit = () => {
  Object.assign(props.student, originalStudent.value)
  isEditing.value = false
}

const formatDate = (date) => {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const calculateAge = (date) => {
  const birthDate = new Date(date)
  let age = Math.floor((new Date() - birthDate) / (365.25 * 24 * 60 * 60 * 1000))
  return age
}
</script>

<style scoped>
.profile-card {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.profile-img {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
}

.profile-info h2 {
  margin: 0;
  font-size: 1.25rem;
  color: #333;
}

.student-id {
  color: #666;
  font-size: 0.9rem;
  margin: 4px 0 4px;
}

.course-name {
  color: #444;
  font-size: 0.9rem;
  margin: 0;
}

.year-level {
  color: #666;
  font-size: 0.85rem;
  margin: 4px 0 4px;
}

.profile-sections {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.section {
  border-top: 1px solid #eee;
  padding-top: 16px;
}

.section h3 {
  color: #333;
  margin: 0 0 12px;
  font-size: 1.1rem;
}

.info-grid {
  display: grid;
  gap: 16px;
}

.view-mode {
  display: grid;
  grid-template-columns: 1fr;
  gap: 8px;
}

.view-mode p {
  margin: 0;
  color: #444;
  font-size: 0.95rem;
  display: flex;
  align-items: center;
  gap: 8px;
}

.label {
  font-weight: 600;
  color: #333;
  min-width: 120px;
}

.edit-mode {
  display: grid;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
  width: 100%;
}

.form-group label {
  font-weight: 500;
  color: #666;
  font-size: 0.9rem;
}

.form-input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.95rem;
  transition: border-color 0.2s;
}

.form-input:focus {
  outline: none;
  border-color: #27ae5f;
}

.form-input[type="date"] {
  cursor: pointer;
}

.form-input[type="tel"] {
  -webkit-text-security: disc;
}

.form-input[rows] {
  min-height: 60px;
  resize: vertical;
}

.action-buttons {
  display: flex;
  justify-content: center;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #eee;
}

.action-buttons button {
  flex: 1;
  max-width: 120px;
}

.action-buttons button:first-child {
  margin-right: 8px;
}

.action-buttons button:last-child {
  margin-left: 8px;
}

.save-btn,
.cancel-btn,
.edit-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.85rem;
  transition: all 0.2s;
}

.save-btn {
  background-color: #10b981;
  color: white;
}

.cancel-btn {
  background-color: #c74848;
  color: white;
}

.edit-btn {
  background-color: #10b981;
  color: white;
}

.save-btn:hover {
  background-color: #0d9f6e;
}

.cancel-btn:hover {
  background-color: #dc2626;
}

.edit-btn:hover {
  background-color: #0d9f6e;
}

@media (max-width: 768px) {
  .profile-card {
    padding: 16px;
  }

  .profile-header {
    flex-direction: column;
    text-align: center;
    align-items: center;
  }

  .profile-img {
    margin-bottom: 12px;
  }

  .edit-mode {
    gap: 12px;
  }

  .form-group {
    gap: 2px;
  }
}
</style>