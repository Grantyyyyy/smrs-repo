<script setup>
import { ref } from 'vue';

import AppMenuItem from './AppMenuItem.vue';

const model = ref([
    // {
    //     items: [
    //         { label: 'Dashboard', icon: 'pi pi-fw pi-home', to: '/' },
    //         { label: 'Schedules', icon: 'pi pi-fw pi-calendar', to: '/pages/instructor/schedules' },
    //     ]
    // },

    

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
    // {
    //     label: 'SAMPLE',
    //     items: [
    //     { label: 'Clearance Dashboard', icon: 'pi pi-id-card', to: '/pages/sample/clearancedashboard', visibleTo: ['sample', 'admin'] },
    //     { label: 'Student Clearance', icon: 'pi pi-id-card', to: '/pages/sample/cstudentclearance', visibleTo: ['sample', 'admin'] },
    //     ]
    // },
    {
        label: 'Offices',
        label: 'Canteen Office',

        items: [
            { label: 'Student Clearance', icon: 'pi pi-users', to: '/pages/canteen/clearance', visibleTo: ['canteen', 'admin'] },
            // { label: 'Cashier Office', icon: 'pi pi-money-bill', to: '/pages/cashier/clearance', visibleTo: ['cashier', 'admin'] },
            // { label: 'Library Office', icon: 'pi pi-book', to: '/pages/library/clearance', visibleTo: ['librarian', 'admin'] },
            // { label: 'Clinic Office', icon: 'pi pi-heart', to: '/pages/clinic/clearance', visibleTo: ['clinic', 'admin'] },
            // { label: 'Guidance Office', icon: 'pi pi-user', to: '/pages/guidance/clearance', visibleTo: ['guidance', 'admin'] },
            // { label: 'Canteen', icon: 'pi pi-utensil', to: '/pages/canteen/clearance', visibleTo: ['canteen', 'admin'] },
            // { label: 'Student Council', icon: 'pi pi-user', to: '/pages/student-council/clearance', visibleTo: ['student-council', 'admin'] },
            // { label: 'OSAS Staff', icon: 'pi pi-user', to: '/pages/osas-staff/clearance', visibleTo: ['osas-staff', 'admin'] },
            // { label: 'OSAS Director', icon: 'pi pi-user-tie', to: '/pages/osas-director/clearance', visibleTo: ['osas-director', 'admin'] }
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

            // { label: 'Test Offers', icon: 'pi pi-fw pi-briefcase', to: '/pages/admin/test' }, 


        ]
    },

    // { label: 'Form Layout', icon: 'pi pi-fw pi-id-card', to: '/uikit/formlayout' },
    // { label: 'Input', icon: 'pi pi-fw pi-check-square', to: '/uikit/input' },
    // { label: 'Button', icon: 'pi pi-fw pi-mobile', to: '/uikit/button', class: 'rotated-icon' },
    // { label: 'Table', icon: 'pi pi-fw pi-table', to: '/uikit/table' },
    // { label: 'List', icon: 'pi pi-fw pi-list', to: '/uikit/list' },
    // { label: 'Tree', icon: 'pi pi-fw pi-share-alt', to: '/uikit/tree' },
    // { label: 'Panel', icon: 'pi pi-fw pi-tablet', to: '/uikit/panel' },
    // { label: 'Overlay', icon: 'pi pi-fw pi-clone', to: '/uikit/overlay' },
    // { label: 'Media', icon: 'pi pi-fw pi-image', to: '/uikit/media' },
    // { label: 'Menu', icon: 'pi pi-fw pi-bars', to: '/uikit/menu' },
    // { label: 'Message', icon: 'pi pi-fw pi-comment', to: '/uikit/message' },
    // { label: 'File', icon: 'pi pi-fw pi-file', to: '/uikit/file' },
    // { label: 'Chart', icon: 'pi pi-fw pi-chart-bar', to: '/uikit/charts' },
    // { label: 'Timeline', icon: 'pi pi-fw pi-calendar', to: '/uikit/timeline' },
    // { label: 'Misc', icon: 'pi pi-fw pi-circle', to: '/uikit/misc' }
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
