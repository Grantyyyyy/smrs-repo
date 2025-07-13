import AppLayout from '@/layout/AppLayout.vue';
import { createRouter, createWebHistory } from 'vue-router';

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            component: AppLayout,
            children: [
                // Test
                {
                    path: '/pages/admin/departments',
                    name: 'departments',
                    component: () => import('@/views/pages/admin/Departments.vue'),
                },
                {
                    path: '/pages/students',
                    name: 'students',
                    component: () => import('@/views/pages/Students.vue'),
                },

                // {
                //     path: '/pages/admin/test',
                //     name: 'test-offers',
                //     component: () => import('@/views/pages/admin/TestOffers.vue')
                // },


                {
                    path: '/pages/admin/subjectoffers',
                    name: 'subjectoffers',
                    component: () => import('@/views/pages/admin/SubjectOffers.vue')
                },
                {
                    path: '/pages/admin/subjects',
                    name: 'admin-subjects',
                    component: () => import('@/views/pages/admin/Subjects.vue')
                },
                {
                    path: '/pages/admin/courses',
                    name: 'courses',
                    component: () => import('@/views/pages/admin/Courses.vue')
                },


                


                {
                    path: '/',
                    name: 'dashboard',
                    component: () => import('@/views/Dashboard.vue')
                },
                {
                    path: '/pages/instructor/classes',
                    name: 'instructor-classes',
                    component: () => import('@/views/pages/instructor/Classes.vue')
                },
                {
                    path: '/pages/instructor/subjects',
                    name: 'instructor-subjects',
                    component: () => import('@/views/pages/instructor/Subjects.vue')
                },

                {
                    path: '/pages/student/dashboard',
                    name: 'student-dashboard',
                    component: () => import('@/views/pages/student/StudentDashboard.vue')
                },
                {
                    path: '/pages/student/grades',
                    name: 'student-grades',
                    component: () => import('@/views/pages/student/StudentGradesTable.vue')
                },
                {
                    path: '/pages/student/schedules',
                    name: 'student-schedules',
                    component: () => import('@/views/pages/student/StudentSchedule.vue')
                },
                // In src/router/index.js
                {
                  path: '/pages/instructor/classes',
                  name: 'instructor-classes',
                  component: () => import('@/views/pages/instructor/Classes.vue'),
                  meta: { requiresAuth: true, role: 'instructor' }
                },
                {
                  path: '/pages/student/schedules',
                  name: 'student-schedules',
                  component: () => import('@/views/pages/student/StudentSchedule.vue'),
                  meta: { requiresAuth: true, role: 'student' }
                },
                {
                    path: '/pages/student/prospectus',
                    name: 'student-prospectus',
                    component: () => import('@/views/pages/student/StudentProspectus.vue'),
                    meta: { requiresAuth: true, role: 'student' }
                },
                {
                    path: '/pages/student/evaluationgrades',
                    name: 'student-evaluationgrades',
                    component: () => import('@/views/pages/student/EvaluationGrades.vue'),
                    meta: { requiresAuth: true, role: 'student' }
                },
                {
                    path: '/pages/student/clearance',
                    name: 'student-clearance',
                    component: () => import('@/views/pages/student/StudentClearance.vue'),
                    meta: { requiresAuth: true, role: 'student' }
                },
                //dsa
                {
                    path: '/pages/dsa/dashboard',
                    name: 'dsa-dashboard',
                    component: () => import('@/views/pages/dsa/DSADashboard.vue'),
                    meta: { requiresAuth: true, role: 'dsa' }
                },
                {
                    path: '/pages/dsa/clearance',
                    name: 'dsa-clearance',
                    component: () => import('@/views/pages/dsa/DSAClearance.vue'),
                    meta: { requiresAuth: true, role: 'dsa' }
                },

                //sample
                {
                    path: '/pages/sample/clearanceform',
                    name: 'sample-clearanceform',
                    component: () => import('@/views/pages/sample/ClearanceForm.vue'),
                    meta: { requiresAuth: true, role: 'sample' }
                },
                {
                    path: '/pages/sample/clearancedashboard',
                    name: 'sample-clearancedashboard',
                    component: () => import('@/views/pages/sample/ClearanceDashboard.vue'),
                    meta: { requiresAuth: true, role: 'sample' }
                },
                //clearance
                // {
                //     path: '/pages/cashier/clearance',
                //     name: 'cashier-office',
                //     component: () => import('@/views/pages/cashier/CashierClearance.vue'),
                //     meta: { requiresAuth: true, roles: ['cashier', 'admin'] }
                // },
                {
                    path: '/pages/library/clearance',
                    name: 'library-office',
                    component: () => import('@/views/pages/library/LibraryOffice.vue'),
                    meta: { requiresAuth: true, roles: ['library', 'admin'] }
                },
                // {
                //     path: '/pages/clinic/clearance',
                //     name: 'clinic-office',
                //     component: () => import('@/views/pages/clinic/ClinicOffice.vue'),
                //     meta: { requiresAuth: true, roles: ['clinic', 'admin'] }
                // },
                {
                    path: '/pages/canteen/clearance',
                    name: 'canteen-office',
                    component: () => import('@/views/pages/canteen/CanteenStudentClearance.vue'),
                    meta: { requiresAuth: true, roles: ['canteen', 'admin'] }
                },
                {
                    path: '/pages/office/clearance',
                    name: 'office-clearance',
                    component: () => import('@/views/pages/offices/OfficeClearance.vue'),
                    meta: { requiresAuth: true, roles: ['office', 'admin'] }
                },
                {
                    path: '/pages/office/portal',
                    name: 'office-portal',
                    component: () => import('@/views/pages/offices/OfficePortal.vue'),
                    meta: { requiresAuth: true, roles: ['office', 'admin'] }
                },
                // {
                //     path: '/pages/clinic/clearance',
                //     name: 'clinic-office',
                //     component: () => import('@/views/pages/clinic/ClinicOffice.vue'),
                //     meta: { requiresAuth: true, roles: ['clinic', 'admin'] }
                // },
                //nothing
                {
                    path: '/uikit/input',
                    name: 'input',
                    component: () => import('@/views/uikit/InputDoc.vue')
                },
                {
                    path: '/uikit/button',
                    name: 'button',
                    component: () => import('@/views/uikit/ButtonDoc.vue')
                },
                {
                    path: '/uikit/table',
                    name: 'table',
                    component: () => import('@/views/uikit/TableDoc.vue')
                },
                {
                    path: '/uikit/list',
                    name: 'list',
                    component: () => import('@/views/uikit/ListDoc.vue')
                },
                {
                    path: '/uikit/tree',
                    name: 'tree',
                    component: () => import('@/views/uikit/TreeDoc.vue')
                },
                {
                    path: '/uikit/panel',
                    name: 'panel',
                    component: () => import('@/views/uikit/PanelsDoc.vue')
                },

                {
                    path: '/uikit/overlay',
                    name: 'overlay',
                    component: () => import('@/views/uikit/OverlayDoc.vue')
                },
                {
                    path: '/uikit/media',
                    name: 'media',
                    component: () => import('@/views/uikit/MediaDoc.vue')
                },
                {
                    path: '/uikit/message',
                    name: 'message',
                    component: () => import('@/views/uikit/MessagesDoc.vue')
                },
                {
                    path: '/uikit/file',
                    name: 'file',
                    component: () => import('@/views/uikit/FileDoc.vue')
                },
                {
                    path: '/uikit/menu',
                    name: 'menu',
                    component: () => import('@/views/uikit/MenuDoc.vue')
                },
                {
                    path: '/uikit/charts',
                    name: 'charts',
                    component: () => import('@/views/uikit/ChartDoc.vue')
                },
                {
                    path: '/uikit/misc',
                    name: 'misc',
                    component: () => import('@/views/uikit/MiscDoc.vue')
                },
                {
                    path: '/uikit/timeline',
                    name: 'timeline',
                    component: () => import('@/views/uikit/TimelineDoc.vue')
                },
                {
                    path: '/pages/empty',
                    name: 'empty',
                    component: () => import('@/views/pages/Empty.vue')
                },
                {
                    path: '/pages/crud',
                    name: 'crud',
                    component: () => import('@/views/pages/Crud.vue')
                },
                {
                    path: '/documentation',
                    name: 'documentation',
                    component: () => import('@/views/pages/Documentation.vue')
                },
                {
                    path: '/pages/landing',
                    name: 'landing',
                    component: () => import('@/views/pages/Landing.vue')
                },
                {
                    path: '/pages/notfound',
                    name: 'notfound',
                    component: () => import('@/views/pages/NotFound.vue')
                },

                
                {
                    path: '/auth/access',
                    name: 'accessDenied',
                    component: () => import('@/views/pages/auth/Access.vue')
                },
                {
                    path: '/auth/error',
                    name: 'error',
                    component: () => import('@/views/pages/auth/Error.vue')
                }
            ]
        },
        {
            path: '/auth/login',
            name: 'login',
            component: () => import('@/views/pages/auth/Login.vue')
        },

    ]
});

export default router;
