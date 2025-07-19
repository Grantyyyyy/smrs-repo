<template>
  <div class="min-h-screen bg-white">
    <!-- Minimal Navigation -->
    <header class="fixed w-full bg-green-100 bg-opacity/90 backdrop-blur-sm z-50 shadow-sm">
      <nav class="container mx-auto px-20 py-2">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-4">
            <img src="" alt="SMIT Logo" class="h-12 w-auto">
            <span class="text-lg font-medium text-gray-800">Santa Monica Institute of Technology</span>
          </div>
          <div class="hidden md:flex items-center space-x-8">
            <a @click="scrollToSection('about')" class="nav-link cursor-pointer">About</a>
            <a @click="scrollToSection('enrollment')" class="nav-link cursor-pointer">Enrollment</a>
            <a @click="scrollToSection('contact')" class="nav-link cursor-pointer">Contact</a>
            <div class="relative">
              <button @click="toggleDropdown" class="login-button">
                Login
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <div v-if="isDropdownOpen" class="absolute mt-2 w-40 bg-white rounded-md shadow-lg py-1">
                <router-link to="/admin-login" class="block px-4 py-2 text-sm text-black hover:bg-green-100 hover:text-green-900">
                  Admin Login
                </router-link>
                <router-link to="/student-login" class="block px-4 py-2 text-sm text-black hover:bg-green-100 hover:text-green-900">
                  Student Login
                </router-link>
                <router-link to="/faculty-login" class="block px-4 py-2 text-sm text-black hover:bg-green-100 hover:text-green-900">
                  Faculty Login
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </nav>
    </header>

    <!-- Hero Section with Minimalist Design -->
    <div class="relative h-[500px]">
      <div class="absolute inset-0 bg-cover bg-center bg-no-repeat opacity-90" 
           style="background-image: url('/img/SMIT-bgimage.png');
           ">
        <div class="absolute inset-0 bg-gradient-to-r from-black/70 to-black/50"></div>
      </div>

      <div class="container mx-auto px-6 h-full relative">
        <div class="flex items-center h-full">
          <div class="max-w-2xl pt-16">
            <h2 class="text-6xl font-bold text-green-200 ml-12 mb-6 leading-tight">
              Student Record Management System
            </h2>
          </div>
        </div>
      </div>
    </div>

    <!-- About Section with Clean Layout -->
    <section id="about" class="py-16 bg-green-100 pb-10">
      <div class="container mx-auto px-24">
        <h2 class="text-2xl font-semibold text-gray-800 mb-16 text-center">About Our Institution</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-12 text-center">
          <div class="bg-white p-6 rounded-lg shadow-xl hover:shadow-xl hover:bg-green-800 hover:text-white transition-all duration-5000 ease-in-out group">
            <h3 class="text-xl font-bold mb-1 text-green-800 group-hover:text-white">VISION</h3>
            <p class="text-sm text-gray-600 leading-relaxed group-hover:text-white">
              We, the member of SANTA MONICA INSTITUTE OF TECHNOLOGY community, envision to become a center of excellence in providing a quality and competitive education to Filipino community attaining quality living.
            </p>
          </div>
          <div class="bg-white p-6 rounded-lg shadow-xl hover:shadow-xl hover:bg-green-800 hover:text-white transition-all duration-5000 ease-in-out group">
            <h3 class="text-xl font-bold mb-1 text-green-800 group-hover:text-white">GOAL</h3>
            <p class="text-sm text-gray-600 leading-relaxed group-hover:text-white">
              Transformation of Graduates to a productive citizen in the community and to attain a quality living.
            </p>
          </div>
          <div class="bg-white p-6 rounded-lg shadow-xl hover:shadow-xl hover:bg-green-800 hover:text-white transition-all duration-5000 ease-in-out group">
            <h3 class="text-xl font-bold mb-1 text-green-800 group-hover:text-white">MISSION</h3>
            <p class="text-sm text-gray-600 leading-relaxed group-hover:text-white">
              We, commit ourselves, to: develop a Filipino equipped with the tools to attain quality of life imbued with moral an values and the sense of commitment of leadership; advocate deep understanding of cultural diversity of peace and promote environmental preservation; provide greater accessibility adnd opportunity to the poor.
            </p>
          </div>
        </div>

        <!-- Objectives with Clean List Design -->
        <div class="bg-white p-6 rounded-lg shadow-xl mt-12 hover:shadow-xl hover:bg-green-800 hover:text-white transition-all duration-5000 ease-in-out group">
          <h3 class="text-xl font-bold mb-1 text-green-800 text-center group-hover:text-white">OBJECTIVES</h3>
          <p class="font-medium text-md text-gray-700 mb-4 group-hover:text-white">SANTA MONICA INSTITUTE OF TECHNOLOGY is expected to:</p>
          <ol class="list-[upper-alpha] space-y-4 text-sm text-gray-600 pl-8 group-hover:text-white">
            <li class="leading-relaxed">include the importance of GOD/ALLAH above all, enlightened by the guidance of the Holy Spirit.</li>
            <li class="leading-relaxed">provide affordable quality education regardless of socio-economic status, sex, age, and religious affiliation.</li>
            <li class="leading-relaxed">accommodates all Students from all walks of life especially the needy, who aspire to achieve a brighter future and are given the opportunity in the development of his/her wellbeing.</li>
            <li class="leading-relaxed">provide opportunities for scholarship programs enhancing his/her personal and professional growth and development; and</li>
            <li class="leading-relaxed">realign the curriculum to inculcating good attitude and values that radiant in the realization of a transform society.</li>
          </ol>
        </div>
      </div>
    </section>

   <!-- Enrollment Updates Section -->
<section id="enrollment" class="py-16 bg-green-100">
  <div class="container mx-auto px-6">
    <h2 class="text-2xl font-semibold text-center text-gray-800 mb-16">Enrollment Updates</h2>
    <div class="max-w-3xl mx-auto">
      <div class="bg-white p-8 rounded-lg shadow-lg hover:bg-gray-100 hover:shadow-md transition-shadow">
        <h3 class="text-xl flex justify-center font-bold mb-4 text-green-800">Requirements</h3>
        <div class="flex flex-col-2 gap-72">
          <h3 class="text-md font-semibold mb-4 text-green-800">Freshmen</h3>            
          <h3 class="text-md font-semibold mb-4 text-green-800">Transferee</h3>            
        </div>
            <div class="flex flex-col-2 gap-24">
              <ul class="list-disc space-y-4 text-sm text-gray-600 pl-8">
                <li class="leading-relaxed">PSA Birth Certificate (Xerox-Clear-Copy)</li>
                <li class="leading-relaxed">Senior High School Card (Form 138) & 137</li>
                <li class="leading-relaxed">Good Moral</li>
                <li class="leading-relaxed">2pc. 2x2 ID Picture (White Background)</li>
                <li class="leading-relaxed">Brown Envelope and Folder (Long)</li>
              </ul>

              <ul class="list-disc space-y-4 text-sm text-gray-600 pl-8">
                <li class="leading-relaxed">PSA Birth Certificate (Xerox-Clear-Copy)</li>
                <li class="leading-relaxed">Transcript of Records</li>
                <li class="leading-relaxed">Evaluation of Grades</li>
                <li class="leading-relaxed">Brown Envelope and Folder (Long)</li>
                <li class="leading-relaxed">2pc. 2x2 ID Picture (White Background)</li>
                <li class="leading-relaxed">Brown Envelope and Folder (Long)</li>
                <li class="leading-relaxed">Good Moral</li>
              </ul>
            </div>
          </div>
          <!-- Add the Enroll Now button here -->
        <div class="text-center mt-8">
          <button @click="toggleEnrollmentForm" class="bg-green-800 text-white px-8 py-3 rounded-md hover:bg-green-700 transition-all shadow-sm flex items-center mx-auto">
            Enroll Now
          </button>
        </div>
      </div>
    </div>
    </section>

   <!-- Enrollment Form Modal -->
   <div v-if="showEnrollmentForm" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
     <div class="bg-white p-8 rounded-lg shadow-xl max-w-4xl w-full mx-4 max-h-[90vh] overflow-y-auto">
   
       <h3 class="text-2xl font-bold text-green-800 mb-6">Enrollment Form</h3>
       <form @submit.prevent="submitEnrollmentForm" class="space-y-8">
         <!-- Personal Information -->
         <div>
           <h4 class="text-lg font-semibold text-green-800 mb-4">Personal Information</h4>
           <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
             <div>
               <label class="block text-sm font-medium text-gray-700">Last Name*</label>
               <input type="text" v-model="enrollmentForm.lastName" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500">
             </div>
             <div>
               <label class="block text-sm font-medium text-gray-700">First Name*</label>
               <input type="text" v-model="enrollmentForm.firstName" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500">
             </div>
             <div>
               <label class="block text-sm font-medium text-gray-700">Middle Name*</label>
               <input type="text" v-model="enrollmentForm.middleName" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500">
             </div>
             <div>
               <label class="block text-sm font-medium text-gray-700">Gender*</label>
               <select v-model="enrollmentForm.gender" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500">
                 <option value="">Select Gender</option>
                 <option value="male">Male</option>
                 <option value="female">Female</option>
               </select>
             </div>
             <div>
               <label class="block text-sm font-medium text-gray-700">Date of Birth*</label>
               <input type="date" v-model="enrollmentForm.dateOfBirth" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500">
             </div>
             <div>
               <label class="block text-sm font-medium text-gray-700">Place of Birth*</label>
               <input type="text" v-model="enrollmentForm.placeOfBirth" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500">
             </div>
             <div>
               <label class="block text-sm font-medium text-gray-700">Phone Number*</label>
               <input type="tel" v-model="enrollmentForm.phoneNumber" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500">
             </div>
             <div>
               <label class="block text-sm font-medium text-gray-700">Email*</label>
               <input type="email" v-model="enrollmentForm.email" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500">
             </div>
             <div>
               <label class="block text-sm font-medium text-gray-700">Religion*</label>
               <input type="text" v-model="enrollmentForm.religion" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500">
             </div>
           </div>
         </div>

         <!-- Address Information -->
         <div>
           <h4 class="text-lg font-semibold text-green-800 mb-4">Address Information</h4>
           <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
             <div>
               <label class="block text-sm font-medium text-gray-700">Street*</label>
               <input type="text" v-model="enrollmentForm.street" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500">
             </div>
             <div>
               <label class="block text-sm font-medium text-gray-700">Barangay*</label>
               <input type="text" v-model="enrollmentForm.barangay" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500">
             </div>
             <div>
               <label class="block text-sm font-medium text-gray-700">City/Municipality*</label>
               <input type="text" v-model="enrollmentForm.cityMunicipality" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500">
             </div>
             <div>
               <label class="block text-sm font-medium text-gray-700">Province*</label>
               <input type="text" v-model="enrollmentForm.province" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500">
             </div>
             <div>
               <label class="block text-sm font-medium text-gray-700">Country*</label>
               <input type="text" v-model="enrollmentForm.country" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500">
             </div>
             <div>
               <label class="block text-sm font-medium text-gray-700">Zipcode*</label>
               <input type="text" v-model="enrollmentForm.zipcode" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500">
             </div>
           </div>
         </div>

         <!-- Guardian Information -->
         <div>
           <h4 class="text-lg font-semibold text-green-800 mb-4">Guardian Information</h4>
           <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
             <div>
               <label class="block text-sm font-medium text-gray-700">Guardian Full Name*</label>
               <input type="text" v-model="enrollmentForm.guardianFullName" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500">
             </div>
             <div>
               <label class="block text-sm font-medium text-gray-700">Guardian Contact Number*</label>
               <input type="tel" v-model="enrollmentForm.guardianContactNumber" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500">
             </div>
           </div>
         </div>

         <!-- Account Information -->
         <div>
           <h4 class="text-lg font-semibold text-green-800 mb-4">Account Information</h4>
           <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
             <div>
               <label class="block text-sm font-medium text-gray-700">Username*</label>
               <input type="text" v-model="enrollmentForm.username" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500">
             </div>
             <div>
               <label class="block text-sm font-medium text-gray-700">Password*</label>
               <input type="password" v-model="enrollmentForm.password" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500">
             </div>
           </div>
         </div>

         <!-- Last School Attended -->
         <div>
           <h4 class="text-lg font-semibold text-green-800 mb-4">Previous Education</h4>
           <div>
             <label class="block text-sm font-medium text-gray-700">Last School Attended*</label>
             <input type="text" v-model="enrollmentForm.lastSchoolAttended" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500">
           </div>
         </div>

               <!-- Academic Information -->
      <div>
        <h4 class="text-lg font-semibold text-green-800 mb-4">Academic Information</h4>
        <div class="grid grid-cols-1 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">Student Type</label>
            <select v-model="enrollmentForm.studentType" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500">
              <option value="">Select Type</option>
              <option value="freshman">Freshman</option>
              <option value="transferee">Transferee</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Course</label>
            <select v-model="enrollmentForm.course" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500">
              <option value="">Select Course</option>
              <option value="bsit">Bachelor of Elementary Education</option>
            </select>
          </div>
        </div>
      </div>

         <!-- Required Documents Checklist -->
         <div>
           <h4 class="text-lg font-semibold text-green-800 mb-4">Required Documents</h4>
           <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
             <div class="space-y-4">
               <label class="flex items-center space-x-3">
                 <input type="checkbox" v-model="enrollmentForm.documents.photo" class="rounded border-gray-300 text-green-600 focus:ring-green-500">
                 <span class="text-sm text-gray-700">2x2 ID Photo*</span>
               </label>
               <label class="flex items-center space-x-3">
                 <input type="checkbox" v-model="enrollmentForm.documents.form137" class="rounded border-gray-300 text-green-600 focus:ring-green-500">
                 <span class="text-sm text-gray-700">Form 137*</span>
               </label>
               <label class="flex items-center space-x-3">
                 <input type="checkbox" v-model="enrollmentForm.documents.form138" class="rounded border-gray-300 text-green-600 focus:ring-green-500">
                 <span class="text-sm text-gray-700">Form 138*</span>
               </label>
               <label class="flex items-center space-x-3">
                 <input type="checkbox" v-model="enrollmentForm.documents.goodMoral" class="rounded border-gray-300 text-green-600 focus:ring-green-500">
                 <span class="text-sm text-gray-700">Good Moral*</span>
               </label>
             </div>
             <div class="space-y-4">
               <label class="flex items-center space-x-3">
                 <input type="checkbox" v-model="enrollmentForm.documents.psaBirthCertificate" class="rounded border-gray-300 text-green-600 focus:ring-green-500">
                 <span class="text-sm text-gray-700">PSA Birth Certificate*</span>
               </label>
               <label class="flex items-center space-x-3">
                 <input type="checkbox" v-model="enrollmentForm.documents.honorableDismissal" class="rounded border-gray-300 text-green-600 focus:ring-green-500">
                 <span class="text-sm text-gray-700">Honorable Dismissal (for Transferee)</span>
               </label>
               <label class="flex items-center space-x-3">
                 <input type="checkbox" v-model="enrollmentForm.documents.evaluationOfGrades" class="rounded border-gray-300 text-green-600 focus:ring-green-500">
                 <span class="text-sm text-gray-700">Evaluation of Grades (for Transferee)</span>
               </label>
             </div>
           </div>
         </div>

         <!-- Form Actions -->
         <div class="flex justify-end space-x-4 pt-6">
           <button type="button" @click="showEnrollmentForm = false" class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500">
             Cancel
           </button>
           <button type="submit" class="px-4 py-2 text-sm font-medium text-white bg-green-800 hover:bg-green-700 rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500">
             Submit Application
           </button>
         </div>
       </form>
     </div>
   </div>

 
<section id="contact" class="pb-16 bg-green-100">
  <div class="container mx-auto px-4 text-sm py-4 ">
    <h2 class="text-2xl font-semibold text-center text-gray-800 mb-16">Contact Us</h2>
    <div class="max-w-6xl mx-auto grid md:grid-cols-3 gap-16">

      <!-- Phone Card -->
      <div class="bg-green-100 p-4 rounded-lg shadow-md hover:shadow-xl transition-shadow w-full h-20">
        <div class="flex items-center space-x-6 ">
          <div class="">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-green-800" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
            </svg>
          </div>
          <div class="">
            <div class="space-y-1">
              <p class="text-gray-600">(063) 221-2678</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Email Card -->
      <div class="bg-green-100 p-4 rounded-lg shadow-md hover:shadow-xl transition-shadow w-full h-20">
        <div class="flex items-center space-x-6">
          <div class="">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-green-800" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
          </div>
          <div class="">
            <div class="space-y-1">
              <p class="text-gray-600">santamonicailigan@ymail.com</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Address Card -->
            <div class="bg-green-100 p-4 rounded-lg shadow-md hover:shadow-xl transition-shadow w-full h-20">
        <div class="flex items-center space-x-6">
          <div class="">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-green-800" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
          </div>
          <div class="">
            <div class="space-y-1">
              <p class="text-gray-600">ANDRADA BLDG., CABILI AVENUE 9200 ILIGAN CITY</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<section id="contact" class="bg-green-100">
  <div class="container mx-auto px-4 text-sm pb-16">
    
    <!-- Google Maps Section -->
    <div class="max-w-6xl mx-auto">
      <div class="bg-white rounded-lg shadow-lg">
        <iframe
          src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d244.99619803541583!2d124.2346594!3d8.2296344!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x325575dc2dbf9371:0xc26fc6d7980c6b2d!2sSanta+Monica+Institute+Of+Technology!5e0!3m2!1sen!2sph!4v1709799144070!5m2!1sen!2sph&zoom=19"
          width="100%"
          height="450"
          style="border:0;"
          allowfullscreen=""
          loading="lazy"
          referrerpolicy="no-referrer-when-downgrade"
          class="rounded-lg"
        ></iframe>
      </div>
    </div>
  </div>
</section>


    <!-- Footer -->
    <footer class="bg-gray-900 text-white py-6">
      <div class="container mx-auto px-6">
        <div class="text-center">
          <p class="text-sm text-gray-400">&copy; 2024 Santa Monica Institute of Technology. All rights reserved.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isDropdownOpen: false,
      showEnrollmentForm: false,
      enrollmentForm: {
        firstName: '',
        middleName: '',
        lastName: '',
        gender: '',
        dateOfBirth: '',
        phoneNumber: '',
        email: '',
        religion: '',
        street: '',
        barangay: '',
        cityMunicipality: '',
        province: '',
        country: '',
        zipcode: '',
        guardianFullName: '',
        guardianContactNumber: '',
        username: '',
        password: '',
        lastSchoolAttended: '',
        studentType: '',
        course: '',
        documents: {
          photo: false,
          form137: false,
          form138: false,
          goodMoral: false,
          psaBirthCertificate: false,
          honorableDismissal: false,
          evaluationOfGrades: false
        }
      }
    }
  },
  mounted() {
    document.addEventListener('click', this.closeDropdown)
  },
  beforeDestroy() {
    document.removeEventListener('click', this.closeDropdown)
  },
  methods: {
    toggleDropdown() {
      this.isDropdownOpen = !this.isDropdownOpen
      if (this.isDropdownOpen) {
        this.showEnrollmentForm = false
      }
    },
    closeDropdown(event) {
      if (!event.target.closest('.relative')) {
        this.isDropdownOpen = false
      }
    },
    toggleEnrollmentForm() {
      this.showEnrollmentForm = !this.showEnrollmentForm
      if (this.showEnrollmentForm) {
        this.isDropdownOpen = false
      }
    },
    submitEnrollmentForm() {
      console.log('Form submitted:', this.enrollmentForm)
      // Reset form
      this.enrollmentForm = {
        firstName: '',
        middleName: '',
        lastName: '',
        gender: '',
        dateOfBirth: '',
        phoneNumber: '',
        email: '',
        religion: '',
        street: '',
        barangay: '',
        cityMunicipality: '',
        province: '',
        country: '',
        zipcode: '',
        guardianFullName: '',
        guardianContactNumber: '',
        username: '',
        password: '',
        lastSchoolAttended: '',
        studentType: '',
        course: '',
        documents: {
          photo: false,
          form137: false,
          form138: false,
          goodMoral: false,
          psaBirthCertificate: false,
          honorableDismissal: false,
          evaluationOfGrades: false
        }
      }
      this.showEnrollmentForm = false
      alert('Application submitted successfully!')
    },
    scrollToSection(sectionId) {
      const section = document.getElementById(sectionId);
      if (section) {
        const targetPosition = section.offsetTop - 80; 
        const startPosition = window.pageYOffset;
        const distance = targetPosition - startPosition;
        const duration = 1500;
        let start = null;

        window.history.pushState({}, '', `#${sectionId}`);
        
        function animation(currentTime) {
          if (start === null) start = currentTime;
          const timeElapsed = currentTime - start;
          const progress = Math.min(timeElapsed / duration, 1);
          
          // Easing function for smoother animation
          const ease = t => t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
          
          window.scrollTo(0, startPosition + distance * ease(progress));
          
          if (timeElapsed < duration) {
            requestAnimationFrame(animation);
          }
        }
        
        requestAnimationFrame(animation);
      }
    },
  }
}
</script>

<style scoped lang="postcss">
.nav-link {
  @apply text-gray-600;
  position: relative;
  transition: all 0.5s ease-in-out;
}

.nav-link::after {
  content: '';
  position: absolute;
  width: 0;
  height: 2px;
  bottom: -2px;
  left: 0;
  background-color: #166534; /* green-800 */
  transition: width 0.5s ease-in-out;
}

.nav-link:hover {
  @apply text-green-800;
}

.nav-link:hover::after {
  width: 100%;
}

.login-button {
  @apply bg-green-800 text-white px-4 py-2 rounded-md shadow-sm flex items-center;
  transition: all 0.5s ease-in-out;
}

.login-button:hover {
  @apply bg-green-700;
  transform: translateY(-1px);
}

.transition-all {
  transition: all 0.5s ease-in-out;
}

.shadow-sm {
  transition: box-shadow 0.3s ease-in-out;
}
</style>
