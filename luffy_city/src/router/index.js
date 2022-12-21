import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Seckill from "@/views/Seckill";
import Course from "@/views/Course";
import FreeCourse from "@/views/FreeCourse";
import LightCourse from "@/views/LightCourse";
import CourseDetail from "@/views/CourseDetail";
import SearchView from "@/views/SearchView";
import PaySuccess from "@/views/PaySuccess";

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        name: 'home',
        component: HomeView
    },
    {
        path: '/seckill',
        name: 'seckill',
        component: Seckill
    },
    {
        path: '/actual-course',
        name: 'course',
        component: Course
    },
    {
        path: '/free-course',
        name: 'free-course',
        component: FreeCourse
    },
    {
        path: '/light-course',
        name: 'light-course',
        component: LightCourse
    },
    {
        path: '/course/detail/:id',
        name: 'detail',
        component: CourseDetail
    },
    {
        path: '/course/search',
        name: 'search',
        component: SearchView
    },
    {
        path: '/pay/success',
        name: 'paysuccess',
        component: PaySuccess
    },
]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

export default router
