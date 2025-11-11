import { createRouter, createWebHistory } from 'vue-router';
import { defineBreadcrumbs, defineSidebar } from "@/router/helpers.js";
const routes = [
    {
        path: "/login",
        name: "Login",
        component: () => import("@/views/LoginView.vue"),
        meta: {
            ...defineSidebar(false)
        }
    },
    {
        path: "/",
        name: "Dashboard",
        component: () => import("@/views/DashboardView.vue"),
        meta: {
            ...defineBreadcrumbs({ name: "Ülevaade", link: "/" }),
            ...defineSidebar(true)
        }
    },
    {
        path: "/cats/:id",
        name: "CatProfile",
        component: () => import("@/views/CatProfile.vue"),
        meta: {
            ...defineBreadcrumbs({ name: "Ülevaade", link: "/" }, { name: "Kassid", link: "/cats" }, { name: "[nimi] Profiil" }),
            ...defineSidebar(true)
        }
    },
    {
        path: "/cats",
        name: "CatsList",
        component: () => import("@/views/CatsView.vue"),
        meta: {
            ...defineBreadcrumbs({ name: "Ülevaade", link: "/" }, { name: "Kassid" }),
            ...defineSidebar(true)
        }
    },
    {
        path: "/add-manager",
        name: "AddManager",
        component: () => import("@/views/AddManager.vue"),
        meta: {
            ...defineBreadcrumbs({ name: "Ülevaade", link: "/" }, { name: "Vabatahtlikud", link: "/managers" }, { name: "Lisa Vabatahtlik" }),
            ...defineSidebar(true)
        }
    },
    {
        path: "/managers",
        name: "ManagerLsist",
        component: () => import("@/views/Managers.vue"),
        meta: {
            ...defineBreadcrumbs({ name: "Ülevaade", link: "/" }, { name: "Vabatahtlikud" }),
            ...defineSidebar(true)
        }
    },
    {
        path: "/add-cat",
        name: "AddCat",
        component: () => import("@/views/AddCat.vue"),
        meta: {
            ...defineBreadcrumbs({ name: "Ülevaade", link: "/" }, { name: "Kassid", link: "/cats" }, { name: "Lisa Kass" }),
            ...defineSidebar(true)
        }
    },
    // ! has to be last, match all routes not defined above
    {
        path: "/:pathMatch(.*)*",
        name: "NotFound",
        component: () => import("@/views/NotFound.vue"),
        meta: {
            ...defineSidebar(false)
        }
    }
];
export const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes,
});
export default router;
