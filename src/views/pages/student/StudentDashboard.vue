<template>
  <div class="dashboard">
    <div class="content-wrapper">
      <StudentProfileCard 
        :student="user" 
        class="profile-card" 
        @profile-updated="handleProfileUpdate"
        ref="profileCard"
      />
    </div>
  </div>
</template>

<script setup>
import { UserService } from '@/service/user';
import { onMounted, ref } from 'vue';
import StudentProfileCard from './StudentProfileCard.vue';

const user = ref({});

const student = ref({
  photo: '/demo/images/profile.png',
  name: {
    firstName: 'Juan',
    middleName: 'Dela',
    lastName: 'Cruz'
  },
  studentID: '202300123',
  course: 'Bachelor of Science in Information Technology',
  year: '4th Year',
  personalInfo: {
    gender: 'Male',
    dateOfBirth: '1999-01-15',
    contactNumber: '+63 912 345 6789',
    email: 'juan.delacruz@email.com'
  },
  educationalBackground: {
    elementary: {
      school: 'St. Mary\'s Elementary School',
      graduationYear: '2010'
    },
    juniorHigh: {
      school: 'St. Mary\'s Junior High School',
      graduationYear: '2014'
    },
    seniorHigh: {
      school: 'St. Mary\'s Senior High School',
      graduationYear: '2016'
    }
  },
  guardian: {
    fullName: 'Maria Cruz',
    relationship: 'Mother',
    contactNumber: '+63 987 654 3210',
    address: '123 Main Street, Quezon City, Philippines'
  }
});

const profileCard = ref(null);

function editProfile() {
  profileCard.value.editProfile();
}

function handleProfileUpdate(updatedStudent) {
  student.value = { ...updatedStudent };
}


onMounted(async () => {
  try {
    const res = await UserService.getMe();
    user.value = res.data;
    console.log('User loaded:', user.value);

  } catch (err) {
    console.error('Failed to fetch user:', err);
  }
});
</script>

<style scoped>
.dashboard {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.content-wrapper {
  width: 100%;
  max-width: 1200px;
  display: flex;
  justify-content: center;
}

.profile-card {
  width: 100%;
}

@media (max-width: 768px) {
  .content-wrapper {
    padding: 0 1rem;
  }
}
</style>