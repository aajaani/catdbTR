import type { useRoute } from "vue-router";

// function allows for dynamic routes like /cats/:id to return the cat's name or whatever
// link is optional, if not provided the breadcrumb will not be a link (for the current page)
interface Breadcrumb {
	name: string | ( ( route: ReturnType< typeof useRoute > ) => string ),
	link?: string
}

export function defineBreadcrumbs( ...breadcrumbs: Breadcrumb[] ) {
	return { breadcrumbs: [ ...breadcrumbs ] };
}

export function defineSidebar( enabled: boolean ) {
	return { sidebar: enabled };
}

export function getBreadcrumbs( routeMeta: any ): Breadcrumb[] {
	if ( routeMeta && routeMeta.breadcrumbs ) {
		return routeMeta.breadcrumbs as Breadcrumb[];
	}

	return [];
}

export function isSidebarAvailable( routeMeta: any ): boolean {
	if ( routeMeta && typeof routeMeta.sidebar === "boolean" ) {
		return routeMeta.sidebar as boolean;
	}

	return false;
}