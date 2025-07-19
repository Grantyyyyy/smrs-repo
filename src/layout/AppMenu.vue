<script setup>
import { ref } from 'vue';

import AppMenuItem from './AppMenuItem.vue';

const model = ref([


    {
        label: 'Instructor',
        items: [
            { label: 'My Classes', icon: 'pi pi-fw pi-calendar-clock', to: '/pages/instructor/classes' },
            { label: 'My Subjects Handled', icon: 'pi pi-fw pi-book', to: '/pages/instructor/subjects' },
            { label: 'Logout', icon: 'pi pi-fw pi-sign-out', to: '/auth/login' },
        ]
    },
    {   
        label: 'Student',
        items: [
            { label: 'My Profile', icon: 'pi pi-fw pi-user', to: '/pages/student/dashboard' },
            { label: 'My Schedules', icon: 'pi pi-fw pi-calendar-clock', to: '/pages/student/schedules' },
            { label: 'My Transcript of Records', icon: 'pi pi-fw pi-file', to: '/pages/student/grades' },
            // { label: 'My Course Prospectus', icon: 'pi pi-fw pi-file', to: '/pages/student/prospectus' },
            { label: 'My Evaluation of Grades', icon: 'pi pi-fw pi-file-plus', to: '/pages/student/evaluationgrades' },
            { label: 'My Clearance', icon: 'pi pi-fw pi-file-check', to: '/pages/student/clearance' },
            { label: 'Logout', icon: 'pi pi-fw pi-sign-out', to: '/auth/login' },
        ]
    },
    {
        label: 'DSA',
        items: [
            { label: 'DSA Dashboard', icon: 'pi pi-fw pi-home', to: '/pages/dsa/dashboard', visibleTo: ['dsa', 'admin'] },
            { label: 'Student Clearance', icon: 'pi pi-users', to: '/pages/dsa/clearance', visibleTo: ['dsa', 'admin'] },
            { label: 'Logout', icon: 'pi pi-fw pi-sign-out', to: '/auth/login' },
        ]
    },

    {
        label: 'Offices',
        label: 'Canteen Office',

        items: [
            { label: 'Student Clearance', icon: 'pi pi-users', to: '/pages/canteen/clearance', visibleTo: ['canteen', 'admin'] },
        ]
    },
    {
        label: 'Test Route',
        items: [
            { label: 'Students', icon: 'pi pi-fw pi-users', to: '/pages/students' },
            { label: 'Courses', icon: 'pi pi-fw pi-user', to: '/pages/admin/courses' },
            { label: 'Departments', icon: 'pi pi-fw pi-building', to: '/pages/admin/departments' },
            { label: 'Subject Offers', icon: 'pi pi-fw pi-briefcase', to: '/pages/admin/subjectoffers' },
            { label: 'Subjects', icon: 'pi pi-fw pi-book', to: '/pages/admin/subjects' },
            { label: 'Curriculums', icon: 'pi pi-fw pi-calendar', to: '/pages/admin/curriculums' },

        ]
    },

]);
</script>

<template>
    <ul class="layout-menu">
        <template v-for="(item, i) in model" :key="item">
            <app-menu-item v-if="!item.separator" :item="item" :index="i"></app-menu-item>
            <li v-if="item.separator" class="menu-separator"></li>
        </template>
    </ul>
</template>

<style lang="scss" scoped></style>
