import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
	{
		path: "/",
		name: "Dashboard",
		component: ( ) => import( "@/views/DashboardView.vue" ),
		meta: {
			breadcrumbs: [
				{ name: "Ulevaade", link: "/" }
			]
		}
	},
	{
		path: "/cats",
		name: "CatsList",
		component: ( ) => import( "@/views/CatsView.vue" ),
		meta: {
			breadcrumbs: [
				{ name: "Ulevaade", link: "/" },
				{ name: "Kassid" }
			]
		}
	},
	{
		path: "/add-manager",
		name: "AddManager",
		component: ( ) => import( "@/views/AddManager.vue" ),
		meta: {
			breadcrumbs: [
				{ name: "Ulevaade", link: "/" },
				{ name: "Vabatahtlikud", link: "/managers" },
				{ name: "Lisa Hooldaja" },
			]
		}
	},
		{
		path: "/managers",
		name: "ManagerLsist",
		component: ( ) => import( "@/views/Managers.vue" ),
		meta: {
			breadcrumbs: [
				{ name: "Ulevaade", link: "/" },
				{ name: "Vabatahtlikud" },
			]
		}
	},
	{
		path: "/add-cat",
		name: "AddCat",
		component: ( ) => import( "@/views/AddCat.vue" ),
		meta: {
			breadcrumbs: [
				{ name: "Ulevaade", link: "/" },
				{ name: "Kassid", link: "/cats" },
				{ name: "Lisa Kass" },
			]
		}
	},

	// ! has to be last, match all routes not defined above
	{
		path: "/:pathMatch(.*)*",
		name: "NotFound",
		component: () => import( "@/views/NotFound.vue" ),
	}
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

export default router

