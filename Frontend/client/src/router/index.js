import Vue from 'vue';
import VueRouter from 'vue-router';
// import Tasks from '../components/Tasks.vue';
import Main from '../components/Main.vue';
Vue.use(VueRouter);
const pingRoutes = [
    {
        path: '/',
        name: 'Main',
        component: Main,
    },
    {
        path: '/tasks',
        name: 'Tasks',
        component: () => import(/* webpackChunkName: "about" */ '../components/Tasks.vue'),
    },
];
const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes: pingRoutes,
});
export default router;
//# sourceMappingURL=index.js.map